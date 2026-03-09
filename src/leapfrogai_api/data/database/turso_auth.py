"""Turso authentication implementation."""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Any
from dataclasses import dataclass
import aiosqlite
import jwt
from leapfrogai_api.data.database.base import AuthClient


@dataclass
class User:
    """User model."""
    id: str
    email: str
    encrypted_password: str = ""
    email_confirmed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    is_active: bool = True
    is_admin: bool = False
    metadata: dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class UserResponse:
    """Response wrapper for get_user."""
    user: User


@dataclass
class Session:
    """Session model."""
    id: str
    user_id: str
    token_hash: str
    expires_at: datetime
    created_at: Optional[datetime] = None


class TursoAuthClient(AuthClient):
    """Turso authentication client.
    
    Provides three authentication methods:
    1. API Key authentication (for programmatic access)
    2. Email/Password authentication (for UI login)
    3. JWT token validation (for session management)
    
    Integration points:
    - UDS Keycloak: Use Keycloak tokens, store user_id mapping
    - Custom JWT: Generate and validate our own tokens
    - API Keys: Simple token lookup in api_keys table
    """
    
    def __init__(self, db_path: str, jwt_secret: str = "change-me-in-production"):
        """Initialize Turso auth client.
        
        Args:
            db_path: Path to SQLite database
            jwt_secret: Secret key for JWT signing
        """
        self.db_path = db_path
        self.jwt_secret = jwt_secret
        self._current_user_id: Optional[str] = None
        self._access_token: Optional[str] = None
    
    async def get_user(self, token: str | None = None) -> UserResponse:
        """Get current authenticated user.
        
        Supports three token types:
        1. API Key: "lfai_<key>" format
        2. JWT Token: Standard JWT format
        3. Session Token: Opaque session identifier
        
        Args:
            token: Authentication token (optional if set_session was called)
            
        Returns:
            UserResponse with user data
            
        Raises:
            Exception: If authentication fails
        """
        if not token and not self._access_token:
            raise Exception("No authentication token provided")
        
        token = token or self._access_token
        
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            
            # Try API Key authentication
            if token.startswith("lfai_"):
                return await self._authenticate_api_key(db, token)
            
            # Try JWT token authentication
            elif token.count('.') == 2:  # JWT format: header.payload.signature
                return await self._authenticate_jwt(db, token)
            
            # Try session token authentication
            else:
                return await self._authenticate_session(db, token)
    
    async def _authenticate_api_key(self, db, token: str) -> UserResponse:
        """Authenticate with API key."""
        # Hash the token
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        # Look up API key
        async with db.execute(
            "SELECT user_id, expires_at FROM api_keys WHERE key_hash = ? AND is_active = 1",
            [token_hash]
        ) as cursor:
            row = await cursor.fetchone()
            
            if not row:
                raise Exception("Invalid API key")
            
            # Check expiration
            if row['expires_at']:
                expires_at = datetime.fromisoformat(row['expires_at'])
                if datetime.utcnow() > expires_at:
                    raise Exception("API key expired")
            
            user_id = row['user_id']
            
            # Get user
            async with db.execute(
                "SELECT * FROM users WHERE id = ? AND is_active = 1",
                [user_id]
            ) as cursor:
                user_row = await cursor.fetchone()
                
                if not user_row:
                    raise Exception("User not found or inactive")
                
                user = User(
                    id=user_row['id'],
                    email=user_row['email'],
                    encrypted_password=user_row['encrypted_password'],
                    is_active=bool(user_row['is_active']),
                    is_admin=bool(user_row['is_admin']),
                    metadata=user_row['metadata'] or {}
                )
                
                return UserResponse(user=user)
    
    async def _authenticate_jwt(self, db, token: str) -> UserResponse:
        """Authenticate with JWT token."""
        try:
            # Decode JWT
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            user_id = payload.get('sub') or payload.get('user_id')
            
            if not user_id:
                raise Exception("Invalid JWT: missing user_id")
            
            # Get user
            async with db.execute(
                "SELECT * FROM users WHERE id = ? AND is_active = 1",
                [user_id]
            ) as cursor:
                user_row = await cursor.fetchone()
                
                if not user_row:
                    raise Exception("User not found or inactive")
                
                user = User(
                    id=user_row['id'],
                    email=user_row['email'],
                    encrypted_password=user_row['encrypted_password'],
                    is_active=bool(user_row['is_active']),
                    is_admin=bool(user_row['is_admin']),
                    metadata=user_row['metadata'] or {}
                )
                
                return UserResponse(user=user)
        
        except jwt.ExpiredSignatureError:
            raise Exception("JWT token expired")
        except jwt.InvalidTokenError as e:
            raise Exception(f"Invalid JWT token: {str(e)}")
    
    async def _authenticate_session(self, db, token: str) -> UserResponse:
        """Authenticate with session token."""
        # Hash the token
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        # Look up session
        async with db.execute(
            "SELECT user_id, expires_at FROM sessions WHERE token_hash = ?",
            [token_hash]
        ) as cursor:
            row = await cursor.fetchone()
            
            if not row:
                raise Exception("Invalid session token")
            
            # Check expiration
            expires_at = datetime.fromisoformat(row['expires_at'])
            if datetime.utcnow() > expires_at:
                raise Exception("Session expired")
            
            user_id = row['user_id']
            
            # Get user
            async with db.execute(
                "SELECT * FROM users WHERE id = ? AND is_active = 1",
                [user_id]
            ) as cursor:
                user_row = await cursor.fetchone()
                
                if not user_row:
                    raise Exception("User not found or inactive")
                
                user = User(
                    id=user_row['id'],
                    email=user_row['email'],
                    encrypted_password=user_row['encrypted_password'],
                    is_active=bool(user_row['is_active']),
                    is_admin=bool(user_row['is_admin']),
                    metadata=user_row['metadata'] or {}
                )
                
                return UserResponse(user=user)
    
    async def set_session(self, access_token: str, refresh_token: str = None) -> None:
        """Set session tokens.
        
        Stores the access token for subsequent get_user() calls.
        Also creates a session record in the database.
        
        Args:
            access_token: Access token (JWT or opaque token)
            refresh_token: Refresh token (optional)
        """
        self._access_token = access_token
        self._current_user_id = None
        
        # If it's a JWT, extract user_id
        if access_token.count('.') == 2:
            try:
                payload = jwt.decode(access_token, self.jwt_secret, algorithms=['HS256'])
                self._current_user_id = payload.get('sub') or payload.get('user_id')
            except:
                pass
        
        # Store session in database
        if self._current_user_id:
            session_id = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(access_token.encode()).hexdigest()
            expires_at = datetime.utcnow() + timedelta(hours=24)
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """INSERT INTO sessions (id, user_id, token_hash, expires_at)
                       VALUES (?, ?, ?, ?)""",
                    [session_id, self._current_user_id, token_hash, expires_at.isoformat()]
                )
                await db.commit()
    
    async def create_api_key(self, user_id: str, name: str, expires_at: Optional[datetime] = None) -> str:
        """Create a new API key for a user.
        
        Args:
            user_id: User ID
            name: API key name/description
            expires_at: Expiration date (optional)
            
        Returns:
            API key string (lfai_<random>)
        """
        # Generate API key
        api_key = f"lfai_{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        key_id = secrets.token_urlsafe(16)
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT INTO api_keys (id, user_id, key_hash, name, expires_at)
                   VALUES (?, ?, ?, ?, ?)""",
                [key_id, user_id, key_hash, name, expires_at.isoformat() if expires_at else None]
            )
            await db.commit()
        
        return api_key
    
    async def create_user(self, email: str, password: str, metadata: dict = None) -> User:
        """Create a new user.
        
        Args:
            email: User email
            password: Plain text password (will be hashed)
            metadata: Additional user metadata
            
        Returns:
            Created User object
        """
        user_id = secrets.token_urlsafe(16)
        # TODO: Use proper password hashing (bcrypt/argon2)
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT INTO users (id, email, encrypted_password, metadata)
                   VALUES (?, ?, ?, ?)""",
                [user_id, email, encrypted_password, metadata or {}]
            )
            await db.commit()
        
        return User(
            id=user_id,
            email=email,
            encrypted_password=encrypted_password,
            metadata=metadata or {}
        )
    
    async def sign_in(self, email: str, password: str) -> tuple[str, str]:
        """Sign in user with email and password.
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            Tuple of (access_token, refresh_token)
            
        Raises:
            Exception: If authentication fails
        """
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            
            # Find user
            async with db.execute(
                "SELECT * FROM users WHERE email = ? AND encrypted_password = ? AND is_active = 1",
                [email, password_hash]
            ) as cursor:
                user_row = await cursor.fetchone()
                
                if not user_row:
                    raise Exception("Invalid email or password")
                
                user_id = user_row['id']
        
        # Generate tokens
        access_token = jwt.encode(
            {
                'sub': user_id,
                'email': email,
                'exp': datetime.utcnow() + timedelta(hours=1),
                'iat': datetime.utcnow()
            },
            self.jwt_secret,
            algorithm='HS256'
        )
        
        refresh_token = secrets.token_urlsafe(32)
        
        # Set session
        await self.set_session(access_token, refresh_token)
        
        return access_token, refresh_token

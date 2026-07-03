"""Database session dependency."""

import logging
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from cowabunga_api.data.database.base import DatabaseClient
from cowabunga_api.backend.security.api_key import APIKey

logger = logging.getLogger(__name__)

security = HTTPBearer()


async def init_database_client(
    auth_creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> DatabaseClient:
    """
    Returns an authenticated database client using the provided token.

    Parameters:
        auth_creds (HTTPAuthorizationCredentials): the auth credentials for the user that include the bearer token

    Returns:
        DatabaseClient: a client instantiated with the authenticated session
    """
    from cowabunga_api.utils.database_factory import create_database_client

    client = await create_database_client()

    # Try JWT Auth first
    if _validate_jwt_token(auth_creds.credentials):
        try:
            await client.auth.set_session(
                access_token=auth_creds.credentials, refresh_token="dummy"
            )
        except Exception as e:
            logger.exception("\t%s", e)
            raise HTTPException(
                detail="Token has expired or is not valid. Generate a new token",
                status_code=status.HTTP_401_UNAUTHORIZED,
            ) from e

        if await _validate_jwt_authorization(client, auth_creds.credentials):
            return client

    # Try API Key Auth
    try:
        api_key = APIKey.parse(auth_creds.credentials)

        client.options.auto_refresh_token = False
        client.options.headers.update({"x-custom-api-key": api_key.unique_key})

        if not await _validate_api_authorization(client):
            raise HTTPException(
                detail="API Key has expired or is not valid. Generate a new token",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        return client
    except ValueError as e:
        logger.exception("\t%s", e)
        raise HTTPException(
            detail="Failed to validate API Key",
            status_code=status.HTTP_401_UNAUTHORIZED,
        ) from e


# This variable needs to be added to each endpoint even if it's not used to ensure auth is required for the endpoint
Session = Annotated[DatabaseClient, Depends(init_database_client)]


async def _validate_api_authorization(session: DatabaseClient) -> bool:
    """
    Check if the provided API key is valid

    Parameters:
        session (DatabaseClient): a session with x-custom-api-key header

    Returns:
        bool: True if the API key is valid, False otherwise
    """

    response = await session.table("api_keys").select("*").execute()

    if not response or not response.data:
        return False

    return True


async def _validate_jwt_authorization(session: DatabaseClient, authorization: str) -> bool:
    """
    Check if the provided user's JWT token is valid, raises a 403 if not

    Parameters:
        session (DatabaseClient): the default session
        authorization (str): the JWT token for the user
    """

    authorized: bool = False

    if authorization:
        try:
            user_response = await session.auth.get_user(
                authorization.replace("Bearer ", "")
            )

            if user_response:
                authorized = True

        except Exception:
            authorized = False

    if not authorized:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return authorized


def _validate_jwt_token(token: str) -> bool:
    """
    Check if the provided JWT token is valid

    Parameters:
        token (str): the JWT token

    Returns:
        bool: True if the token is valid, False otherwise
    """

    try:
        _header, _payload, _signature = token.split(".")
        if not _header or not _payload or not _signature:
            return False
        return True
    except ValueError:
        return False

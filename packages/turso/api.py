"""Simple HTTP API for Turso SQLite database."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aiosqlite
import os

app = FastAPI(title="Turso SQLite API")
DB_PATH = os.getenv("TURSO_DATABASE_PATH", "/data/cowabunga.db")


class QueryRequest(BaseModel):
    """Request model for SQL queries."""
    query: str
    params: list = []


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "database": "turso"}


@app.post("/query")
async def execute_query(request: QueryRequest):
    """Execute SQL query."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        try:
            async with db.execute(request.query, request.params) as cursor:
                rows = await cursor.fetchall()
                return {"data": [dict(row) for row in rows]}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

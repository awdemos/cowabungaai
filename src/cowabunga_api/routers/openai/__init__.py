"""OpenAI-compliant router utilities."""

from fastapi import HTTPException, status


def raise_parse_error(resource: str, exc: Exception) -> None:
    """Raise a 400 HTTPException for unparseable request data."""
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unable to parse {resource} request",
    ) from exc

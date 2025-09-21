from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from consumer.database.dbsqlite import save_events_to_db
from consumer.file_storage.log_file import save_events_to_file
from consumer.schemas import Event


async def check_api_key(
    api_key: str = Depends(APIKeyHeader(name="my-api-Key", auto_error=False))
) -> None:
    """Checks the api key from the requet header"""
    if api_key != "secret":
        raise HTTPException(status_code=403, detail="Invalid API Key")


async def save_to_events(events: list[Event], storage_type: str) -> tuple[bool, str]:
    """Saves events to file or database"""
    if storage_type.lower() == "db":
        status, message = await save_events_to_db(events)
    elif storage_type.lower() == "file":
        status, message = await save_events_to_file(events)
    else:
        status, message = False, f"Storage type not supported: {storage_type}"

    return status, message

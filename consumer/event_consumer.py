import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from consumer.configuration.config import settings
from consumer.database.dbsqlite import init_sqlite_db
from consumer.schemas import Event
from consumer.services import check_api_key, save_to_events

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.STORAGE_TYPE.lower() == "db":
        logger.info("Creating events table")
        await init_sqlite_db()
        logger.info("Created events table")
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/event", dependencies=[Depends(check_api_key)])
async def incoming_event_parse(events: list[Event]) -> dict[str, str]:
    logger.info(f"[GOT EVENT]: {events}")
    is_succesful_save, message = await save_to_events(
        events=events, storage_type=settings.STORAGE_TYPE
    )

    logger.info(message)

    return {"success": is_succesful_save, "detail": message}

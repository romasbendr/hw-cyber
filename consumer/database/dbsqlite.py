import logging
from pathlib import Path

import aiosqlite

from consumer.configuration.config import settings
from consumer.schemas import Event

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

DB_FILE = Path(settings.DB_URL)


async def init_sqlite_db() -> None:
    """Creates sqlite events table"""
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         event_type TEXT NOT NULL,
                         event_payload TEXT NOT NULL
                         )
            """
        )
        await db.commit()


async def save_events_to_db(events: list[Event]) -> tuple[bool, str]:
    """Saves all events inside events list"""
    events_counts = len(events)
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            await db.executemany(
                """
                INSERT INTO events (event_type, event_payload) VALUES (?,?)
                """,
                [(event.event_type, event.event_payload) for event in events],
            )
            await db.commit()
        return True, f"Successful insert of {events_counts}"

    except Exception as e:
        logger.info(f"Error while writing events: {str(e)}")
        return False, e

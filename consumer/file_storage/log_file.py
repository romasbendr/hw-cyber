import json
import logging

import aiofiles

from consumer.configuration.config import settings
from consumer.schemas import Event

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


async def save_events_to_file(events: list[Event]) -> tuple[bool, str]:
    """Saves events to a file"""
    try:
        async with aiofiles.open(settings.STORAGE_FILE, "a", encoding="utf-8") as f:
            for event in events:
                await f.write(json.dumps(event.model_dump()) + "\n")
    except Exception as e:
        msg = f"Failed to save events to a file: {str(e)}"
        logger.info(msg)
        return False, msg

    return True, "Events saved to a file"

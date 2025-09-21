import asyncio
import json
import logging
import random
from typing import Any

import httpx

from propagator.configuration.config import settings

# NOTE: I comment this because maybe the propagator is ment to be random streaming source
# personally i would add check before sending
# class Event(BaseModel):
#     event_type: Any
#     event_payload: Any


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def read_tasks_json(
    events_file_path: str = settings.EVENTS_FILE,
) -> list[dict[Any, Any]]:
    """Reads events/tasks from JSON file to dict and returns the list"""
    try:

        with open(events_file_path, "r", encoding="utf-8") as f:
            events_json = json.load(f)

    except json.JSONDecodeError as e:
        logger.error(f"Error reading events: {e}")

    logger.info(f"Read events from file: {events_file_path}")

    # events = [Event(**event) for event in events_json]

    return events_json


async def send_event(event: dict[Any, Any]) -> None:
    """Sends single event to consumer"""
    header = {"Accept": "application/json", "my-api-key": "secret"}

    event_to_send = [event]
    async with httpx.AsyncClient() as client:
        try:

            response = await client.post(
                headers=header, url=settings.CONSUMER_ENDPOINT, json=event_to_send
            )

            if response.status_code in [200, 202]:
                logger.info(
                    f"{response.status_code} Event sent: {event}. Response: {response.content}"
                )

            elif response.status_code in [422]:
                logger.error(
                    f"{response.status_code} Event sent: {event}. Response: {response.content} "
                )

            else:
                logger.error(
                    f"{response.status_code} While sending event to consumer. Event sent: {event}. Response: {response.content} "
                )

        except Exception as e:
            logger.error(
                f"Unexpected exception while sending event to consumer. Event: {event}. Error: {str(e)}"
            )


async def main() -> None:
    """Propagator main function. Reads events and send one by one to consumer."""

    logger.info("Progator started")

    events = read_tasks_json(events_file_path=settings.EVENTS_FILE)

    try:
        while True:
            event = random.choice(events)

            # put in internal queue and go straight to sleep
            asyncio.create_task(send_event(event))

            await asyncio.sleep(settings.PERIOD_SECONDS)

    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Stoped by ctrl+c")


if __name__ == "__main__":
    asyncio.run(main())

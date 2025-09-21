import json
from pathlib import Path

import aiofiles
import pytest
import pytest_asyncio

from consumer.configuration.config import settings
from consumer.schemas import Event
from consumer.services import save_to_events

TEST_FILE = Path("test_events.log")


@pytest_asyncio.fixture
async def setup_file():
    """Deletes the test file, test creates new, deletes file after test"""
    if TEST_FILE.exists():
        TEST_FILE.unlink()
    yield
    if TEST_FILE.exists():
        TEST_FILE.unlink()


@pytest.mark.asyncio
async def test_save_to_events(setup_file, monkeypatch):
    """Test if events are saves properly to log file"""
    # swap STORAGE file to test file
    monkeypatch.setattr(settings, "STORAGE_FILE", TEST_FILE)

    events = [
        Event(event_type="aaa", event_payload="bbb"),
        Event(event_type="ccc", event_payload="ddd"),
    ]

    # add events
    status, message = await save_to_events(events, storage_type="file")

    assert status is True
    assert message == "Events saved to a file"

    # check if events added ok
    async with aiofiles.open(TEST_FILE, "r", encoding="utf-8") as f:
        lines = await f.readlines()

    event_entries_from_lines = [json.loads(line) for line in lines]

    assert event_entries_from_lines[0]["event_type"] == "aaa"
    assert event_entries_from_lines[0]["event_payload"] == "bbb"
    assert event_entries_from_lines[1]["event_type"] == "ccc"
    assert event_entries_from_lines[1]["event_payload"] == "ddd"

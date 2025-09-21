from pydantic import BaseModel


class Event(BaseModel):
    event_type: str
    event_payload: str

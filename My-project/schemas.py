from pydantic import BaseModel
from datetime import datetime
from typing import List


class MessageSchema(BaseModel):
    id: int
    channel_name: str
    message_text: str
    posted_at: datetime

    class Config:
        orm_mode = True

class TopProductSchema(BaseModel):
    product_name: str
    count: int

class ChannelActivitySchema(BaseModel):
    date: str
    count: int

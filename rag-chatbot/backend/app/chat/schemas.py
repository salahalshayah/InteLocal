# app/schemas.py

import uuid

from pydantic import BaseModel


class ChatMessage(BaseModel):
    content: str

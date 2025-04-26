from pydantic import BaseModel
from datetime import datetime
from src.shared.enums.chat_type import ChatType

class Chat(BaseModel):
    type: ChatType
    message: str
    created_at: datetime

from pydantic import BaseModel
from src.shared.enums.chat_type import ChatType

class ChatViewModel(BaseModel):
    type: ChatType
    message: str
    created_at: str
    session_id: str
from datetime import datetime
import pytz
from src.shared.entities.Chat import Chat
from src.modules.chat.chat_repository import ChatRepository
from src.modules.chat.chat_viewmodel import ChatViewModel

class ChatUseCase:
    def __init__(self, repo: ChatRepository):
        self.repo = repo

    def __call__(self, data: dict):
        try:

            human_message = Chat(
                type="HUMAN",
                message=data.get("message", "Olá"),
                created_at=datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()
            )

            repo_chat = self.repo.chat(human_message.message)

            viewmodel = ChatViewModel(type="AI", message=repo_chat,created_at=datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat())

            return viewmodel.dict()
        except Exception as e:
            raise Exception(f"Erro ao processar o ChatUseCase: {str(e)}")

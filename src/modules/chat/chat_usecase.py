from src.modules.chat.chat_repository import ChatRepository
from src.modules.chat.chat_viewmodel import ChatViewModel

class ChatUseCase:
    def __init__(self, repo: ChatRepository):
        self.repo = repo

    def __call__(self):
        try:
            viewmodel = ChatViewModel()
            return viewmodel.dict()
        except Exception as e:
            raise e
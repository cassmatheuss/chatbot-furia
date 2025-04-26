from src.modules.history.history_repository import HistoryRepository
from src.modules.history.history_viewmodel import HistoryViewModel


class HistoryUseCase:
    def __init__(self, repo: HistoryRepository):
        self.repo = repo

    def __call__(self, data: dict):
        try:
            session_id = data.get("session_id")
            if not session_id:
                raise ValueError("O campo 'session_id' é obrigatório.")

            messages = self.repo.get_messages_by_session_id(session_id)

            viewmodel = HistoryViewModel(history=messages)

            return viewmodel.dict()
        except Exception as e:
            raise Exception(f"Erro ao processar o HistoryUseCase: {str(e)}")
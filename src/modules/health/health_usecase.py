from src.modules.health.health_repository import HealthRepository
from src.modules.health.health_viewmodel import HealthViewModel

class HealthUseCase:
    def __init__(self, repo: HealthRepository):
        self.repo = repo

    def __call__(self):
        try:
            status_message = "Funcionando! Bem-Vindo Furioso! 🐯🚀"
            check = self.repo.app_check()
            viewmodel = HealthViewModel(status=status_message if check else "O serviço não está disponível!")
            return viewmodel.dict()
        except Exception as e:
            raise e
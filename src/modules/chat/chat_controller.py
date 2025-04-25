from flask import Blueprint
from src.modules.chat.chat_repository import ChatRepository
from src.modules.chat.chat_usecase import ChatUseCase


chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['POST'])
def chat():
    repository = ChatRepository()
    usecase = ChatUseCase(repository)
    result = usecase()
    
    status_code = 200 if result['status'] else 503
    return result, status_code

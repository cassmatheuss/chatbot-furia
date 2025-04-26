from flask import Blueprint, request
from src.modules.chat.chat_repository import ChatRepository
from src.modules.chat.chat_usecase import ChatUseCase


chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    repository = ChatRepository()
    usecase = ChatUseCase(repository)
    result = usecase(data)
    
    status_code = 200 if result else 500
    return result, status_code

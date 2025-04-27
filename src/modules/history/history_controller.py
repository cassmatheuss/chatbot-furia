from flask import Blueprint, jsonify

from src.modules.history.history_repository import HistoryRepository
from src.modules.history.history_usecase import HistoryUseCase

history_bp = Blueprint('history', __name__)

@history_bp.route('/history/<session_id>', methods=['GET'])
def get_history(session_id):
    try:
        repository = HistoryRepository()
        usecase = HistoryUseCase(repository)
        result = usecase({"session_id": session_id})
        
        status_code = 200 if result else 404
        return result, status_code
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
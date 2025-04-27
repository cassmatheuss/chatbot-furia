from flask import Blueprint, jsonify
from src.modules.health.health_repository import HealthRepository
from src.modules.health.health_usecase import HealthUseCase

health_bp = Blueprint('health', __name__)

@health_bp.route('/', methods=['GET'])
def health_check():
    repository = HealthRepository()
    usecase = HealthUseCase(repository)
    result = usecase()
    
    status_code = 200 if result['status'] else 503
    return result, status_code

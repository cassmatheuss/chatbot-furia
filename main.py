from flask import Flask
from src.modules.health.health_controller import health_bp
from src.shared.infra.environments import Environments
from src.modules.chat.chat_controller import chat_bp

app = Flask(__name__)

# health check
app.register_blueprint(health_bp)

#chat
app.register_blueprint(chat_bp)

if __name__ == '__main__':
    Environments()
    app.run(debug=True)

from flask import Flask
from src.modules.health.health_controller import health_bp

app = Flask(__name__)

# health check
app.register_blueprint(health_bp)

if __name__ == '__main__':
    app.run(debug=True)

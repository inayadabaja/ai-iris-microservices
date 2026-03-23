from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev_secret_key")

    default_db_uri = (
        f"postgresql://{os.getenv('APP_POSTGRES_USER', 'postgres')}:"
        f"{os.getenv('APP_POSTGRES_PASSWORD', 'postgres')}@"
        f"{os.getenv('APP_POSTGRES_HOST', 'localhost')}:"
        f"{os.getenv('APP_POSTGRES_PORT', '5432')}/"
        f"{os.getenv('APP_POSTGRES_DB', 'app_db')}"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = default_db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PREDICTION_API_URL"] = os.getenv("PREDICTION_API_URL", "http://localhost:8004")

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from app.models.user_model import User
    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.prediction_routes import prediction_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(prediction_bp)

    with app.app_context():
        db.create_all()

    return app
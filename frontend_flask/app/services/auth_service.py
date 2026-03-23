from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user_model import User


class AuthService:
    def signup(self, username: str, email: str, password: str):
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            raise ValueError("Nom d'utilisateur ou email déjà utilisé")

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()
        return user

    def login(self, username: str, password: str):
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            raise ValueError("Identifiants invalides")

        return user
from ..models import User


class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: str):
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user_id: str, username: str, email: str, hashed_password: str, role: str):
        user = User(
            id=user_id,
            email=email,
            username=username,
            hashed_password=hashed_password,
            role=role,
        )
        self.db.add(user)
        self.db.flush()
        self.db.commit()
        self.db.refresh(user)
        return user

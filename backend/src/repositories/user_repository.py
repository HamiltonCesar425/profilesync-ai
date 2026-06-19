from sqlalchemy.orm import Session

from models.user_model import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(
        self,
        email: str,
        hashed_password: str,
    ) -> User:
        user = User(
            email=email,
            hashed_password=hashed_password,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user


def get_by_email(self, email: str) -> User | None:
    return self.db.query(User).filter(User.email == email).first()

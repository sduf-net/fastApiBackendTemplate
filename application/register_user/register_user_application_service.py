from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.user.user import User
from shared.transaction_manager import TransactionManager


class UserRegistrationData(BaseModel):
    email: str


def execute(params: UserRegistrationData, db: Session):
    """
    Creates a new user in the database with a transaction.
    """
    transaction_manager = TransactionManager(db)

    with transaction_manager.transaction() as session:
        # Create a new user object and add it to the session
        new_user = User(email=params.email, password=params.password)
        session.add(new_user)

    return new_user

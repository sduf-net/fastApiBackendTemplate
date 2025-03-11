import uuid
from sqlalchemy.orm import Session
from facade import register_user
from models.user.user import User
import pytest

def test_execute_creates_user(db_session: Session):
    """
    Test that the execute function creates a new user in the database.
    """
    email=f"{str(uuid.uuid4())}@test.com"
    password=str(uuid.uuid4())
    new_user = register_user(email, password, db_session)

    # Assert that the correct user object was created
    assert new_user.email == email
    assert isinstance(new_user, User)

def test_execute_user_already_registered(db_session: Session):
    """
    Test that trying to register a user with an already existing email raises an error.
    """
    # Create a new user first
    email = f"{str(uuid.uuid4())}@test.com"
    password = str(uuid.uuid4())
    register_user(email, password, db_session)  # First registration

    # Assert that it raises a ValueError when user is already registered
    with pytest.raises(ValueError, match="User already registered"):
        register_user(email, password, db_session)

from sqlalchemy.orm import Session
from models.user.user import User
from repositories.user_repository.user_repository import UserRepository

def test_sign_in_success(client, db_session: Session, mock_requests_post):
    user = User("testuser1@example.com", "Password123!")
    db_session.add(user)
    db_session.commit()

    valid_sign_in_payload = {
        "user_id": "user-uuid",
        "action": "user-uuid",
        "project_id": "project-uuid",
        "screen_id": "screen-uuid",
        "payload": {
            "data": {
                "email": "testuser1@example.com",
                "password": "Password123!"
            }
        }
    }
    response = client.post("/auth/sign_in", json=valid_sign_in_payload)
    mock_requests_post.assert_called_once()
    assert response.status_code == 204

    user = UserRepository.get_by_email(db_session, "testuser1@example.com")
    # assert user.id is not None
    # assert user.email =="testuser1@example.com"


def test_sign_in_missing_fields(client, mock_requests_post):
    invalid_sign_in_payload = {
        "user_id": "user-uuid",
        "action": "user-uuid",
        "project_id": "project-uuid",
        "screen_id": "screen-uuid",
        "payload": {
            "data": {}
        }
    }
    response = client.post("auth/sign_in", json=invalid_sign_in_payload)
    assert response.status_code == 200
    assert response.json() == {
        'error_message': 'Missing required fields (email, password)'}
    mock_requests_post.assert_called()


def test_sign_in_invalid_email(client, mock_requests_post):
    invalid_sign_in_payload = {
        "user_id": "user-uuid",
        "action": "user-uuid",
        "project_id": "project-uuid",
        "screen_id": "screen-uuid",
        "payload": {
            "data": {
                "email": "invalidemail",
                "password": "Password123!"
            }
        }
    }
    response = client.post("/auth/sign_in", json=invalid_sign_in_payload)
    assert response.status_code == 200
    assert response.json() == {'error_message': 'Invalid email format'}
    mock_requests_post.assert_called()


def test_sign_in_incorrect_password(client, mock_requests_post):
    invalid_sign_in_payload = {
        "user_id": "user-uuid",
        "action": "user-uuid",
        "project_id": "project-uuid",
        "screen_id": "screen-uuid",
        "payload": {
            "data": {
                "email": "testuser1@example.com",
                "password": "IncorrectPassword"
            }
        }
    }
    response = client.post("/auth/sign_in", json=invalid_sign_in_payload)
    assert response.status_code == 200
    assert response.json() == {'error_message': 'Incorrect email or password'}
    mock_requests_post.assert_called()


def test_sign_up_success(client, mock_requests_post):
    valid_sign_up_payload = {
        "user_id": "user-uuid",
        "action": "user-uuid",
        "project_id": "project-uuid",
        "screen_id": "screen-uuid",
        "payload": {
            "data": {
                "email": "newuser@example.com",
                "password": "Password123!",
                "password_confirm": "Password123!"
            }
        }
    }
    response = client.post("/auth/sign_up", json=valid_sign_up_payload)
    assert response.status_code == 204
    mock_requests_post.assert_called()


def test_sign_up_mismatched_passwords(client, mock_requests_post):
    invalid_sign_up_payload = {
        "user_id": "user-uuid",
        "action": "user-uuid",
        "project_id": "project-uuid",
        "screen_id": "screen-uuid",
        "payload": {
            "data": {
                "email": "newuser@example.com",
                "password": "Password123!",
                "password_confirm": "DifferentPassword"
            }
        }
    }
    response = client.post("/auth/sign_up", json=invalid_sign_up_payload)
    assert response.status_code == 200
    assert response.json() == {'error_message': 'Passwords do not match'}
    mock_requests_post.assert_called()


def test_sign_up_missing_fields(client, mock_requests_post):
    invalid_sign_up_payload = {
        "user_id": "user-uuid",
        "action": "user-uuid",
        "project_id": "project-uuid",
        "screen_id": "screen-uuid",
        "payload": {
            "data": {}
        }
    }
    response = client.post("/auth/sign_up", json=invalid_sign_up_payload)
    assert response.status_code == 200
    assert response.json() == {
        'error_message': 'Missing required fields (email, password)'}
    mock_requests_post.assert_called()


def test_sign_up_user_exists(client, mock_requests_post):
    invalid_sign_up_payload = {
        "user_id": "user-uuid",
        "action": "user-uuid",
        "project_id": "project-uuid",
        "screen_id": "screen-uuid",
        "payload": {
            "data": {
                "email": "testuser1@example.com",
                "password": "Password123!",
                "password_confirm": "Password123!"
            }
        }
    }
    response = client.post("/auth/sign_up", json=invalid_sign_up_payload)
    assert response.status_code == 200
    assert response.json() == {'error_message': 'User already registered'}
    mock_requests_post.assert_called()

import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response
from database import get_db
from repositories.user_repository.user_repository import UserRepository
from facade import register_user
from shared.token import Token
from sduf.sduf_request import SdufEvent, SdufRequest
from sduf.api_client import send_event

router = APIRouter()


@router.post("/sign_in")
async def sign_in(params: SdufRequest, db: Session = Depends(get_db)):
    try:
        if 'data' not in params.payload:
            raise ValueError("Missing required fields (email, password)")

        data = params.payload['data']
        # Validate that email and password are present
        if not data or 'email' not in data or 'password' not in data:
            raise ValueError("Missing required fields (email, password)")

        if '@' not in data['email'] and '.' not in data['email']:
            raise ValueError("Invalid email format")

        # Authenticate user
        user = UserRepository.get_by_email(db, data['email'])
        if user and user.check_password(data['password']):
            # Generate a token for the user if authentication is successful
            token = Token.generate_and_sign(user_id=str(user.id))

            event = SdufEvent(
                event_id=str(uuid.uuid4()),
                user_id=params.user_id,
                project_id=params.project_id,
                screen_id=params.screen_id,
                action="login",
                payload={"id": user.id, "token": token}
            )
            send_event(event)
            return Response(status_code=204)
        raise ValueError("Incorrect email or password")
    except Exception as e:
        error_message = str(e)
        # If authentication fails, send an error message
        event = SdufEvent(
            event_id=str(uuid.uuid4()),
            user_id=params.user_id,
            project_id=params.project_id,
            screen_id=params.screen_id,
            action="show_error_message",
            payload={"error_message": error_message}
        )
        send_event(event)
        return {"error_message": error_message}


@router.post("/sign_up")
async def sign_up(params: SdufRequest, db: Session = Depends(get_db)):
    try:
        if 'data' not in params.payload:
            raise ValueError("Missing required fields (email, password)")

        data = params.payload['data']
        # Validate that email and password are present
        if not data or 'email' not in data or 'password' not in data:
            raise ValueError("Missing required fields (email, password)")

        if '@' not in data['email'] and '.' not in data['email']:
            raise ValueError("Invalid email format")

        # Check if passwords match
        if data['password'] != data['password_confirm']:
            raise ValueError("Passwords do not match")

        user = register_user(email=data['email'], password=data['password'], db=db)
        token = Token.generate_and_sign(user_id=str(user.id))
        # Send login success event
        event = SdufEvent(
            event_id=str(uuid.uuid4()),
            user_id=params.user_id,
            project_id=params.project_id,
            screen_id=params.screen_id,
            action="login",
            payload={"id": user.id, "token": token}
        )
        send_event(event)

        # Send close popup event
        event = SdufEvent(
            event_id=str(uuid.uuid4()),
            user_id=params.user_id,
            project_id=params.project_id,
            screen_id=params.screen_id,
            action="close_popup",
            payload={}
        )
        send_event(event)

        return Response(status_code=204)
    except ValueError as e:
        error_message = str(e)
        # If authentication fails, send an error message
        event = SdufEvent(
            event_id=str(uuid.uuid4()),
            user_id=params.user_id,
            project_id=params.project_id,
            screen_id=params.screen_id,
            action="show_error_message",
            payload={"error_message": error_message}
        )
        send_event(event)
        return {"error_message": error_message}

import uuid
from sduf.api_client import send_event
from sduf.sduf_request import SdufEvent


def test_sign_in_success(mock_requests_post):
    event = SdufEvent(
        event_id=str(uuid.uuid4()),
        user_id=str(uuid.uuid4()),
        project_id=str(uuid.uuid4()),
        screen_id=str(uuid.uuid4()),
        action="show_error_message",
        payload={}
    )
    send_event(event)
    mock_requests_post.assert_called_once()

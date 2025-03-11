import requests
from config import get_settings
from sduf.sduf_request import SdufEvent

BASE_URL = get_settings().SDUF_BASE_URL
PROJECT_TOKEN = get_settings().SDUF_PROJECT_API_TOKEN

def send_event(body: SdufEvent):
    headers = {
        "Content-Type": "application/json",
        "x-api-token": PROJECT_TOKEN
    }
    response = requests.post(f"{BASE_URL}/api/v1/push/event", json=body.model_dump(), headers=headers, timeout=60000)
    response.raise_for_status()
    return response

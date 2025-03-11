from pydantic import BaseModel
from typing import Any, Optional, Union

class SdufRequest(BaseModel):
    payload: Any
    user_id: str
    action: str
    user_token: Optional[str] = None
    screen_id: Union[str, int]
    project_id: str

class SdufEvent(BaseModel):
    payload: Any
    event_id: str
    user_id: str
    project_id: str
    screen_id: Union[str, int]
    action: str
from pydantic import BaseModel
from typing import Optional, Union, List

class ChatInput(BaseModel):
    message: Optional[str] = None
    image: Optional[Union[str, bytes]] = None
    audio: Optional[str] = None
    document: Optional[str] = None
    is_url: bool = False

class Message(BaseModel):
    role: str
    content: Union[str, List[dict]]

class ChatResponse(BaseModel):
    response: str
    error: Optional[str] = None

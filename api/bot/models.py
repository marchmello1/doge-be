from pydantic import BaseModel, Field
from typing import Optional, Union, List

class ImageURL(BaseModel):
    url: str
    detail: str = "high"

class MessageContent(BaseModel):
    type: str
    text: Optional[str] = None
    image_url: Optional[ImageURL] = None

class Message(BaseModel):
    role: str
    content: Union[str, List[MessageContent]]

class ChatRequest(BaseModel):
    message: str
    image: Optional[Union[str, bytes]] = None
    is_url: bool = False

class ChatResponse(BaseModel):
    response: str
    error: Optional[str] = None

class BotConfig(BaseModel):
    api_key: str
    api_base: str = "https://api.x.ai/v1"
    temperature: float = Field(default=0.7, ge=0, le=2)
    model: str = "grok-vision-beta"

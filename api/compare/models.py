from pydantic import BaseModel
from typing import List, Optional, Union

class BaseItem(BaseModel):
    title: str
    description: str
    state_reference: str
    impact: str
    source_link: Optional[str] = None

class Response(BaseModel):
    data: List[BaseItem]

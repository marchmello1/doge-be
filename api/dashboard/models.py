from pydantic import BaseModel
from typing import List, Optional, Union

class GeneralItem(BaseModel):
    title: str
    description: str

class Response(BaseModel):
    data: Union[GeneralItem, List[GeneralItem]]

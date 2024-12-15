from pydantic import BaseModel
from typing import List, Optional, Union

class GeneralItem(BaseModel):
    summary: str

class Response(BaseModel):
    data: Union[GeneralItem, List[GeneralItem]]

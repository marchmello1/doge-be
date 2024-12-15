from pydantic import BaseModel
from typing import List, Optional

class GeneralComparisonItem(BaseModel):
    title: str
    description: str

class GeneralComparisonResponse(BaseModel):
    data: List[GeneralComparisonItem]

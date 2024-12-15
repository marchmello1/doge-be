from pydantic import BaseModel
from typing import List, Optional, Union


class BaseItem(BaseModel):
    title: str
    description: str
    state_reference: str
    impact: str
    source_link: Optional[str] = None


class LawItem(BaseItem):
    pass

class LawData(BaseModel):
    law_difference_data: List[LawItem]

class TaxItem(BaseItem):
    pass

class TaxData(BaseModel):
    tax_difference_data: List[TaxItem]

class EducationItem(BaseItem):
    pass

class EducationData(BaseModel):
    education_difference_data: List[EducationItem]

class EmergencyServiceItem(BaseItem):
    pass

class EmergencyServiceData(BaseModel):
    emergency_service_difference_data: List[EmergencyServiceItem]

class PropertyItem(BaseItem):
    pass

class PropertyData(BaseModel):
    property_difference_data: List[PropertyItem]

class Response(BaseModel):
    data: Union[LawData, TaxData, EducationData, EmergencyServiceData, PropertyData]
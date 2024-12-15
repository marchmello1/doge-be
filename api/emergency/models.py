# models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class ContactInfo(BaseModel):
    phone: str = Field(..., description="Emergency contact number")
    address: Optional[str] = Field(None, description="Physical address if applicable")
    hours: str = Field(..., description="Operating hours (e.g., 24/7)")

class EmergencyService(BaseModel):
    title: str = Field(..., description="Name of the emergency service")
    type: str = Field(..., description="Type of emergency (e.g., General Emergency, Medical, Fire, Police)")
    description: str = Field(..., description="Brief description of the service and its primary purpose")
    contact: ContactInfo
    service_level: Optional[str] = Field(None, description="Description of service level (e.g., Level 1 Trauma Center)")
    coverage_area: str = Field(..., description="Areas covered by this service")
    response_time: Optional[str] = Field(None, description="Average response time if available")
    special_services: Optional[str] = Field(None, description="Any specialized services offered")
    state_specific_info: Optional[str] = Field(None, description="State-specific emergency service information")
    source_link: Optional[str] = Field(None, description="URL to the official emergency service website")

class EmergencyServiceResponse(BaseModel):
    status: str = Field(..., description="Status of the API response")
    data: List[EmergencyService] = Field(..., description="List of emergency services")
    message: Optional[str] = Field(None, description="Error message if applicable")

class EmergencyComparison(BaseModel):
    source_state: str
    target_state: str
    differences: List[dict] = Field(..., description="List of key differences in emergency services")
    recommendations: List[str] = Field(..., description="Recommendations for new residents")
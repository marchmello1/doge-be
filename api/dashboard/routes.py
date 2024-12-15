from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.responses import JSONResponse
from api.dashboard.methods import get_general_info
from env import env
import logging

router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"],
    responses={404: {"description": "Not found"}},
)

class ComparisonRequest(BaseModel):
    source_state: str = Field(..., description="Name of the source state")
    target_state: str = Field(..., description="Name of the target state")

class LawComparison(BaseModel):
    title: str = Field(..., description="Title of the law comparison")
    description: str = Field(..., description="Description of the differences")

class ComparisonResponse(BaseModel):
    data: List[LawComparison] = Field(..., description="List of law comparisons")
    status: str = Field(default="success", description="Status of the response")

@router.post("/", response_model=ComparisonResponse)
async def dashboard_endpoint(request: ComparisonRequest):
    """
    Compare different aspects between two states.
    
    Returns a comparison of laws and regulations between the states.
    """
    try:
        result = get_general_info(request.source_state, request.target_state, env.XAI_KEY)
        
        if isinstance(result, dict) and result.get("status") == "error":
            raise HTTPException(
                status_code=400,
                detail=result["message"]
            )
            
        # Transform the data to match the expected format
        if isinstance(result, dict) and "data" in result:
            formatted_data = result["data"]
        else:
            # If the data isn't properly structured, format it
            formatted_data = [
                LawComparison(
                    title=item.get("title", "Unknown"),
                    description=item.get("description", "No description available")
                )
                for item in (result if isinstance(result, list) else [])
            ]
        
        return ComparisonResponse(
            data=formatted_data,
            status="success"
        )
        
    except Exception as e:
        logging.error(f"Error in dashboard endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
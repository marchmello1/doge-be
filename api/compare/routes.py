from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Optional
from fastapi.responses import JSONResponse
from api.compare.methods import compare_states  # Assuming the compare_states function is in compare.py
from api.compare.models import Response
from env import env
import logging

router = APIRouter(
    prefix="/api/v1/states",
    tags=["state-comparison"],
    responses={404: {"description": "Not found"}},
)

class ComparisonRequest(BaseModel):
    source_state: str = Field(..., description="Name of the source state")
    target_state: str = Field(..., description="Name of the target state")
    comparison_type: Literal["laws", "taxes", "education", "emergency_services", "property"] = Field(
        ..., 
        description="Type of comparison to perform"
    )

@router.post("/compare", response_model=Response)
async def compare_states_endpoint(request: ComparisonRequest):
    """
    Compare different aspects between two states.
    
    Returns a comparison based on the specified type (laws, taxes, education, emergency_services, property)
    """
    try:
        result = compare_states(
            source_state=request.source_state,
            target_state=request.target_state,
            comparison_type=request.comparison_type,
            api_key=env.XAI_KEY
        )

        logging.info(request)
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=400,
                detail={
                    "message": result["message"],
                    "raw_response": result.get("raw_response")
                }
            )
        logging.info(result["data"])
        return result["data"]
        
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Internal server error: {str(e)}"
            }
        )
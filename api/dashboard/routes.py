from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Optional
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


@router.post("/")
async def dashboard_endpoint(request: ComparisonRequest):
    """
    Compare different aspects between two states.
    
    Returns a comparison based on the specified type (laws, taxes, education, emergency_services, property)
    """
    try:
        result = get_general_info(request.source_state, request.target_state, env.XAI_KEY)

        logging.info(request)
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=400,
                detail={
                    "message": result["message"],

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
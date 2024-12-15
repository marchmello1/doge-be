from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Union, Optional
from fastapi.responses import JSONResponse, PlainTextResponse
from api.bot.methods import RelocationBot
from env import env
import logging

router = APIRouter(
    prefix="/api/v1/bot",
    tags=["Bot"],
    responses={404: {"description": "Not found"}},
)

class BotRequest(BaseModel):
    message : str
    image: Optional[Union[str, bytes]] = None
    audio: Optional[str] = None
    document: Optional[str] = None
    is_url: bool = False


@router.post("/")
async def bot_endpoint(request: BotRequest):
    """
    Compare different aspects between two states.
    
    Returns a comparison based on the specified type (laws, taxes, education, emergency_services, property)
    """
    try:
        bot = RelocationBot(api_key=env.XAI_KEY)
        result = bot.chat(message=request.message)
        return PlainTextResponse(content=result)
        
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Internal server error: {str(e)}"
            }
        )
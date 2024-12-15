# routes.py
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Optional
from langchain_openai import OpenAI
import logging
import os
import json
from .models import EmergencyServiceResponse, EmergencyComparison
from .prompts import get_emergency_services_prompt, get_emergency_comparison_prompt
from env import env

router = APIRouter(prefix="/api/v1/emergency", tags=["emergency"])

def get_llm(api_key: str, api_base: str = "https://api.x.ai/v1"):
    """Initialize LLM with given credentials"""
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_API_BASE"] = api_base
    
    return OpenAI(
        model="grok-2-1212",
        max_tokens=50000,
        temperature=0.3,
    )


@router.get("/services/{state}", response_model=EmergencyServiceResponse)
async def get_emergency_services(
    state: str
):
    """
    Get emergency services information for a specific state
    
    Args:
        state: Name of the state
    """
    try:
        api_key=env.XAI_KEY

        llm = get_llm(api_key)
        
        prompt = get_emergency_services_prompt(state)
        response = llm(prompt)
        
        # Clean and parse response
        clean_response = response.strip().replace('\n', ' ').replace('\r', '')
        data = json.loads(clean_response)
        
        logging.info(data)

        return data
        
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching emergency services: {str(e)}"
        )


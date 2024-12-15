from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
import os
import json
from typing import Dict
from api.dashboard.models import GeneralComparisonResponse
from api.dashboard.prompts import get_general_prompt
from env import env

def get_general_info(source_state: str, target_state: str, api_key: str) -> Dict:
    """
    Get general information about different aspects between states
    
    Args:
        source_state (str): Name of the source state
        target_state (str): Name of the target state
        api_key (str): API key for authentication
        
    Returns:
        Dict: General information or error information
    """
    
    if not source_state or not target_state:
        return {
            "status": "error",
            "message": "Source state and target state are required"
        }
    
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_API_BASE"] = "https://api.x.ai/v1"
    
    try:
        llm = OpenAI(
            model_name="grok-2-1212",
            max_tokens=2048,
            temperature=0.3,
        )
        
       
        prompt = PromptTemplate(
            template=get_general_prompt(source_state, target_state),
            input_variables=["dummy"]
        )
        
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        
        
        output = llm_chain.run(dummy="")
        
        
        clean_output = output.strip().replace('\n', ' ').replace('\r', '').replace('<|eos|>', '')
        
        
        start_idx = clean_output.find('{')
        end_idx = clean_output.rfind('}') + 1
        
        if start_idx == -1 or end_idx <= start_idx:
            raise ValueError("Invalid JSON response format")
            
        json_str = clean_output[start_idx:end_idx]
        parsed_json = json.loads(json_str)
        
       
        validated_data = GeneralComparisonResponse.parse_obj(parsed_json)
        
        return {
            "status": "success",
            "data": validated_data.dict()["data"]
        }
        
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "message": f"Failed to parse JSON response: {str(e)}"
        }
    except ValueError as e:
        return {
            "status": "error",
            "message": str(e)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }

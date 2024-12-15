from langchain_openai import OpenAI
import os
import json
from typing import Dict
from api.compare.models import Response
from api.compare.prompts import get_comparison_prompts
from env import env

def compare_states(
    source_state: str, 
    target_state: str, 
    comparison_type: str,
    api_key: str,
    api_base: str = "https://api.x.ai/v1"
) -> Dict:
    """
    Compare different aspects between states
    
    Args:
        source_state (str): Name of the source state
        target_state (str): Name of the target state
        comparison_type (str): Type of comparison (laws, taxes, education, emergency_services, property)
        api_key (str): API key for authentication
        api_base (str, optional): Base URL for the API. Defaults to "https://api.x.ai/v1"
        
    Returns:
        Dict: Comparison results or error information
    """
    
    
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_API_BASE"] = api_base

    llm = OpenAI(
        model="grok-2-1212",
        max_tokens=50000,
        temperature=0.3,
    )

    def generate_with_retry(prompt: str, max_retries: int = 3) -> Dict:
        """Helper function to generate response with retries"""
        for attempt in range(max_retries):
            try:
               
                output = llm(prompt)
                
               
                if not output or output.strip() == "<|eos|>":
                    simplified_prompt = (
                        f"Generate a detailed comparison of {comparison_type} between "
                        f"{source_state} and {target_state} as a JSON object. "
                        f"Use this exact format:\n{prompt}"
                    )
                    output = llm(simplified_prompt)
                
                
                if not output or output.strip() == "<|eos|>":
                    basic_prompt = (
                        f"Compare {comparison_type} between {source_state} and {target_state}. "
                        f"Return only a JSON object using this structure:\n{prompt}"
                    )
                    output = llm(basic_prompt)
                
                
                clean_output = output.strip().replace('\n', ' ').replace('\r', '').replace('<|eos|>', '')
                
                if clean_output:
                    start_idx = clean_output.find('{')
                    end_idx = clean_output.rfind('}') + 1
                    
                    if start_idx != -1 and end_idx > start_idx:
                        json_str = clean_output[start_idx:end_idx]
                        try:
                            parsed_json = json.loads(json_str)
                            validated_data = parsed_json
                            return {
                                "status": "success",
                                "data": json.loads(validated_data.model_dump_json())
                            }
                        except (json.JSONDecodeError, ValueError) as e:
                            if attempt == max_retries - 1:
                                return {
                                    "status": "error",
                                    "message": f"JSON validation error: {str(e)}",
                                    "raw_response": json_str
                                }
                            continue
                
                if attempt < max_retries - 1:
                    continue
                else:
                    return {
                        "status": "error",
                        "message": "No valid response after retries",
                        "raw_response": output
                    }
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                else:
                    return {
                        "status": "error",
                        "message": str(e),
                        "raw_response": output if 'output' in locals() else None
                    }
        
        return {
            "status": "error",
            "message": "Max retries reached",
            "raw_response": None
        }

   
    prompts = get_comparison_prompts(source_state, target_state)
    if comparison_type not in prompts:
        return {
            "status": "error",
            "message": f"Invalid comparison type: {comparison_type}"
        }

    return generate_with_retry(prompts[comparison_type])


# res=compare_states(source_state="California", target_state="Georgia", comparison_type="laws", api_key=env.XAI_KEY)

# print(res)
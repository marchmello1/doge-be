from langchain import OpenAI
import os
import json
from typing import Dict

def get_general_info(source_state: str, target_state: str, api_key: str) -> Dict:
    """
    Get general information comparing aspects between states
    """
    if not source_state or not target_state:
        return {"status": "error", "message": "States required"}
    
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_API_BASE"] = "https://api.x.ai/v1"
    
    try:
        llm = OpenAI(
            model_name="grok-2-1212",
            max_tokens=2048,
            temperature=0.3,
        )

        prompt = f"""You are a helpful assistant that provides state comparisons in JSON format.

        Task: Compare {source_state} and {target_state}.

        Instructions:
        1. Provide ONLY a valid JSON response
        2. Do not include any additional text or explanations
        3. Follow the exact structure below
        4. Each description should be single sentence with limit of 15 words at max
        5. Ensure all JSON syntax is correct

        Required JSON structure:
        {{
            "data": [
                {{
                    "title": "Tax Rates",
                    "description": "Compare overall tax burden including state income tax, sales tax, and property tax rates."
                }},
                {{
                    "title": "Vehicle Registration",
                    "description": "Compare vehicle registration processes, fees, and requirements."
                }},
                {{
                    "title": "Employment Laws",
                    "description": "Compare major employment laws including minimum wage and worker protections."
                }},
                {{
                    "title": "Property Laws",
                    "description": "Compare property laws focusing on homestead exemptions and real estate regulations."
                }},
                {{
                    "title": "Education",
                    "description": "Compare K-12 education systems, funding, and performance metrics."
                }}
            ]
        }}"""

        # Get completion
        response = llm.predict(prompt)
        
        # Clean the response
        response = response.strip()
        
        # Find the JSON part
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end != -1:
            response = response[start:end]
        
        # Try to parse the JSON
        try:
            parsed = json.loads(response)
            
            # Validate structure
            if "data" not in parsed:
                return {"status": "error", "message": "Invalid response structure"}
                
            # Basic validation of data items
            for item in parsed["data"]:
                if "title" not in item or "description" not in item:
                    return {"status": "error", "message": "Invalid data item structure"}
            
            return {
                "status": "success",
                "data": parsed["data"]
            }
            
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "message": f"JSON parsing error: {str(e)}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}"
        }
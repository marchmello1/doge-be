from langchain import OpenAI
import os
import json
from typing import Dict
from env import env

def get_general_info(state:str):
    """
    Get general information comparing aspects between states
    """
    if not state:
        return {"status": "error", "message": "States required"}
    
    os.environ["OPENAI_API_KEY"] = env.XAI_KEY
    os.environ["OPENAI_API_BASE"] = "https://api.x.ai/v1"
    
    try:
        llm = OpenAI(
            model_name="grok-2-1212",
            max_tokens=2048,
            temperature=0.3,
        )

        prompt = f"""Return only a JSON object containing emergency services information for {state}. Format:
     
     Instructions:
        1. Provide ONLY a valid JSON response
        2. Do not include any additional text or explanations
        3. Follow the exact structure below
        4. Ensure all JSON syntax is correct
   
   {{
  "status": "success",
  "data": [
    {{
      "title": "Name of the emergency service",
      "type": "Type of emergency (e.g., General Emergency, Medical, Fire, Police)",
      "description": "Brief description of the service and its primary purpose",
      "contact": {{
        "phone": "Emergency contact number",
        "address": "Physical address if applicable",
        "hours": "Operating hours (e.g., 24/7)"
      }},
      "service_level": "Description of service level (e.g., Level 1 Trauma Center)",
      "coverage_area": "Areas covered by this service",
      "response_time": "Average response time if available",
      "special_services": "Any specialized services offered",
      "state_specific_info": "State-specific emergency service information",
      "source_link": "URL to the official emergency service website"
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
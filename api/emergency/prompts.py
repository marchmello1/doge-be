# prompts.py
from typing import Optional

def get_emergency_services_prompt(state: str) -> str:
    """Generate prompt for fetching emergency services for a specific state"""
    return f"""Return only a JSON object containing emergency services information for {state}. Format:
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


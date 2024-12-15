from typing import Callable, Dict

def get_general_prompt(source_state: str, target_state: str) -> Callable[[], str]:
    """Get a general prompt that compares the states"""
    return lambda: f"""Return a JSON object that compares the following general information between {source_state} and {target_state}:

{{
  "data": [
    {{
      "title": "Tax Rates",
      "description": "provide a sentence on Comparison of the tax rates between the states"
    }},
    {{
      "title": "Vehicle Registration",
      "description": "provide a sentence on Comparison of the vehicle registration process between the states"
    }},
    {{
      "title": "Employment Laws",
      "description": "provide a sentence on Comparison of the employment laws between the states"
    }},
    {{
      "title": "Property Laws",
      "description": "provide a sentence on Comparison of the property laws between the states"
    }},
    {{
      "title": "Education",
      "description": "provide a sentence on Comparison of the education system between the states"
    }}
  ]
}}
"""

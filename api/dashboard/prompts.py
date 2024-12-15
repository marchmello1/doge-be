from typing import Callable, Dict

def get_general_prompt(source_state: str, target_state: str) -> Callable[[], str]:
    """Get a general prompt that compares the states"""
    return lambda: f"""Return a JSON object that compares the following general information between {source_state} and {target_state}:

{{
  "data": [
    {{
      "title": "Tax Rates",
      "description": "Describe how the tax rates differ between {source_state} and {target_state}, including the approximate percentage difference and any key differences in specific tax categories."
    }},
    {{
      "title": "Vehicle Registration",
      "description": "Explain the differences in the vehicle registration process between {source_state} and {target_state}, such as whether registration is annual or biennial, any unique requirements, and the impact on new residents."
    }},
    {{
      "title": "Employment Laws",
      "description": "Compare the employment laws and policies between {source_state} and {target_state}, highlighting any differences in areas like at-will employment, worker protections, and regulations."
    }},
    {{
      "title": "Property Laws",
      "description": "Describe the key differences in property laws and regulations between {source_state} and {target_state}, such as homestead exemptions, property tax rates, and any unique requirements for real estate transactions."
    }},
    {{
      "title": "Education",
      "description": "Contrast the education systems between {source_state} and {target_state}, including differences in school district structures, curriculum standards, funding mechanisms, and any notable policy variations."
    }}
  ]
}}
"""

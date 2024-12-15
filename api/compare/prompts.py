def get_comparison_prompts(source_state: str, target_state: str) -> dict:
    """Get all comparison prompts with formatted state names"""
    
    return {
        "laws": f"""Return only a JSON object comparing laws between {source_state} and {target_state}. Format:
{{
  "data": [
    {{
      "title": "Title of the law",
      "description": "Description of how the law differs in the target state",
      "state_reference": "Reference to the specific state law code or statute",
      "impact": "Brief explanation of how this difference impacts new residents",
      "source_link": "URL to the official state or government source for verification"
    }}
  ]
}}""",

        "taxes": f"""Return only a JSON object comparing taxes between {source_state} and {target_state}. Format:
{{
  "data": [
    {{
      "title": "Title of the tax",
      "description": "Description of how the tax differs in the target state",
      "state_reference": "Reference to the specific state tax code",
      "impact": "Brief explanation of how this difference impacts new residents",
      "source_link": "URL to the official state tax authority source"
    }}
  ]
}}""",

        "education": f"""Return only a JSON object comparing education between {source_state} and {target_state}. Format:
{{
  "data": [
    {{
      "title": "Title of education difference",
      "description": "Description of how education differs in the target state",
      "state_reference": "Reference to specific education code or policy",
      "impact": "Brief explanation of how this difference impacts new residents",
      "source_link": "URL to the official education department source"
    }}
  ]
}}""",

        "emergency_services": f"""Return only a JSON object comparing emergency services between {source_state} and {target_state}. Format:
{{
  "data": [
    {{
      "title": "911 Emergency Response System",
      "description": "Comparison of emergency numbers and response systems between states, including any state-specific protocols",
      "state_reference": "State emergency management agency regulations",
      "impact": "How emergency response differences affect new residents",
      "source_link": "Official state emergency management website"
    }},
    {{
      "title": "Emergency Medical Services",
      "description": "Detailed comparison of ambulance services, paramedic response, and medical emergency protocols",
      "state_reference": "State EMS regulations and standards",
      "impact": "How EMS differences affect emergency medical care access",
      "source_link": "State EMS department website"
    }},
    {{
      "title": "Fire Emergency Services",
      "description": "Comparison of fire department coverage, response times, and specialized services",
      "state_reference": "State fire service regulations",
      "impact": "How fire service differences affect resident safety and response",
      "source_link": "State fire marshal website"
    }},
    {{
      "title": "Emergency Communication Centers",
      "description": "Comparison of dispatch centers, emergency alert systems, and communication protocols",
      "state_reference": "State emergency communication regulations",
      "impact": "How communication differences affect emergency response",
      "source_link": "State emergency communication center website"
    }},
    {{
      "title": "Disaster Response Services",
      "description": "Comparison of natural disaster response systems and emergency management protocols",
      "state_reference": "State disaster response regulations",
      "impact": "How disaster response differences affect emergency preparedness",
      "source_link": "State emergency management website"
    }}
  ]
}}""",

        "property": f"""Return only a JSON object comparing property between {source_state} and {target_state}. Format:
{{
  "data": [
    {{
      "title": "Title of property difference",
      "description": "Description of how property laws or market differs",
      "state_reference": "Reference to specific property codes or regulations",
      "impact": "Brief explanation of how this difference impacts new residents",
      "source_link": "URL to the official property or real estate source"
    }}
  ]
}}"""
    }
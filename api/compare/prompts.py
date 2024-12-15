def get_comparison_prompts(source_state: str, target_state: str) -> dict:
    """Get all comparison prompts with formatted state names"""
    
    return {
        "laws": f"""Return only a JSON object comparing laws between {source_state} and {target_state}. Format:
{{
  "data": {{
    "data": [
      {{
        "title": "Title of the law",
        "description": "Description of how the law differs in the target state",
        "state_reference": "Reference to the specific state law code or statute",
        "impact": "Brief explanation of how this difference impacts new residents",
        "source_link": "URL to the official state or government source for verification"
      }}
    ]
  }}
}}""",

        "taxes": f"""Return only a JSON object comparing taxes between {source_state} and {target_state}. Format:
{{
  "data": {{
    "data": [
      {{
        "title": "Title of the tax",
        "description": "Description of how the tax differs in the target state",
        "state_reference": "Reference to the specific state tax code",
        "impact": "Brief explanation of how this difference impacts new residents",
        "source_link": "URL to the official state tax authority source"
      }}
    ]
  }}
}}""",

        "education": f"""Return only a JSON object comparing education between {source_state} and {target_state}. Format:
{{
  "data": {{
    "data": [
      {{
        "title": "Title of education difference",
        "description": "Description of how education differs in the target state",
        "state_reference": "Reference to specific education code or policy",
        "impact": "Brief explanation of how this difference impacts new residents",
        "source_link": "URL to the official education department source"
      }}
    ]
  }}
}}""",

        "emergency_services": f"""Return only a JSON object comparing emergency services between {source_state} and {target_state}. Format:
{{
  "data": {{
    "data": [
      {{
        "title": "Title of emergency service difference",
        "description": "Description of how the service differs in the target state",
        "state_reference": "Reference to specific emergency service regulation",
        "impact": "Brief explanation of how this difference impacts new residents",
        "source_link": "URL to the official emergency services source"
      }}
    ]
  }}
}}""",

        "property": f"""Return only a JSON object comparing property between {source_state} and {target_state}. Format:
{{
  "data": {{
    "data": [
      {{
        "title": "Title of property difference",
        "description": "Description of how property laws or market differs",
        "state_reference": "Reference to specific property codes or regulations",
        "impact": "Brief explanation of how this difference impacts new residents",
        "source_link": "URL to the official property or real estate source"
      }}
    ]
  }}
}}"""
    }
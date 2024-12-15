def get_general_prompt(source_state: str, target_state: str) -> str:
    """Get a general prompt that compares the states"""
    
    return (
        f"Return a JSON object that compares the following general information between {source_state} and {target_state}. "
        "The descriptions should be 1-2 small sentences summarizing the key differences: "
        '{"data": ['
        '{"title": "Tax Rates", '
        f'"description": "Describe how the tax rates differ between {source_state} and {target_state}, including the approximate percentage difference and any key differences in specific tax categories."}, '
        '{"title": "Vehicle Registration", '
        f'"description": "Explain the differences in the vehicle registration process between {source_state} and {target_state}, such as whether registration is annual or biennial, any unique requirements, and the impact on new residents."}, '
        '{"title": "Employment Laws", '
        f'"description": "Compare the employment laws and policies between {source_state} and {target_state}, highlighting any differences in areas like at-will employment, worker protections, and regulations."}, '
        '{"title": "Property Laws", '
        f'"description": "Describe the key differences in property laws and regulations between {source_state} and {target_state}, such as homestead exemptions, property tax rates, and any unique requirements for real estate transactions."}, '
        '{"title": "Education", '
        f'"description": "Contrast the education systems between {source_state} and {target_state}, including differences in school district structures, curriculum standards, funding mechanisms, and any notable policy variations."}'
        ']}'
    )

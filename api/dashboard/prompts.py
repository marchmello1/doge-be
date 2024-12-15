from typing import Callable, Dict

def get_general_prompts(source_state: str, target_state: str) -> Dict[str, Callable[[], str]]:
    """Get all general prompts with formatted state names"""
    return {
        "tax_rates": lambda: f"State tax rate variation between {source_state} and {target_state}.",
        "vehicle_registration": lambda: f"Annual vs biennial vehicle registration between {source_state} and {target_state}.",
        "employment_laws": lambda: f"{source_state} and {target_state} have different at-will employment policies.",
        "property_laws": lambda: f"{source_state} and {target_state} have different homestead exemptions.",
        "education": lambda: f"{source_state} and {target_state} have different school district regulations."
    }

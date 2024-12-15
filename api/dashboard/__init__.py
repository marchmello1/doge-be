from .api.dashboard.models import Response
from .api.dashboard.prompts import get_general_prompt
from .api.dashboard.methods import get_general_info


__all__ = [
    "Response",
    "get_general_prompt",
    "get_general_info"
]

from typing import Any, Optional



def success_response(message: str, data: Optional[Any]={}) -> dict:
    """
    Generate a success response dictionary.
    Parameters:
        - message (str): The success message to include in the response.
        - data (Optional[Any]): Optional additional data to include in the response. Can be of any type.
    Returns:
        - dict: A dictionary containing the success status, message, and optionally the data if provided.
    Example:
        - success_response("Operation completed successfully", {"id": 123}) -> {"success": True, "message": "Operation completed successfully", "data": {"id": 123}}
    """
    if data is None:
        return {"success": True, "message": message}

    return {"success": True, "message": message, "data": data}

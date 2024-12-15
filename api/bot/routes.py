from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import Union, Optional
from fastapi.responses import JSONResponse, PlainTextResponse
from api.bot.methods import RelocationBot
from env import env
import logging
import os
import uuid
from datetime import datetime

router = APIRouter(
    prefix="/api/v1/bot",
    tags=["Bot"],
    responses={404: {"description": "Not found"}},
)

# Configuration for file uploads
UPLOAD_DIR = "uploads"
ALLOWED_DOCUMENT_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx"
}
ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif"
}

def setup_upload_directory():
    """Create upload directory if it doesn't exist"""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

def generate_unique_filename(original_filename: str, file_type: str) -> str:
    """Generate a unique filename with timestamp and UUID"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    extension = os.path.splitext(original_filename)[1] or file_type
    return f"{timestamp}_{unique_id}{extension}"

async def save_uploaded_file(file: UploadFile, allowed_types: dict) -> str:
    """
    Save uploaded file and return its path
    Raises ValueError if file type is not allowed
    """
    if file.content_type not in allowed_types:
        raise ValueError(f"Unsupported file type: {file.content_type}")
    
    filename = generate_unique_filename(file.filename, allowed_types[file.content_type])
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return file_path

def cleanup_old_files():
    """Delete files older than 24 hours"""
    current_time = datetime.now().timestamp()
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getctime(file_path)
            if file_age > 86400:  # 24 hours in seconds
                try:
                    os.remove(file_path)
                except Exception as e:
                    logging.error(f"Error deleting file {file_path}: {e}")

@router.post("/")
async def bot_endpoint(
    message: str = Form(...),
    document: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None)
):
    """
    Handle bot requests with file uploads
    """
    try:
        setup_upload_directory()
        cleanup_old_files()
        
        document_path = None
        image_path = None
        
        # Handle document upload
        if document:
            try:
                document_path = await save_uploaded_file(document, ALLOWED_DOCUMENT_TYPES)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        # Handle image upload
        if image:
            try:
                image_path = await save_uploaded_file(image, ALLOWED_IMAGE_TYPES)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        # Process the request
        bot = RelocationBot(api_key=env.XAI_KEY)
        result = bot.chat(
            message=message,
            document=document_path,
            image=image_path
        )
        
        return PlainTextResponse(content=result)
        
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Internal server error: {str(e)}"
            }
        )
    finally:
        # Clean up uploaded files after processing
        for file_path in filter(None, [document_path, image_path]):
            try:
                os.remove(file_path)
            except Exception as e:
                logging.error(f"Error removing file {file_path}: {e}")
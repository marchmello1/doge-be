from openai import OpenAI
import base64
from typing import Optional, Union
import speech_recognition as sr
import PyPDF2
import docx
from api.bot.prompts import SYSTEM_MESSAGES

class RelocationBot:
    def __init__(self, api_key: str, api_base: str = "https://api.x.ai/v1", system_message_type: str = 'detailed'):
        if not api_key:
            raise ValueError("API key is required")
            
        self.client = OpenAI(
            api_key=api_key,
            base_url=api_base
        )
        
        self.messages = [{
            "role": "system",
            "content": SYSTEM_MESSAGES
        }]
        
        self.recognizer = sr.Recognizer()

    def process_audio(self, audio_file: str) -> str:
        """Process audio file to text"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                return self.recognizer.recognize_google(audio)
        except Exception as e:
            return f"Error processing audio: {str(e)}"

    def process_document(self, file_path: str) -> str:
        """Process PDF or DOCX document"""
        try:
            if file_path.lower().endswith('.pdf'):
                return self._read_pdf(file_path)
            elif file_path.lower().endswith('.docx'):
                return self._read_docx(file_path)
            else:
                return "Unsupported document format"
        except Exception as e:
            return f"Error processing document: {str(e)}"

    def _read_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    def _read_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    def chat(self, 
             message: Optional[str] = None, 
             image: Optional[Union[str, bytes]] = None, 
             audio: Optional[str] = None,
             document: Optional[str] = None,
             is_url: bool = False) -> str:
        try:
            content = []
            
            
            if image:
                if is_url:
                    image_data = {"url": image}
                else:
                    base64_image = image if isinstance(image, str) and image.startswith("data:image") else self.encode_image(image)
                    image_data = {"url": f"data:image/jpeg;base64,{base64_image}"}
                
                content.append({
                    "type": "image_url",
                    "image_url": {
                        **image_data,
                        "detail": "high"
                    }
                })

            
            if audio:
                audio_text = self.process_audio(audio)
                message = audio_text if message is None else f"{message} {audio_text}"

           
            if document:
                doc_text = self.process_document(document)
                message = doc_text if message is None else f"{message}\n\nDocument content: {doc_text}"
            
          
            if message:
                content.append({
                    "type": "text",
                    "text": message
                })

            self.messages.append({
                "role": "user",
                "content": content
            })

            response = self.client.chat.completions.create(
                model="grok-vision-beta",
                messages=self.messages,
                temperature=0.7,
                stream=True
            )

            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content

            self.messages.append({
                "role": "assistant",
                "content": full_response
            })

            return full_response

        except Exception as e:
            return f"Error: {str(e)}"

    def encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def reset(self):
        self.messages = [self.messages[0]]

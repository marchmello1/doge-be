from openai import OpenAI
import base64
from typing import Optional, Union
from api.bot.prompts import SYSTEM_MESSAGES

class RelocationBot:
    def __init__(self, api_key: str, api_base: str = "https://api.x.ai/v1", system_message_type: str = 'detailed'):
        if not api_key:
            raise ValueError("API key is required")
            
        self.client = OpenAI(
            api_key=api_key,
            base_url=api_base
        )
        
        # Get system message from prompts
        system_message = SYSTEM_MESSAGES.get(system_message_type, SYSTEM_MESSAGES['default'])
        self.messages = [{
            "role": "system",
            "content": system_message
        }]

    def chat(self, message: str, image: Optional[Union[str, bytes]] = None, is_url: bool = False) -> str:
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

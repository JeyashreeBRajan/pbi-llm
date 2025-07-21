import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class GroqService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = os.getenv("GROQ_MODEL", "whisper-large-v3-turbo")  # OpenAI model

    async def get_response(self, message: str, context: Optional[str] = None) -> str:
        """Get response from Groq model (OpenAI-compatible)"""
        try:
            prompt = message
            if context:
                prompt = f"Context: {context}\n\nUser Question: {message}"

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }

            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            return data["choices"][0]["message"]["content"]

        except Exception as e:
            return f"Error: {str(e)}"

# Try to create instance
try:
    groq_service = GroqService()
except Exception as e:
    print(f"Could not initialize Groq service: {e}")
    groq_service = None

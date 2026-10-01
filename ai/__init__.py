import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = "gemini-2.0-flash"

client = genai.Client(api_key=api_key) if api_key else None

def generate_outline(data: dict):
    try:
        if not client:
            return {"outline": "Error: API Key missing in .env"}

        prompt = f"""
        Create a comic book outline.
        Title: {data.get('title')}
        Genre: {data.get('genre')}
        Theme: {data.get('theme')}
        Characters: {data.get('characters')}
        Setting: {data.get('setting')}
        Pages: {data.get('pages')}
        Write 3 pages with dialogues.
        """

        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return {"outline": response.text}
    except Exception as e:
        return {"outline": f"AI Error: {str(e)}"}
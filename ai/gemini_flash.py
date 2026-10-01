import json
import os
import re

from google import genai
from dotenv import load_dotenv

load_dotenv()


def _get_client():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY or GOOGLE_API_KEY is not set. Add it to your .env file before running the app."
        )
    return genai.Client(api_key=api_key)


def _extract_flashcards(text: str):
    if not text:
        return []

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            cards = parsed.get("cards") or parsed.get("flashcards") or []
            if isinstance(cards, list):
                return cards
        if isinstance(parsed, list):
            return parsed
    except Exception:
        pass

    match = re.search(r"\[\s*\{.*?\}\s*\]", text, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(0))
            if isinstance(parsed, list):
                return parsed
        except Exception:
            pass

    return []


def generate_outline(data: dict):
    payload = data or {}
    title = str(payload.get("title", "Chennai Hero") or "Chennai Hero")
    pages = int(payload.get("pages", 3) or 3)

    prompt = (
        f"Create a cinematic comic story for '{title}' with {pages} pages. "
        "Return valid JSON only. Use this structure: "
        "{\"summary\": \"short one-paragraph story summary\", "
        "\"cards\": [{\"front\": \"short prompt/question\", \"back\": \"answer/explanation\"}, ...]} "
        "Use 4 to 6 flashcards that summarize the hero, villain, conflict, turning point, climax, and ending."
    )

    try:
        client = _get_client()
        model_candidates = [
            "gemini-3.8-flash",
            "gemini-3.5-flash-lite",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-flash-latest",
        ]
        last_error = None

        for model_name in model_candidates:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                text = getattr(response, "text", None) or str(response)
                cards = _extract_flashcards(text)
                if cards:
                    summary = "Flash card story summary."
                    try:
                        parsed = json.loads(text)
                        if isinstance(parsed, dict):
                            summary = parsed.get("summary", summary)
                    except Exception:
                        pass
                    return {
                        "title": title,
                        "pages": pages,
                        "summary": summary,
                        "cards": cards,
                        "outline": summary,
                    }
                return {
                    "title": title,
                    "pages": pages,
                    "summary": text,
                    "cards": [],
                    "outline": text,
                }
            except Exception as exc:
                last_error = exc

        raise RuntimeError(f"No supported Gemini model worked. Last error: {last_error}")
    except Exception as exc:
        return {
            "title": title,
            "pages": pages,
            "summary": f"Unable to generate outline: {exc}",
            "cards": [],
            "outline": f"Unable to generate outline: {exc}",
            "error": str(exc),
        }
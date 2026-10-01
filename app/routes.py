from fastapi import APIRouter
from ai.gemini_flash import generate_outline

router = APIRouter()


@router.post("/generate-outline")
def create_outline(data: dict | None = None):
    payload = data or {}
    result = generate_outline(payload)
    return result
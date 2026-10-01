from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routes import router


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="ComicCraftAI",
    description="AI-powered comic generation application",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# STATIC FILES
# ============================================================

if STATIC_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(STATIC_DIR)),
        name="static",
    )


# ============================================================
# API ROUTES
# ============================================================

app.include_router(router)


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/", include_in_schema=False)
async def home():

    index_file = TEMPLATES_DIR / "index.html"

    if not index_file.exists():
        return {
            "message": "ComicCraftAI backend is running.",
            "error": "templates/index.html was not found.",
        }

    return FileResponse(index_file)


# ============================================================
# FAVICON
# ============================================================

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():

    favicon_file = STATIC_DIR / "favicon.ico"

    if favicon_file.exists():
        return FileResponse(favicon_file)

    return {
        "message": "No favicon configured."
    }


# ============================================================
# APPLICATION HEALTH
# ============================================================

@app.get("/health", include_in_schema=False)
async def health():

    return {
        "status": "healthy",
        "application": "ComicCraftAI",
        "version": "1.0.0",
    }


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
async def startup_event():

    print("=" * 60)
    print("ComicCraftAI")
    print("Application started successfully")
    print("=" * 60)
    print(f"Base directory : {BASE_DIR}")
    print(f"Templates      : {TEMPLATES_DIR}")
    print(f"Static files   : {STATIC_DIR}")
    print("=" * 60)


# ============================================================
# SHUTDOWN
# ============================================================

@app.on_event("shutdown")
async def shutdown_event():

    print("=" * 60)
    print("ComicCraftAI application shutting down...")
    print("=" * 60)
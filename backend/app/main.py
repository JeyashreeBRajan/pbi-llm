import sys
import os
import json
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Dict
from pathlib import Path

# Load environment variables
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Chat with Data API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load PBI schema from local file
PBI_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "pbi_schema.json")
pbi_schema = {}
try:
    with open(PBI_SCHEMA_PATH, "r") as f:
        pbi_schema = json.load(f)
except Exception as e:
    logger.error(f"Failed to load pbi_schema.json: {e}")

@app.get("/api/powerbi/local-schema")
def get_local_pbi_schema():
    """Return the static Power BI semantic model loaded from file"""
    if not pbi_schema:
        raise HTTPException(status_code=404, detail="PBI schema not loaded")
    return {"success": True, "schema": pbi_schema}

# Import Groq service
groq_available = False
groq_service = None
try:
    from app.groq_service import groq_service as cs
    if cs is not None:
        groq_service = cs
        groq_available = True
        logger.info("groq service initialized successfully")
except Exception as e:
    logger.error(f"groq service not available: {e}")

# Optional service imports
multi_agent_available = False
try:
    from app.multi_agent_service import multi_agent_service
    multi_agent_available = True
except:
    pass

try:
    from app.knowledge_base_service import knowledge_base_service
except:
    pass

# Error handlers
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": str(exc)}
    )

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Chat with Data API",
        "status": "running",
        "version": "1.0.0",
        "groq_available": groq_available
    }

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "groq_available": groq_available}

# API config check
@app.get("/api/config")
def check_config():
    api_key_exists = bool(os.getenv("GROQ_API_KEY"))
    return {
        "groq_configured": api_key_exists and groq_available,
        "api_key_exists": api_key_exists,
        "groq_service_loaded": groq_available,
        "app_name": os.getenv("APP_NAME", "Chat with Data")
    }

# Natural language to DAX
@app.post("/api/powerbi/query-natural")
async def query_powerbi_natural(body: Dict):
    question = body.get("question", "")
    if not question:
        raise HTTPException(status_code=400, detail="question is required")

    from app.llm_query_generator import generate_dax_from_schema
    result = generate_dax_from_schema(question, pbi_schema)

    return {
        "response": result.get("answer", "Query completed"),
        "dax_query": result.get("dax_query"),
        "success": result.get("success", False)
    }

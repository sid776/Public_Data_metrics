"""FastAPI application entrypoint."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: ensure data dirs; shutdown: nothing special."""
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(
    title="Document Intelligence API",
    description="RAG-powered document Q&A for environmental and social specialists. Proof of Concept for AI/ML workflows.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.get("/")
def root():
    return {
        "service": "Document Intelligence POC",
        "docs": "/docs",
        "health": "/api/v1/health",
    }

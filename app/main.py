"""
FastAPI application factory for Medical Document Processor.
"""
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from app.api import documents, extract, validate, fhir
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.db.session import close_db, init_db

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting Medical Document Processor...")
    configure_logging()
    await init_db()

    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    logger.info("Application started")
    yield

    logger.info("Shutting down...")
    await close_db()
    logger.info("Application stopped")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Medical Document Processor",
        description="Medical document processor with NER, validation, and FHIR export",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(documents.router, prefix="/api/v1")
    app.include_router(extract.router, prefix="/api/v1")
    app.include_router(validate.router, prefix="/api/v1")
    app.include_router(fhir.router, prefix="/api/v1")

    @app.get("/", include_in_schema=False)
    async def root():
        return {
            "name": "Medical Document Processor",
            "version": "0.1.0",
            "docs": "/docs",
            "health": "/api/v1/health",
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level=settings.log_level.lower(),
    )
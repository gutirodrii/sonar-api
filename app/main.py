from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog


def create_app() -> FastAPI:
    app = FastAPI(
        title="Sonar Experiment API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Logging config
    structlog.configure(processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.EventRenamer("message"),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ])

    # Routers
    from app.api.public.routes import public_router
    from app.api.admin.routes import admin_router

    app.include_router(public_router, prefix="/api/public", tags=["public"])
    app.include_router(admin_router, prefix="/api/admin", tags=["admin"])

    return app


app = create_app()


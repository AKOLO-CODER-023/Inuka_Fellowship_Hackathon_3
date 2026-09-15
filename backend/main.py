"""
backend/main.py

Inuka Fellowship Hackathon 3
Backend API using FastAPI.

Run the API from the project root with:

    python -m uvicorn backend.main:app --reload

Then open:

    http://127.0.0.1:8000/

API documentation:

    http://127.0.0.1:8000/docs
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from backend.database import (
    initialize_database,
    get_inventory,
    get_decisions,
)

from backend.schemas import (
    ForecastRequest,
    ForecastResponse,
    ReplenishmentRequest,
    HealthResponse,
)

from backend.services import generate_replenishment_decision


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("inuka-api")


# ============================================================
# APPLICATION STARTUP / SHUTDOWN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Code that runs when the FastAPI application starts
    and stops.
    """

    # Initialize the SQLite database when the API starts.
    try:
        initialize_database()
        logger.info("Database initialized successfully.")

    except Exception:
        logger.exception("Database initialization failed.")
        raise

    logger.info("======================================")
    logger.info("Inuka Supply Chain API started")
    logger.info("======================================")

    # Allow the application to continue running.
    yield

    # This runs when the application is stopped.
    logger.info("Inuka Supply Chain API stopped.")


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Inuka Supply Chain API",
    description=(
        "Backend API for inventory forecasting, "
        "replenishment decisions, alerts and ROI analysis."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    """
    API homepage.

    This is useful for checking whether the server
    is running.
    """

    return {
        "message": "Inuka Supply Chain API is running",
        "status": "healthy",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Check whether the API is running.

    Used by deployment systems, monitoring systems
    and CI/CD health checks.
    """

    return {
        "status": "healthy",
        "service": "inuka-api",
    }


# ============================================================
# INVENTORY ENDPOINT
# ============================================================

@app.get("/inventory")
def inventory_endpoint():
    """
    Return all inventory records.

    Example:

        GET /inventory
    """

    try:
        inventory = get_inventory()

        return {
            "count": len(inventory),
            "items": inventory,
        }

    except Exception:
        logger.exception("Unable to retrieve inventory.")

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve inventory.",
        )


# ============================================================
# FORECAST ENDPOINT
# ============================================================

@app.post("/forecast", response_model=ForecastResponse)
def forecast_endpoint(request: ForecastRequest):
    """
    Forecast demand for a product at a depot.

    NOTE:
    This currently returns the forecast value supplied
    by the request.

    Later, this endpoint can be connected to Member 1's
    actual forecasting model.
    """

    logger.info(
        "Forecast request received | depot=%s | product=%s",
        request.depot,
        request.product,
    )

    return {
        "depot": request.depot,
        "product": request.product,
        "forecast_demand_m3": request.forecast_demand_m3,
    }


# ============================================================
# REPLENISHMENT ENDPOINT
# ============================================================

@app.post("/replenishment")
def replenishment_endpoint(request: ReplenishmentRequest):
    """
    Generate a replenishment recommendation.

    This endpoint passes the request data to the
    decision engine through services.py.
    """

    logger.info(
        "Replenishment request received | depot=%s | product=%s",
        request.depot,
        request.product,
    )

    try:

        # Convert the Pydantic request model into a dictionary.
        request_data = request.model_dump()

        # Send the data to the business/service layer.
        result = generate_replenishment_decision(
            request_data
        )

        logger.info(
            "Replenishment decision generated successfully."
        )

        return result

    except ValueError as error:

        # Business-rule or validation error.
        logger.warning(
            "Replenishment validation failed: %s",
            error,
        )

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception:

        # Unexpected error.
        logger.exception(
            "Unexpected error while generating replenishment decision."
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to generate replenishment decision.",
        )


# ============================================================
# ALERTS ENDPOINT
# ============================================================

@app.get("/alerts")
def alerts_endpoint():
    """
    Return high-risk and critical replenishment decisions.

    These records can later be displayed on the
    Streamlit dashboard.
    """

    try:

        decisions = get_decisions()

        alerts = [
            decision
            for decision in decisions
            if decision.get("risk_level") in {
                "CRITICAL",
                "HIGH",
            }
        ]

        return {
            "count": len(alerts),
            "alerts": alerts,
        }

    except Exception:

        logger.exception(
            "Unable to retrieve alerts."
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve alerts.",
        )


# ============================================================
# BATCHES ENDPOINT
# ============================================================

@app.get("/batches")
def batches_endpoint():
    """
    Return replenishment decision records.

    For the current prototype, replenishment decisions
    are represented as batch records.
    """

    try:

        decisions = get_decisions()

        return {
            "count": len(decisions),
            "batches": decisions,
        }

    except Exception:

        logger.exception(
            "Unable to retrieve batches."
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve batches.",
        )


# ============================================================
# ROI ENDPOINT
# ============================================================

@app.get("/roi")
def roi_endpoint():
    """
    ROI analysis endpoint.

    This is currently a placeholder and can later
    connect to the project's ROI comparison dataset.
    """

    return {
        "status": "demo",
        "message": (
            "ROI endpoint is ready for connection "
            "to roi_comparison_2026.csv."
        ),
    }


# ============================================================
# API INFORMATION ENDPOINT
# ============================================================

@app.get("/api-info")
def api_info():
    """
    Return information about the available API endpoints.
    """

    return {
        "project": "Inuka Fellowship Hackathon 3",
        "api": "Inuka Supply Chain API",
        "version": "1.0.0",

        "endpoints": {
            "home": "GET /",
            "health": "GET /health",
            "inventory": "GET /inventory",
            "forecast": "POST /forecast",
            "replenishment": "POST /replenishment",
            "alerts": "GET /alerts",
            "batches": "GET /batches",
            "roi": "GET /roi",
            "documentation": "GET /docs",
        },
    }


# ============================================================
# GLOBAL ERROR HANDLER
# ============================================================

@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    """
    Catch unexpected application errors.

    The actual error is written to the terminal logs,
    while the user receives a simple message.
    """

    logger.exception(
        "Unhandled application error on %s",
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error.",
            "path": request.url.path,
        },
    )

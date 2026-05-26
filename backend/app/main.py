from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.schemas import (
    AnalyzeTrendsRequest,
    AnalyzeTrendsResponse,
    ErrorResponse,
    GDELTFetchResponse,
    HealthResponse,
)
from app.services.gdelt_service import GDELTFetchError, fetch_gdelt_articles
from app.services.trend_analyzer import analyze_trends_with_langchain

settings = get_settings()

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", app_name=settings.app_name)


@app.get("/fetch-gdelt", response_model=GDELTFetchResponse)
async def fetch_gdelt(
    query: str = Query(..., min_length=1),
    max_articles: int = Query(default=20, ge=1, le=50),
) -> GDELTFetchResponse:
    try:
        articles = await fetch_gdelt_articles(query=query, max_articles=max_articles, settings=settings)
    except GDELTFetchError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - external dependency failure
        raise HTTPException(status_code=502, detail=f"Failed to fetch GDELT articles: {exc}") from exc

    return GDELTFetchResponse(query=query, count=len(articles), articles=articles)


@app.post("/analyze-trends", response_model=AnalyzeTrendsResponse)
async def analyze_trends(payload: AnalyzeTrendsRequest) -> AnalyzeTrendsResponse:
    try:
        articles = await fetch_gdelt_articles(
            query=payload.query,
            max_articles=payload.max_articles,
            settings=settings,
        )
    except GDELTFetchError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - external dependency failure
        raise HTTPException(status_code=502, detail=f"Failed to fetch GDELT articles: {exc}") from exc

    analysis = await analyze_trends_with_langchain(
        query=payload.query,
        articles=articles,
        settings=settings,
    )

    return AnalyzeTrendsResponse(
        query=payload.query,
        summary=analysis.summary,
        overall_recommendation=analysis.overall_recommendation,
        top_trends=analysis.top_trends,
        sources=articles,
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(detail=str(exc.detail)).model_dump(),
    )

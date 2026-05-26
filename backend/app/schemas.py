from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class HealthResponse(BaseModel):
    status: str
    app_name: str


class Article(BaseModel):
    title: str = ""
    url: HttpUrl | str = ""
    domain: str = ""
    source_country: str = ""
    language: str = ""
    published_at: str = ""
    snippet: str = ""


class GDELTFetchResponse(BaseModel):
    query: str
    count: int
    articles: list[Article]


class AnalyzeTrendsRequest(BaseModel):
    query: str = Field(min_length=1)
    max_articles: int = Field(default=20, ge=1, le=50)


class TrendInsight(BaseModel):
    topic: str
    attention_score: int = Field(ge=0, le=100)
    why_it_is_trending: str
    target_audience: str
    recommended_action: str
    content_ideas: list[str] = Field(default_factory=list)
    campaign_angles: list[str] = Field(default_factory=list)
    best_channels: list[str] = Field(default_factory=list)
    risk_level: str
    confidence: str


class TrendAnalysisPayload(BaseModel):
    summary: str
    overall_recommendation: str
    top_trends: list[TrendInsight]


class AnalyzeTrendsResponse(TrendAnalysisPayload):
    query: str
    sources: list[Article]


class ErrorResponse(BaseModel):
    detail: str
    extra: dict[str, Any] | None = None

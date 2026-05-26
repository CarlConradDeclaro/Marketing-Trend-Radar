from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx

from app.config import Settings
from app.schemas import Article

GDELT_ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return text


def _normalize_article(raw: dict[str, Any]) -> Article:
    title = _clean_text(
        raw.get("title")
        or raw.get("seendate_title")
        or raw.get("docTitle")
        or raw.get("source")
    )
    url = _clean_text(raw.get("url") or raw.get("documenturl") or raw.get("documentUrl"))
    domain = _clean_text(raw.get("domain") or raw.get("sourceDomain") or raw.get("source"))
    source_country = _clean_text(raw.get("sourceCountry") or raw.get("country") or raw.get("sourcecountry"))
    language = _clean_text(raw.get("language") or raw.get("lang"))
    published_at = _clean_text(raw.get("seendate") or raw.get("date") or raw.get("datetime"))
    snippet = _clean_text(raw.get("snippet") or raw.get("summary") or raw.get("description"))

    return Article(
        title=title,
        url=url,
        domain=domain,
        source_country=source_country,
        language=language,
        published_at=published_at,
        snippet=snippet,
    )


def _extract_article_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []

    for key in ("articles", "Articles", "artlist", "doc", "items", "results"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]

    return []


async def fetch_gdelt_articles(query: str, max_articles: int, settings: Settings) -> list[Article]:
    params = {
        "query": query,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": max_articles,
        "sort": "DateDesc",
    }

    timeout = httpx.Timeout(settings.gdelt_timeout_seconds)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(GDELT_ENDPOINT, params=params)
        response.raise_for_status()
        payload = response.json()

    raw_articles = _extract_article_items(payload)
    cleaned = [_normalize_article(item) for item in raw_articles]

    unique: list[Article] = []
    seen_urls: set[str] = set()
    for article in cleaned:
        key = article.url if isinstance(article.url, str) else str(article.url)
        if key in seen_urls:
            continue
        seen_urls.add(key)
        unique.append(article)

    return unique[:max_articles]


def extract_recent_dates(articles: list[Article]) -> list[datetime]:
    dates: list[datetime] = []
    for article in articles:
        if not article.published_at:
            continue
        try:
            dates.append(datetime.fromisoformat(article.published_at.replace("Z", "+00:00")))
        except ValueError:
            continue
    return dates

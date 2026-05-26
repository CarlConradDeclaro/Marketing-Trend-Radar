from __future__ import annotations

import asyncio
import html
from datetime import datetime
from urllib.parse import urlparse
from typing import Any
from xml.etree import ElementTree

import httpx

from app.config import Settings
from app.schemas import Article

GDELT_ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"
GDELT_RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
GOOGLE_NEWS_RSS_ENDPOINT = "https://news.google.com/rss/search"


class GDELTFetchError(RuntimeError):
    """Raised when GDELT cannot be fetched reliably."""


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


def _domain_from_url(value: str) -> str:
    if not value:
        return ""
    parsed = urlparse(value)
    return parsed.netloc.replace("www.", "")


def _decode_feed_text(value: str | None) -> str:
    return html.unescape(value or "").strip()


def _normalize_rss_article(item: ElementTree.Element) -> Article:
    title = _decode_feed_text(item.findtext("title"))
    url = _decode_feed_text(item.findtext("link"))
    source_element = item.find("source")
    source_name = _decode_feed_text(source_element.text if source_element is not None else "")
    source_url = _decode_feed_text(source_element.attrib.get("url") if source_element is not None else "")
    domain = source_name or _domain_from_url(source_url) or _domain_from_url(url)
    published_at = _decode_feed_text(item.findtext("pubDate"))
    snippet = _decode_feed_text(item.findtext("description"))

    return Article(
        title=title,
        url=url,
        domain=domain,
        source_country="",
        language="en",
        published_at=published_at,
        snippet=snippet,
    )


async def fetch_gdelt_articles(query: str, max_articles: int, settings: Settings) -> list[Article]:
    try:
        gdelt_articles = await _fetch_gdelt_articles(query=query, max_articles=max_articles, settings=settings)
        if gdelt_articles:
            return gdelt_articles
    except GDELTFetchError:
        pass

    return await fetch_google_news_articles(query=query, max_articles=max_articles, settings=settings)


async def _fetch_gdelt_articles(query: str, max_articles: int, settings: Settings) -> list[Article]:
    params = {
        "query": query,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": max_articles,
        "sort": "DateDesc",
    }

    timeout = httpx.Timeout(settings.gdelt_timeout_seconds)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response: httpx.Response | None = None
        last_error: Exception | None = None
        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                response = await client.get(GDELT_ENDPOINT, params=params)
                if response.status_code in GDELT_RETRY_STATUS_CODES:
                    retry_after = response.headers.get("Retry-After")
                    if attempt < max_attempts:
                        delay = float(retry_after) if retry_after and retry_after.isdigit() else 2.0 * attempt
                        await asyncio.sleep(delay)
                        continue
                    raise GDELTFetchError(
                        "GDELT is temporarily rate limiting requests. Please try again in a moment."
                    )

                response.raise_for_status()
                payload = response.json()
                break
            except (httpx.RequestError, httpx.HTTPStatusError, ValueError) as exc:
                last_error = exc
                if attempt < max_attempts:
                    await asyncio.sleep(2.0 * attempt)
                    continue
                if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code in GDELT_RETRY_STATUS_CODES:
                    raise GDELTFetchError(
                        "GDELT is temporarily rate limiting requests. Please try again in a moment."
                    ) from exc
                raise GDELTFetchError("Failed to fetch GDELT articles.") from exc
        else:  # pragma: no cover - loop is always broken or raised
            if last_error is not None:
                raise GDELTFetchError("Failed to fetch GDELT articles.") from last_error
            raise GDELTFetchError("Failed to fetch GDELT articles.")

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


async def fetch_google_news_articles(query: str, max_articles: int, settings: Settings) -> list[Article]:
    params = {
        "q": query,
        "hl": "en-US",
        "gl": "US",
        "ceid": "US:en",
    }

    timeout = httpx.Timeout(settings.gdelt_timeout_seconds)
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            response = await client.get(GOOGLE_NEWS_RSS_ENDPOINT, params=params)
            response.raise_for_status()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        raise GDELTFetchError("Google News fallback is temporarily unavailable.") from exc

    try:
        root = ElementTree.fromstring(response.text)
    except ElementTree.ParseError as exc:
        raise GDELTFetchError("Failed to parse Google News fallback feed.") from exc

    items = root.findall("./channel/item")
    articles = [_normalize_rss_article(item) for item in items]

    unique: list[Article] = []
    seen_urls: set[str] = set()
    for article in articles:
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

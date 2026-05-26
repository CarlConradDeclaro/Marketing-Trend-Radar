from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from app.agents.marketing_trend_agent import build_marketing_trend_prompt
from app.config import Settings
from app.schemas import Article, TrendAnalysisPayload, TrendInsight

try:
    from langchain_openai import ChatOpenAI
except Exception:  # pragma: no cover - dependency import guard
    ChatOpenAI = None


@dataclass
class HeuristicAnalysis:
    summary: str
    overall_recommendation: str
    top_trends: list[TrendInsight]


def _extract_keywords(articles: Iterable[Article]) -> list[tuple[str, int]]:
    words: Counter[str] = Counter()
    stop_words = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "that",
        "this",
        "into",
        "your",
        "you",
        "are",
        "how",
        "new",
        "why",
        "what",
        "will",
        "can",
        "use",
        "market",
        "marketing",
        "ai",
    }

    for article in articles:
        text = f"{article.title} {article.snippet}".lower()
        cleaned = []
        for token in text.replace("-", " ").replace("/", " ").split():
            token = "".join(ch for ch in token if ch.isalpha())
            if len(token) < 4 or token in stop_words:
                continue
            cleaned.append(token)
        words.update(cleaned)

    return words.most_common(6)


def _build_heuristic_trends(query: str, articles: list[Article]) -> list[TrendInsight]:
    keywords = _extract_keywords(articles)
    if not keywords:
        keywords = [(query, 1)]

    trends: list[TrendInsight] = []
    for index, (keyword, count) in enumerate(keywords[:5], start=1):
        score = min(100, 55 + (count * 8) + ((5 - index) * 4))
        trends.append(
            TrendInsight(
                topic=keyword.title(),
                attention_score=score,
                why_it_is_trending=f"The articles repeatedly mention {keyword} across multiple headlines and snippets.",
                target_audience="Marketing teams, growth leaders, and content strategists",
                recommended_action=f"Build a short-form content angle and a practical campaign test around {keyword}.",
                content_ideas=[
                    f"Explainer post about {keyword}",
                    f"Checklist for applying {keyword} in campaigns",
                ],
                campaign_angles=[
                    f"Position {keyword} as a fast-moving market opportunity",
                    f"Showcase operational benefits of {keyword}",
                ],
                best_channels=["LinkedIn", "Email", "Blog"],
                risk_level="medium" if score >= 70 else "low",
                confidence="medium" if score >= 65 else "low",
            )
        )
    return trends


def _build_heuristic_analysis(query: str, articles: list[Article]) -> HeuristicAnalysis:
    if not articles:
        return HeuristicAnalysis(
            summary=f"No current GDELT articles were found for '{query}'.",
            overall_recommendation="Try a broader or more newsworthy query, or reduce the specificity of the topic.",
            top_trends=[],
        )

    top_trends = _build_heuristic_trends(query, articles)
    leading_topics = ", ".join(trend.topic for trend in top_trends[:3])
    summary = (
        f"Recent coverage for '{query}' is concentrated around {leading_topics}."
        if leading_topics
        else f"Recent coverage for '{query}' is concentrated in a small cluster of recurring themes."
    )
    overall_recommendation = (
        "Focus on concise, educational content and quick-turn campaign tests tied to the most repeated themes."
    )
    return HeuristicAnalysis(
        summary=summary,
        overall_recommendation=overall_recommendation,
        top_trends=top_trends,
    )


def _build_articles_json(articles: list[Article]) -> str:
    payload = [article.model_dump(mode="json") for article in articles]
    return json.dumps(payload, ensure_ascii=True, indent=2)


async def analyze_trends_with_langchain(
    query: str,
    articles: list[Article],
    settings: Settings,
) -> TrendAnalysisPayload:
    if not articles:
        fallback = _build_heuristic_analysis(query, articles)
        return TrendAnalysisPayload.model_validate(fallback)

    if not settings.openai_api_key or ChatOpenAI is None:
        fallback = _build_heuristic_analysis(query, articles)
        return TrendAnalysisPayload.model_validate(fallback)

    llm = ChatOpenAI(
        model=settings.llm_model,
        temperature=0,
        api_key=settings.openai_api_key,
    )
    prompt = build_marketing_trend_prompt()
    structured_llm = llm.with_structured_output(TrendAnalysisPayload)
    chain = prompt | structured_llm

    try:
        result = await chain.ainvoke(
            {
                "query": query,
                "articles_json": _build_articles_json(articles),
            }
        )
        return result
    except Exception:
        fallback = _build_heuristic_analysis(query, articles)
        return TrendAnalysisPayload.model_validate(fallback)

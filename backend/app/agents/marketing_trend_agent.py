from langchain_core.prompts import ChatPromptTemplate


SYSTEM_PROMPT = """You are a Marketing Trend Analyst Agent.
Analyze the provided GDELT articles and identify marketing topics getting attention.
Give practical recommendations, content ideas, campaign angles, target audiences, best channels, risks, and confidence scores.
Base your answer only on the provided data.
Return valid JSON only.
"""


def build_marketing_trend_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            (
                "user",
                "Query: {query}\n\nArticle data:\n{articles_json}\n",
            ),
        ]
    )

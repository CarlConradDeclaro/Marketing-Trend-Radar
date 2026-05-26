export type Article = {
  title: string;
  url: string;
  domain: string;
  source_country: string;
  language: string;
  published_at: string;
  snippet: string;
};

export type TrendInsight = {
  topic: string;
  attention_score: number;
  why_it_is_trending: string;
  target_audience: string;
  recommended_action: string;
  content_ideas: string[];
  campaign_angles: string[];
  best_channels: string[];
  risk_level: string;
  confidence: string;
};

export type AnalyzeTrendsResponse = {
  query: string;
  summary: string;
  overall_recommendation: string;
  top_trends: TrendInsight[];
  sources: Article[];
};

export type AnalyzeTrendsRequest = {
  query: string;
  max_articles: number;
};


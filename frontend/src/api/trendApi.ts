import type { AnalyzeTrendsRequest, AnalyzeTrendsResponse } from "@/types/trend";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function parseResponse<T>(response: Response): Promise<T> {
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json") ? await response.json() : await response.text();

  if (!response.ok) {
    const message =
      typeof payload === "object" && payload && "detail" in payload
        ? String((payload as { detail: unknown }).detail)
        : "Request failed";
    throw new Error(message);
  }

  return payload as T;
}

export async function analyzeTrends(input: AnalyzeTrendsRequest): Promise<AnalyzeTrendsResponse> {
  const response = await fetch(`${API_BASE}/analyze-trends`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(input),
  });

  return parseResponse<AnalyzeTrendsResponse>(response);
}


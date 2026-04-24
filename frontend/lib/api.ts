import { PredictInput, PredictResponse, HistoryRecord } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5001/api";

export async function predictAMR(input: PredictInput): Promise<PredictResponse> {
  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || err.errors?.join(", ") || "Prediction failed");
  }
  return res.json();
}

export async function getModelComparison(): Promise<Record<string, unknown>> {
  const res = await fetch(`${API_BASE}/models/comparison`);
  if (!res.ok) return {};
  return res.json();
}

export async function getMicrobes(): Promise<string[]> {
  const res = await fetch(`${API_BASE}/microbes`);
  if (!res.ok) return [];
  return res.json();
}

export async function getHistory(): Promise<HistoryRecord[]> {
  const res = await fetch(`${API_BASE}/history`);
  if (!res.ok) throw new Error("Failed to fetch history");
  return res.json();
}

export async function saveHistory(
  input: PredictInput,
  result: PredictResponse
): Promise<HistoryRecord> {
  const res = await fetch(`${API_BASE}/history`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input, result }),
  });
  if (!res.ok) throw new Error("Failed to save history");
  return res.json();
}

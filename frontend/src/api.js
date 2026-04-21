import axios from "axios";

/** Vite: .env sets direct URL. Docker build: Dockerfile sets /api/run (nginx → backend). */
export const API_URL = import.meta.env.VITE_API_URL || "/api/run";

const REQUEST_TIMEOUT_MS = 120_000;

/**
 * GET pipeline + LLM JSON. Throws on HTTP/network errors (caller handles UI).
 */
export async function fetchRunAnalysis() {
  const res = await axios.get(API_URL, { timeout: REQUEST_TIMEOUT_MS });
  return res?.data ?? null;
}

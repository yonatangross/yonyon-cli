import { CliError, usageError } from "./errors.js";

export const DEFAULT_BASE_URL = "https://yonyon.ai";

/** LLM-backed endpoints think for a while; the flat JSON ones should not. */
export const SLOW_TIMEOUT_MS = 60_000;
export const FAST_TIMEOUT_MS = 15_000;

export interface RequestContext {
  baseUrl: string;
  timeoutMs: number;
}

/** Normalize and validate a base URL so a typo fails here, not mid-request. */
export function resolveBaseUrl(raw: string | undefined): string {
  const candidate = raw ?? process.env["YONYON_BASE_URL"] ?? DEFAULT_BASE_URL;
  let parsed: URL;
  try {
    parsed = new URL(candidate);
  } catch {
    throw usageError(`--base-url must be an absolute URL, got "${candidate}".`);
  }
  if (parsed.protocol !== "http:" && parsed.protocol !== "https:") {
    throw usageError(`--base-url must be http or https, got "${parsed.protocol}".`);
  }
  return parsed.origin + parsed.pathname.replace(/\/$/, "");
}

function describeRateLimit(response: Response): CliError {
  const limit = response.headers.get("x-ratelimit-limit");
  const retryAfter = response.headers.get("retry-after");
  const ceiling = limit ? `${limit} requests per IP per minute` : "10 requests per IP per minute";
  const wait = retryAfter ? ` Retry in ${retryAfter}s.` : "";
  return new CliError(`Rate limited by yonyon.ai (${ceiling}).${wait}`, {
    hints: [
      "The public API is unauthenticated, so the budget is shared per source IP.",
      "Wait for the window to reset and run the command again.",
    ],
  });
}

/**
 * Reduce a non-JSON error body to one useful line.
 *
 * Returns "" when the body is markup with nothing quotable, because the status
 * line alone reads better than a wall of HTML.
 */
export function summariseNonJsonBody(text: string): string {
  const trimmed = text.trim();
  if (!trimmed) return "";

  const looksLikeHtml = /^\s*(<!doctype|<html|<\?xml)/i.test(trimmed);
  if (looksLikeHtml) {
    const title = /<title[^>]*>([^<]{1,200})<\/title>/i.exec(trimmed)?.[1]?.trim();
    return title ? title.replace(/\s+/g, " ") : "";
  }

  // Plain text, so it is probably already the message. Collapse whitespace so a
  // multi-line body does not smear across the terminal.
  const oneLine = trimmed.replace(/\s+/g, " ");
  return oneLine.length > 200 ? `${oneLine.slice(0, 200)}...` : oneLine;
}

/** Pull the most useful message out of an error body, whatever shape it has. */
async function describeFailure(response: Response, url: string): Promise<CliError> {
  if (response.status === 429) return describeRateLimit(response);

  let detail = "";
  try {
    const text = await response.text();
    if (text) {
      try {
        const body: unknown = JSON.parse(text);
        if (body !== null && typeof body === "object") {
          const record = body as Record<string, unknown>;
          const message = record["error"] ?? record["message"];
          const code = record["code"];
          if (typeof message === "string") detail = message;
          if (typeof code === "string") detail = detail ? `${detail} (${code})` : code;
        }
      } catch {
        // Not JSON. An HTML error page is the common case here (a wrong
        // --base-url lands on the site's 404 page, not the API), and echoing
        // 300 characters of `<!DOCTYPE html><html lang="en"...` into the
        // terminal buries the one line that matters. Prefer the <title>, and
        // otherwise say nothing rather than paste markup.
        detail = summariseNonJsonBody(text);
      }
    }
  } catch {
    // A body we cannot read is not more informative than the status line.
  }

  const suffix = detail ? `: ${detail}` : "";
  return new CliError(`Request to ${url} failed with HTTP ${response.status}${suffix}`);
}

/** Turn fetch's opaque failures into something a human can act on. */
function describeNetworkFailure(error: unknown, url: string, timeoutMs: number): CliError {
  if (error instanceof Error && (error.name === "AbortError" || error.name === "TimeoutError")) {
    return new CliError(`Request to ${url} timed out after ${timeoutMs}ms.`, {
      hints: ["Raise the ceiling with --timeout <ms>, or retry."],
    });
  }
  const reason = error instanceof Error ? error.message : String(error);
  return new CliError(`Could not reach ${url}: ${reason}`, {
    hints: ["Check your network connection, or point elsewhere with --base-url."],
  });
}

async function send(url: string, init: RequestInit, timeoutMs: number): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...init, signal: controller.signal });
  } catch (error) {
    throw describeNetworkFailure(error, url, timeoutMs);
  } finally {
    clearTimeout(timer);
  }
}

export async function getJson<T>(ctx: RequestContext, path: string): Promise<T> {
  const url = `${ctx.baseUrl}${path}`;
  const response = await send(url, { headers: { accept: "application/json" } }, ctx.timeoutMs);
  if (!response.ok) throw await describeFailure(response, url);
  return (await response.json()) as T;
}

export async function postJson<T>(
  ctx: RequestContext,
  path: string,
  body: unknown,
  extraHeaders: Record<string, string> = {}
): Promise<T> {
  const url = `${ctx.baseUrl}${path}`;
  const response = await send(
    url,
    {
      method: "POST",
      headers: { "content-type": "application/json", accept: "application/json", ...extraHeaders },
      body: JSON.stringify(body),
    },
    ctx.timeoutMs
  );
  if (!response.ok) throw await describeFailure(response, url);
  return (await response.json()) as T;
}

/**
 * POST and stream the text body back chunk by chunk.
 *
 * `/api/chat` enforces a CSRF check that rejects any request without an
 * `Origin` header whose host matches the request host (verified 2026-08-21: a
 * bare POST returns HTTP 403 `{"error":"Forbidden","code":"forbidden"}`). We
 * send the base URL as the Origin so the CLI is a first-class caller rather
 * than a blocked one. Callers that only need one answer should use /ask.
 */
export async function postStream(
  ctx: RequestContext,
  path: string,
  body: unknown,
  onChunk: (text: string) => void
): Promise<void> {
  const url = `${ctx.baseUrl}${path}`;
  const response = await send(
    url,
    {
      method: "POST",
      headers: {
        "content-type": "application/json",
        accept: "text/plain",
        origin: ctx.baseUrl,
      },
      body: JSON.stringify(body),
    },
    ctx.timeoutMs
  );
  if (!response.ok) throw await describeFailure(response, url);
  if (!response.body) {
    onChunk(await response.text());
    return;
  }

  const decoder = new TextDecoder();
  const reader = response.body.getReader();
  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      if (value) onChunk(decoder.decode(value, { stream: true }));
    }
    const tail = decoder.decode();
    if (tail) onChunk(tail);
  } catch (error) {
    throw describeNetworkFailure(error, url, ctx.timeoutMs);
  }
}

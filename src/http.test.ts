import { afterEach, describe, expect, it, vi } from "vitest";
import { CliError } from "./errors.js";
import {
  DEFAULT_BASE_URL,
  getJson,
  postJson,
  postStream,
  resolveBaseUrl,
  summariseNonJsonBody,
  type RequestContext,
} from "./http.js";
import { jsonResponse, textStreamResponse } from "./test-helpers.js";

const ctx: RequestContext = { baseUrl: "https://yonyon.test", timeoutMs: 5000 };

afterEach(() => {
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
});

describe("resolveBaseUrl", () => {
  it("defaults to the production site", () => {
    expect(resolveBaseUrl(undefined)).toBe(DEFAULT_BASE_URL);
  });

  it("prefers the explicit flag over the environment variable", () => {
    vi.stubEnv("YONYON_BASE_URL", "https://from-env.test");
    expect(resolveBaseUrl("https://from-flag.test")).toBe("https://from-flag.test");
  });

  it("falls back to the environment variable", () => {
    vi.stubEnv("YONYON_BASE_URL", "https://from-env.test");
    expect(resolveBaseUrl(undefined)).toBe("https://from-env.test");
  });

  it("strips a trailing slash so paths do not double up", () => {
    expect(resolveBaseUrl("https://x.test/")).toBe("https://x.test");
  });

  it("keeps a path prefix for a proxied deployment", () => {
    expect(resolveBaseUrl("http://localhost:3000/base/")).toBe("http://localhost:3000/base");
  });

  it("rejects a value that is not a URL", () => {
    expect(() => resolveBaseUrl("notaurl")).toThrowError(/must be an absolute URL/);
  });

  it("rejects a non-http protocol", () => {
    expect(() => resolveBaseUrl("ftp://x.test")).toThrowError(/must be http or https/);
  });
});

describe("getJson", () => {
  it("requests the composed URL and returns the parsed body", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse({ total: 3 }));
    vi.stubGlobal("fetch", fetchMock);

    await expect(getJson(ctx, "/api/v1/projects")).resolves.toEqual({ total: 3 });
    expect(fetchMock.mock.calls[0]![0]).toBe("https://yonyon.test/api/v1/projects");
  });

  it("surfaces the API's own error message and code on a 4xx", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValue(
          jsonResponse(
            { error: "limit must be an integer between 1 and 50.", code: "invalid_limit" },
            { status: 400 }
          )
        )
    );

    await expect(getJson(ctx, "/api/v1/projects?limit=999")).rejects.toThrowError(
      /HTTP 400: limit must be an integer between 1 and 50\. \(invalid_limit\)/
    );
  });

  it("falls back to the bare status line when the body is unquotable markup", async () => {
    // Deliberately NOT echoing the HTML. A wrong --base-url lands on the site's
    // HTML 404 page, and pasting markup into the terminal hides the status.
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response("<html>oops</html>", { status: 502 }))
    );
    await expect(getJson(ctx, "/x")).rejects.toThrowError(/HTTP 502$/);
  });

  it("surfaces an HTML error page's title when it has one", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response("<!DOCTYPE html><html><head><title>404: Not Found</title></head></html>", {
          status: 404,
        })
      )
    );
    await expect(getJson(ctx, "/x")).rejects.toThrowError(/HTTP 404: 404: Not Found/);
  });

  it("keeps a plain-text error body", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response("upstream timeout", { status: 504 }))
    );
    await expect(getJson(ctx, "/x")).rejects.toThrowError(/HTTP 504: upstream timeout/);
  });

  it("reports a network failure with the URL and a hint", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("fetch failed")));
    const error = await getJson(ctx, "/x").catch((e: unknown) => e);
    expect(error).toBeInstanceOf(CliError);
    expect((error as CliError).message).toMatch(
      /Could not reach https:\/\/yonyon\.test\/x: fetch failed/
    );
    expect((error as CliError).hints.join(" ")).toMatch(/--base-url/);
  });

  it("reports a timeout as a timeout, with the ceiling that was hit", async () => {
    const abortError = new Error("The operation was aborted.");
    abortError.name = "AbortError";
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(abortError));

    const error = await getJson(ctx, "/x").catch((e: unknown) => e);
    expect((error as CliError).message).toMatch(/timed out after 5000ms/);
    expect((error as CliError).hints.join(" ")).toMatch(/--timeout/);
  });
});

describe("rate limiting", () => {
  it("explains a 429 in terms of the published rate limit and the retry delay", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        jsonResponse(
          { error: "Too many requests. Please try again later.", code: "rate_limited" },
          {
            status: 429,
            headers: {
              "retry-after": "43",
              "x-ratelimit-limit": "10",
              "x-ratelimit-remaining": "0",
            },
          }
        )
      )
    );

    const error = await postJson(ctx, "/ask", { query: "hi" }).catch((e: unknown) => e);
    expect(error).toBeInstanceOf(CliError);
    const cliError = error as CliError;
    expect(cliError.message).toBe(
      "Rate limited by yonyon.ai (10 requests per IP per minute). Retry in 43s."
    );
    expect(cliError.exitCode).toBe(1);
    expect(cliError.hints.join(" ")).toMatch(/shared per source IP/);
  });

  it("still names the documented ceiling when the headers are missing", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("", { status: 429 })));
    await expect(getJson(ctx, "/x")).rejects.toThrowError(
      /Rate limited by yonyon\.ai \(10 requests per IP per minute\)\.$/
    );
  });
});

describe("postJson", () => {
  it("sends the body as JSON with the right content type", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse({ answer: "ok" }));
    vi.stubGlobal("fetch", fetchMock);

    await postJson(ctx, "/ask", { query: "hi" });
    const init = fetchMock.mock.calls[0]![1] as RequestInit;
    expect(init.method).toBe("POST");
    expect(init.body).toBe('{"query":"hi"}');
    expect((init.headers as Record<string, string>)["content-type"]).toBe("application/json");
  });
});

describe("postStream", () => {
  it("sends an Origin header, because /api/chat rejects requests without one", async () => {
    const fetchMock = vi.fn().mockResolvedValue(textStreamResponse(["hi"]));
    vi.stubGlobal("fetch", fetchMock);

    await postStream(ctx, "/api/chat", { messages: [] }, () => {});
    const init = fetchMock.mock.calls[0]![1] as RequestInit;
    expect((init.headers as Record<string, string>)["origin"]).toBe("https://yonyon.test");
  });

  it("hands each chunk to the callback in order", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(textStreamResponse(["Hey", " there", "!"])));
    const chunks: string[] = [];
    await postStream(ctx, "/api/chat", { messages: [] }, (chunk) => chunks.push(chunk));
    expect(chunks.join("")).toBe("Hey there!");
  });

  it("reports the CSRF rejection instead of streaming an error page", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValue(jsonResponse({ error: "Forbidden", code: "forbidden" }, { status: 403 }))
    );
    await expect(postStream(ctx, "/api/chat", { messages: [] }, () => {})).rejects.toThrowError(
      /HTTP 403: Forbidden \(forbidden\)/
    );
  });

  it("still returns the text when the response has no readable stream", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("plain", { status: 200 })));
    const chunks: string[] = [];
    await postStream(ctx, "/api/chat", { messages: [] }, (chunk) => chunks.push(chunk));
    expect(chunks.join("")).toBe("plain");
  });
});

describe("summariseNonJsonBody", () => {
  it("returns the title for an HTML error page, not the markup", () => {
    const html =
      '<!DOCTYPE html><html lang="en"><head><title>404: Not Found</title>' +
      '<link rel="stylesheet" href="/_next/static/chunks/x.css"/></head><body>hi</body></html>';
    expect(summariseNonJsonBody(html)).toBe("404: Not Found");
  });

  it("returns nothing for markup with no title, rather than pasting HTML", () => {
    expect(summariseNonJsonBody("<!DOCTYPE html><html><body><div>x</div></body></html>")).toBe("");
  });

  it("never leaks a raw tag into the message", () => {
    const html = '<!DOCTYPE html><html><head><link rel="preload" as="script"/></head></html>';
    expect(summariseNonJsonBody(html)).not.toContain("<");
  });

  it("keeps a plain-text body, collapsed to one line", () => {
    expect(summariseNonJsonBody("Service\n  Unavailable\n")).toBe("Service Unavailable");
  });

  it("truncates a very long plain-text body", () => {
    const out = summariseNonJsonBody("x".repeat(500));
    expect(out.length).toBeLessThanOrEqual(203);
    expect(out.endsWith("...")).toBe(true);
  });

  it("returns empty for an empty body", () => {
    expect(summariseNonJsonBody("   \n ")).toBe("");
  });
});

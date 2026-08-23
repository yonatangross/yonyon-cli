import { afterEach, describe, expect, it, vi } from "vitest";
import { run, version } from "./cli.js";
import { jsonResponse, textStreamResponse, captureIo } from "./test-helpers.js";

afterEach(() => {
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
});

/** No test may reach the network; a bare call would be a bug in the test. */
function forbidNetwork(): void {
  vi.stubGlobal(
    "fetch",
    vi.fn(() => {
      throw new Error("the test made a real network call");
    })
  );
}

describe("top-level dispatch", () => {
  it("prints help and exits 0 for --help", async () => {
    forbidNetwork();
    const io = captureIo();
    await expect(run(["--help"], io)).resolves.toBe(0);
    expect(io.stdout()).toContain("Usage: yonyon <command> [options]");
  });

  it("prints help and exits 1 when called with no command", async () => {
    forbidNetwork();
    const io = captureIo();
    await expect(run([], io)).resolves.toBe(1);
    expect(io.stdout()).toContain("Commands:");
  });

  it("prints the package version for --version", async () => {
    const io = captureIo();
    await expect(run(["--version"], io)).resolves.toBe(0);
    expect(io.stdout().trim()).toBe(version());
    expect(io.stdout().trim()).toMatch(/^\d+\.\d+\.\d+/);
  });

  it("exits 2 and names the known commands on an unknown one", async () => {
    const io = captureIo();
    await expect(run(["frobnicate"], io)).resolves.toBe(2);
    expect(io.stderr()).toContain('Unknown command "frobnicate"');
    expect(io.stderr()).toContain("ask, projects, mcp, book, docs");
  });

  it("shows per-command help without hitting the network", async () => {
    forbidNetwork();
    const io = captureIo();
    await expect(run(["projects", "--help"], io)).resolves.toBe(0);
    expect(io.stdout()).toContain("Usage: yonyon projects");
  });

  it("exits 2 on a bad --base-url before any request is attempted", async () => {
    forbidNetwork();
    const io = captureIo();
    await expect(run(["projects", "--base-url", "notaurl"], io)).resolves.toBe(2);
    expect(io.stderr()).toContain("must be an absolute URL");
  });

  it("routes an unexpected non-CliError to exit 1 rather than crashing", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => {
        throw new RangeError("something structural");
      })
    );
    const io = captureIo();
    await expect(run(["projects"], io)).resolves.toBe(1);
    expect(io.stderr()).toContain("Could not reach");
  });
});

describe("ask", () => {
  it("strips a server-truncated FOLLOW_UPS marker rather than leaking it", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        jsonResponse({
          answer: 'OrchestKit handles retries.\n\n[FOLLOW_UPS: "What does it solve?" | "Ho',
        })
      )
    );
    const io = captureIo();
    await expect(run(["ask", "what?"], io)).resolves.toBe(0);
    expect(io.stdout()).not.toContain("FOLLOW_UPS");
    expect(io.stdout()).toContain("What does it solve?");
    expect(io.stdout()).not.toContain('| "Ho');
  });

  it("prints the answer text and splits out the follow-ups", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        jsonResponse({
          answer: 'Yonatan ships AI products.\n\n[FOLLOW_UPS: "What has he built?" | "Hire him?"]',
        })
      )
    );
    const io = captureIo();
    await expect(run(["ask", "What", "does", "he", "do?"], io)).resolves.toBe(0);
    expect(io.stdout()).toContain("Yonatan ships AI products.");
    expect(io.stdout()).toContain("Follow-ups you could ask:");
    expect(io.stdout()).toContain("What has he built?");
    expect(io.stdout()).not.toContain("[FOLLOW_UPS:");
  });

  it("joins the positionals into one query", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse({ answer: "ok" }));
    vi.stubGlobal("fetch", fetchMock);
    await run(["ask", "two", "words"], captureIo());
    const init = fetchMock.mock.calls[0]![1] as RequestInit;
    expect(init.body).toBe('{"query":"two words"}');
  });

  it("exits 2 when no question was given", async () => {
    forbidNetwork();
    const io = captureIo();
    await expect(run(["ask"], io)).resolves.toBe(2);
    expect(io.stderr()).toContain("needs a question");
  });

  it("prints raw JSON with --json", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse({ answer: "hi", query: "q" })));
    const io = captureIo();
    await run(["ask", "q", "--json"], io);
    expect(JSON.parse(io.stdout())).toEqual({ answer: "hi", query: "q" });
  });

  it("says so when the API returns no answer", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse({})));
    const io = captureIo();
    await expect(run(["ask", "q"], io)).resolves.toBe(0);
    expect(io.stdout()).toContain("no answer");
  });

  it("streams from /api/chat with --stream", async () => {
    const fetchMock = vi.fn().mockResolvedValue(textStreamResponse(["Hey", " there"]));
    vi.stubGlobal("fetch", fetchMock);
    const io = captureIo();
    await expect(run(["ask", "hi", "--stream"], io)).resolves.toBe(0);
    expect(fetchMock.mock.calls[0]![0]).toBe("https://yonyon.ai/api/chat");
    expect(io.stdout()).toBe("Hey there\n");
  });

  it("strips the FOLLOW_UPS trailer out of the stream as well", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValue(textStreamResponse(["Hey there.", "\n\n[FOLL", 'OW_UPS: "a" | "b"]']))
    );
    const io = captureIo();
    await run(["ask", "hi", "--stream"], io);
    expect(io.stdout()).toBe("Hey there.\n");
    expect(io.stdout()).not.toContain("FOLLOW_UPS");
  });

  it("surfaces a 429 with the rate limit explained", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        jsonResponse(
          { error: "Too many requests.", code: "rate_limited" },
          {
            status: 429,
            headers: { "retry-after": "12", "x-ratelimit-limit": "10" },
          }
        )
      )
    );
    const io = captureIo();
    await expect(run(["ask", "hi"], io)).resolves.toBe(1);
    expect(io.stderr()).toContain("Rate limited by yonyon.ai (10 requests per IP per minute)");
    expect(io.stderr()).toContain("Retry in 12s");
  });
});

describe("projects", () => {
  const payload = {
    count: 2,
    total: 3,
    nextCursor: "Mg",
    projects: [
      {
        name: "OrchestKit",
        desc: "Agent framework.",
        url: "https://yonyon.ai/projects/orchestkit",
      },
      {
        name: "Trading AI",
        desc: "LangGraph platform.",
        url: "https://yonyon.ai/projects/trading",
      },
    ],
  };

  it("renders a table with a header and one row per project", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(payload)));
    const io = captureIo();
    await expect(run(["projects"], io), "exit code").resolves.toBe(0);
    expect(io.stdout()).toContain("NAME");
    expect(io.stdout()).toContain("OrchestKit");
    expect(io.stdout()).toContain("https://yonyon.ai/projects/trading");
  });

  it("notes when the page is smaller than the total", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(payload)));
    const io = captureIo();
    await run(["projects"], io);
    expect(io.stdout()).toContain("Showing 2 of 3");
  });

  it("passes --limit through as a query parameter", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse(payload));
    vi.stubGlobal("fetch", fetchMock);
    await run(["projects", "--limit", "2"], captureIo());
    expect(fetchMock.mock.calls[0]![0]).toBe("https://yonyon.ai/api/v1/projects?limit=2");
  });

  it("rejects a limit outside the API's range before sending a request", async () => {
    forbidNetwork();
    const io = captureIo();
    await expect(run(["projects", "--limit", "999"], io)).resolves.toBe(2);
    expect(io.stderr()).toContain("must be between 1 and 50");
  });

  it("prints raw JSON with --json", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(payload)));
    const io = captureIo();
    await run(["projects", "--json"], io);
    expect(JSON.parse(io.stdout()).nextCursor).toBe("Mg");
  });

  it("handles an empty list without rendering an empty table", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(jsonResponse({ count: 0, total: 0, projects: [] }))
    );
    const io = captureIo();
    await run(["projects"], io);
    expect(io.stdout().trim()).toBe("No projects returned.");
  });

  it("honours --base-url so it can point at a local dev server", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse(payload));
    vi.stubGlobal("fetch", fetchMock);
    await run(["projects", "--base-url", "https://portfolio.localhost"], captureIo());
    expect(fetchMock.mock.calls[0]![0]).toBe("https://portfolio.localhost/api/v1/projects");
  });
});

describe("mcp", () => {
  it("prints the claude mcp add command and the .mcp.json block", async () => {
    forbidNetwork();
    const io = captureIo();
    await expect(run(["mcp"], io)).resolves.toBe(0);
    expect(io.stdout()).toContain(
      "claude mcp add --transport http yonyon https://yonyon.ai/api/mcp"
    );
    expect(io.stdout()).toContain('"mcpServers"');
  });

  it("emits only the config object with --json, so it can be redirected to a file", async () => {
    forbidNetwork();
    const io = captureIo();
    await run(["mcp", "--json"], io);
    expect(JSON.parse(io.stdout())).toEqual({
      mcpServers: { yonyon: { type: "http", url: "https://yonyon.ai/api/mcp" } },
    });
  });

  it("lists tool names and descriptions with --tools", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      jsonResponse({
        jsonrpc: "2.0",
        id: 1,
        result: {
          tools: [
            { name: "ask_yonatan", description: "Ask about Yonatan." },
            { name: "browse_projects", description: "List his projects." },
          ],
        },
      })
    );
    vi.stubGlobal("fetch", fetchMock);
    const io = captureIo();
    await expect(run(["mcp", "--tools"], io)).resolves.toBe(0);

    const init = fetchMock.mock.calls[0]![1] as RequestInit;
    expect(JSON.parse(init.body as string).method).toBe("tools/list");
    expect(io.stdout()).toContain("Tools (2):");
    expect(io.stdout()).toContain("ask_yonatan");
    expect(io.stdout()).toContain("Ask about Yonatan.");
  });

  it("reports a JSON-RPC error rather than pretending there are no tools", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(jsonResponse({ jsonrpc: "2.0", id: 1, error: { message: "boom" } }))
    );
    const io = captureIo();
    await run(["mcp", "--tools"], io);
    expect(io.stdout()).toContain("Tools unavailable: boom");
  });

  it("handles a server that reports zero tools", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse({ result: { tools: [] } })));
    const io = captureIo();
    await run(["mcp", "--tools"], io);
    expect(io.stdout()).toContain("no tools");
  });
});

describe("book", () => {
  it("prints the booking URL", async () => {
    forbidNetwork();
    const io = captureIo();
    await expect(run(["book", "--no-open"], io)).resolves.toBe(0);
    expect(io.stdout()).toContain("https://cal.com/yonyon");
    expect(io.stdout()).not.toContain("Opening it in your browser");
  });

  it("does not open a browser when stdout is not a terminal", async () => {
    forbidNetwork();
    const io = captureIo({ isTty: false });
    await run(["book"], io);
    expect(io.stdout()).toContain("Not a terminal");
  });

  it("prints JSON with --json", async () => {
    forbidNetwork();
    const io = captureIo();
    await run(["book", "--json"], io);
    expect(JSON.parse(io.stdout()).bookingUrl).toBe("https://cal.com/yonyon");
  });
});

describe("docs", () => {
  it("lists the discovery documents and the callable endpoints", async () => {
    forbidNetwork();
    const io = captureIo();
    await expect(run(["docs"], io)).resolves.toBe(0);
    expect(io.stdout()).toContain("https://yonyon.ai/llms.txt");
    expect(io.stdout()).toContain("https://yonyon.ai/.well-known/openapi.json");
    expect(io.stdout()).toContain("https://yonyon.ai/.well-known/agent-skills/index.json");
    expect(io.stdout()).toContain("https://yonyon.ai/api/mcp");
    expect(io.stdout()).toContain("https://cal.com/yonyon");
  });

  it("emits a machine-readable map with --json", async () => {
    forbidNetwork();
    const io = captureIo();
    await run(["docs", "--json"], io);
    const parsed = JSON.parse(io.stdout()) as {
      baseUrl: string;
      documents: { url: string }[];
      endpoints: { url: string }[];
    };
    expect(parsed.baseUrl).toBe("https://yonyon.ai");
    expect(parsed.documents.length).toBeGreaterThan(0);
    expect(parsed.endpoints.map((e) => e.url)).toContain("https://yonyon.ai/ask");
  });

  it("rewrites every URL when --base-url is given", async () => {
    forbidNetwork();
    const io = captureIo();
    await run(["docs", "--json", "--base-url", "http://localhost:3000"], io);
    const parsed = JSON.parse(io.stdout()) as { documents: { url: string }[] };
    expect(parsed.documents.every((d) => d.url.startsWith("http://localhost:3000"))).toBe(true);
  });
});

import { assertKnownFlags, boolFlag, type FlagValue } from "../args.js";
import { table } from "../format.js";
import { line, type Io } from "../io.js";

export const DOCS_HELP = `Usage: yonyon docs [options]

Print the discovery map: every machine-readable document an agent can read to
learn what yonyon.ai offers and how to call it.

Options:
  --json             Print the map as JSON.
  --base-url <url>   Point at another deployment (default: https://yonyon.ai).

Examples:
  yonyon docs
  yonyon docs --json`;

interface DocEntry {
  path: string;
  what: string;
}

/** Every path here was verified live against https://yonyon.ai on 2026-08-21. */
const ENTRIES: readonly DocEntry[] = [
  { path: "/llms.txt", what: "Short site summary written for LLMs" },
  { path: "/llms-full.txt", what: "Full bio, projects, services and FAQ" },
  { path: "/developers", what: "Human-readable API and MCP documentation" },
  { path: "/developers.md", what: "The same developer docs as markdown" },
  { path: "/.well-known/openapi.json", what: "OpenAPI 3.1 spec for the public HTTP API" },
  { path: "/.well-known/agent-skills/index.json", what: "Agent skills index" },
  { path: "/.well-known/mcp.json", what: "MCP server descriptor" },
  { path: "/auth.md", what: "Authentication notes (there is none, by design)" },
];

const ENDPOINTS: readonly DocEntry[] = [
  { path: "/ask", what: 'POST {"query":"..."} for a single-shot JSON answer' },
  { path: "/api/chat", what: 'POST {"messages":[...]} for a streaming reply' },
  { path: "/api/v1/projects", what: "GET the portfolio projects, cursor paginated" },
  { path: "/api/mcp", what: "JSON-RPC 2.0 Streamable HTTP MCP server" },
];

export function docsCommand(flags: ReadonlyMap<string, FlagValue>, baseUrl: string, io: Io): void {
  assertKnownFlags(flags, ["json"], "docs");

  const absolute = (entries: readonly DocEntry[]) =>
    entries.map((entry) => ({ url: `${baseUrl}${entry.path}`, what: entry.what }));

  if (boolFlag(flags, "json")) {
    line(
      io,
      JSON.stringify(
        {
          baseUrl,
          documents: absolute(ENTRIES),
          endpoints: absolute(ENDPOINTS),
          booking: "https://cal.com/yonyon",
          rateLimit: "10 requests per IP per minute, unauthenticated",
        },
        null,
        2
      )
    );
    return;
  }

  line(io, "Discovery documents");
  line(
    io,
    table(
      ["URL", "WHAT IT IS"],
      absolute(ENTRIES).map((e) => [e.url, e.what]),
      {
        shrinkable: [1],
      }
    )
  );
  line(io);
  line(io, "Callable endpoints");
  line(
    io,
    table(
      ["URL", "HOW TO CALL IT"],
      absolute(ENDPOINTS).map((e) => [e.url, e.what]),
      {
        shrinkable: [1],
      }
    )
  );
  line(io);
  line(io, "Booking: https://cal.com/yonyon");
  line(io, "Rate limit: 10 requests per IP per minute. No API key, no OAuth.");
}

# yonyon

Command line client for the public [yonyon.ai](https://yonyon.ai) agent API.

Ask the site's agent a question, list the portfolio projects, wire up the MCP server, or grab the
booking link, without writing an HTTP integration first.

The API is public and unauthenticated. There is no key to set, no config file to write, and no login
step. The only constraint is rate: **10 requests per IP per minute**, shared across every endpoint.

## Install

Run it without installing anything:

```bash
npx yonyon ask "What has Yonatan built with MCP?"
```

Or install it globally:

```bash
npm install -g yonyon
yonyon --help
```

Requires Node.js 24 or newer.

## Commands

### `yonyon ask "<question>"`

Ask the agent about Yonatan Gross, his projects, or his services. The default path is `POST /ask`,
the single-shot endpoint built for server-side callers.

```console
$ yonyon ask "What is OrchestKit?"
OrchestKit is an open-source Claude Code agent framework with 100+ skills,
35+ agents, and 200+ hooks.

Follow-ups you could ask:
  What else has he built?
  Is he available for consulting?
```

Add `--stream` to use `POST /api/chat` instead and print tokens as they arrive. Add `--json` to get
the raw `/ask` response body.

```bash
yonyon ask "Is he available for consulting?" --stream
yonyon ask "List his projects" --json
```

### `yonyon projects [--limit N] [--json]`

List the portfolio projects from `GET /api/v1/projects`.

```console
$ yonyon projects --limit 2
NAME                  DESCRIPTION                                    URL
--------------------  ---------------------------------------------  ------------------------------------------------
OrchestKit            Open-source Claude Code agent framework.       https://yonyon.ai/projects/orchestkit
AI Operations Platfo  Production WhatsApp AI (RAG), commerce, cont…  https://yonyon.ai/projects/ai-operations-platform
```

`--limit` accepts 1 to 50, the range the API itself enforces. Use `--json` for the raw body, which
also carries `total` and `nextCursor` for pagination.

```bash
yonyon projects --json
```

### `yonyon mcp [--tools] [--json]`

Print ready-to-paste MCP client configuration for the yonyon.ai MCP server, a JSON-RPC 2.0
Streamable HTTP endpoint that needs no auth.

```console
$ yonyon mcp
MCP endpoint: https://yonyon.ai/api/mcp
Transport: Streamable HTTP. Authentication: none.

Add it to Claude Code:
  claude mcp add --transport http yonyon https://yonyon.ai/api/mcp

Or add this to .mcp.json:
{
  "mcpServers": {
    "yonyon": {
      "type": "http",
      "url": "https://yonyon.ai/api/mcp"
    }
  }
}
```

`--tools` queries `tools/list` live and prints each tool with its description. `--json` prints only
the config object, so it can be redirected into a file.

```bash
yonyon mcp --tools
yonyon mcp --json > .mcp.json
```

### `yonyon book [--no-open]`

Print the link for a free 15-minute intro call, and open it in the default browser.

```console
$ yonyon book
Book a free 15-minute intro call: https://cal.com/yonyon
Opening it in your browser.
```

The browser is only opened when stdout is a terminal, so piping the command never launches anything.
Pass `--no-open` to suppress it explicitly.

```bash
yonyon book --no-open
```

### `yonyon docs [--json]`

Print the discovery map: every machine-readable document an agent can read to learn what the site
offers and how to call it.

```console
$ yonyon docs
Discovery documents
URL                                                 WHAT IT IS
--------------------------------------------------  ------------------------------------------------
https://yonyon.ai/llms.txt                          Short site summary written for LLMs
https://yonyon.ai/llms-full.txt                     Full bio, projects, services and FAQ
https://yonyon.ai/developers                        Human-readable API and MCP documentation
...
```

```bash
yonyon docs --json
```

## Global options

| Option             | Meaning                                                                                                    |
| ------------------ | ---------------------------------------------------------------------------------------------------------- |
| `-h`, `--help`     | Show help. Works per command too: `yonyon ask --help`.                                                     |
| `-v`, `--version`  | Print the CLI version.                                                                                     |
| `--base-url <url>` | Target another deployment. Defaults to `https://yonyon.ai`, or the `YONYON_BASE_URL` environment variable. |
| `--timeout <ms>`   | Per-request timeout. Defaults to 60000 for `ask` and 15000 elsewhere.                                      |
| `--json`           | Machine-readable output, on the commands that support it.                                                  |

Point it at a local dev server:

```bash
yonyon projects --base-url https://portfolio.localhost
```

## Exit codes

| Code | Meaning                                                                   |
| ---- | ------------------------------------------------------------------------- |
| `0`  | Success.                                                                  |
| `1`  | The request failed: network error, timeout, non-2xx response, rate limit. |
| `2`  | A usage mistake: unknown command, unknown flag, missing or invalid value. |

Rate limiting gets its own message rather than a bare HTTP 429:

```console
$ yonyon ask "hello"
yonyon: Rate limited by yonyon.ai (10 requests per IP per minute). Retry in 43s.
  The public API is unauthenticated, so the budget is shared per source IP.
  Wait for the window to reset and run the command again.
```

## Development

```bash
pnpm install
pnpm test          # vitest, network fully mocked
pnpm exec tsc --noEmit
pnpm run build     # emits dist/
node dist/index.js --help
```

The CLI has zero runtime dependencies. Argument parsing is hand-rolled, which is smaller than any
parser library at this command count.

## License

MIT. See [LICENSE](./LICENSE).

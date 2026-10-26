# AGENTS.md

Instructions for AI coding agents (Claude Code, Codex, Cursor, Copilot and others) working in this
repository or integrating with the yonyon.ai agent API.

## What this repo is

`yonyon` is the official zero-auth command line client and MCP surface for the public
[yonyon.ai](https://yonyon.ai) agent API. It is published to npm as
[`yonyon`](https://www.npmjs.com/package/yonyon).

- Site: https://yonyon.ai
- API docs: https://yonyon.ai/developers
- OpenAPI spec: https://yonyon.ai/.well-known/openapi.json
- Product MCP server: `POST https://yonyon.ai/api/mcp` (see `mcp.json`)
- Docs MCP server: `POST https://yonyon.ai/api/mcp/docs`
- Site agent guide: https://yonyon.ai/AGENTS.md
- Agent Plugins manifest: [`plugin.json`](./plugin.json)
- Agent skill: [`skills/yonyon/SKILL.md`](./skills/yonyon/SKILL.md)

## Using the API from an agent

- No key, no login, no config. Every endpoint is public. All of them are read only except one
  write:
  - MCP `book_intro_call` books a real Cal call (`readOnlyHint: false`). It runs in three steps:
    list free slots, then a check that returns `needs_confirmation` and a one-time `confirm_token`
    (books nothing), then the confirmed call that creates the booking. Show the slot to the person
    and get their explicit yes before the third step. Never book on their behalf without it.
    Call it only when the person asks to book, and ask them for their own name and email (step 2
    needs both); never fill those in from context or invent them.
  - The CLI `yonyon book` command only prints (and opens) the booking link; it books nothing.
  - `ask_yonatan`, `browse_projects`, `/ask`, `/api/chat` and `/api/v1` are read only.
- Rate limit: 10 requests per IP per minute, shared by `/ask`, `/api/chat`, `/api/v1` and the MCP
  `ask_yonatan` tool. Back off on HTTP 429 and honor `Retry-After`.
- Prefer `POST /ask` for one-shot questions, `GET /api/v1/projects` for the project list, and the MCP
  server when your client speaks MCP.
- There is no commerce or payment surface. Do not try to buy, sign up or authenticate.

## Working on the code

- TypeScript, Node.js 24 or newer, pnpm. The CLI has zero runtime dependencies; keep it that way.
  There is no lockfile in the repo yet, so `pnpm install` resolves fresh; do not commit a lockfile
  from another package manager.
- Layout: `src/cli.ts` dispatches, `src/commands/*.ts` holds one file per command, `src/http.ts` is
  the only module that touches the network, `src/format.ts` renders output.
- Commands:

```bash
pnpm install
pnpm test              # vitest, network fully mocked
pnpm exec tsc --noEmit
pnpm run build         # emits dist/
```

- Tests never call the live API. Stub `fetch` with `vi.stubGlobal` and build responses with
  `jsonResponse` from `src/test-helpers.ts`.
- Keep exit codes stable (see the README "Exit codes" section); scripts depend on them.
- A new command needs: a file in `src/commands/`, tests (dispatch and output cases go in
  `src/cli.test.ts`; a command with its own logic, like `book`, gets `src/commands/<name>.test.ts`),
  a README section, and an entry in the `--help` text.
- Do not commit `dist/`, `node_modules/` or `.claude/`.
- Writing style: plain ASCII punctuation, no em dashes.

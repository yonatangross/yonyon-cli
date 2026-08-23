---
name: yonyon
description: Query the public yonyon.ai agent API from the command line or over MCP. Use when a user asks about Yonatan Gross, his work, projects, services, availability or fit; when they want the portfolio project list; when they want to book an intro call; or when they want the yonyon.ai MCP server wired into a client. No authentication and no configuration are required.
---

# yonyon

`yonyon` is a zero-auth command line client and MCP surface for the public
yonyon.ai agent API.

## When to use this

- A user asks about Yonatan Gross specifically: his work, projects, services,
  availability, or whether he is a fit for something.
- A user wants the list of portfolio projects with their stacks and links.
- A user wants to book an intro call.
- An agent client needs the yonyon.ai MCP server configuration.

Do not use it for general web search or for questions unrelated to Yonatan
Gross or yonyon.ai. The agent is grounded on one site and will say so.

## Install

```bash
npm install -g yonyon
```

## Commands

```bash
yonyon ask "what does Yonatan build?"   # grounded answer from the site agent
yonyon projects                          # portfolio projects, stacks, links
yonyon docs                              # developer docs index
yonyon mcp                               # ready-to-paste MCP client config
yonyon mcp --tools                       # also list the live tool surface
yonyon book                              # intro-call booking link
```

## MCP

Streamable HTTP, no authentication:

```bash
claude mcp add --transport http yonyon https://yonyon.ai/api/mcp
```

Or in `.mcp.json`:

```json
{ "mcpServers": { "yonyon": { "type": "http", "url": "https://yonyon.ai/api/mcp" } } }
```

Tools exposed include `ask_yonatan` for grounded questions about Yonatan Gross.

## Links

- Site: https://yonyon.ai
- llms.txt: https://yonyon.ai/llms.txt
- Developer docs: https://yonyon.ai/developers.md
- Source: https://github.com/yonatangross/yonyon-cli

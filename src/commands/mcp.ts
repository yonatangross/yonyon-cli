import { assertKnownFlags, boolFlag, type FlagValue } from "../args.js";
import { postJson, type RequestContext } from "../http.js";
import { line, type Io } from "../io.js";

interface McpTool {
  name?: string;
  description?: string;
}

interface ToolsListResponse {
  result?: { tools?: McpTool[] };
  error?: { message?: string };
}

export const MCP_HELP = `Usage: yonyon mcp [options]

Print ready-to-paste client configuration for the yonyon.ai MCP server, a
JSON-RPC 2.0 Streamable HTTP endpoint that needs no auth.

Options:
  --tools            Also query tools/list live and print each tool name
                     with its description.
  --json             Print only the .mcp.json block, for piping into a file.
  --base-url <url>   Point at another deployment (default: https://yonyon.ai).
  --timeout <ms>     Per-request timeout (default: 15000).

Examples:
  yonyon mcp
  yonyon mcp --tools
  yonyon mcp --json > .mcp.json`;

function configBlock(endpoint: string): string {
  return JSON.stringify({ mcpServers: { yonyon: { type: "http", url: endpoint } } }, null, 2);
}

export async function mcpCommand(
  flags: ReadonlyMap<string, FlagValue>,
  ctx: RequestContext,
  io: Io
): Promise<void> {
  assertKnownFlags(flags, ["tools", "json"], "mcp");

  const endpoint = `${ctx.baseUrl}/api/mcp`;

  if (boolFlag(flags, "json")) {
    line(io, configBlock(endpoint));
    return;
  }

  line(io, `MCP endpoint: ${endpoint}`);
  line(io, "Transport: Streamable HTTP. Authentication: none.");
  line(io);
  line(io, "Add it to Claude Code:");
  line(io, `  claude mcp add --transport http yonyon ${endpoint}`);
  line(io);
  line(io, "Or add this to .mcp.json:");
  line(io, configBlock(endpoint));

  if (!boolFlag(flags, "tools")) {
    line(io);
    line(io, "Run 'yonyon mcp --tools' to list the tools the server exposes.");
    return;
  }

  const response = await postJson<ToolsListResponse>(
    ctx,
    "/api/mcp",
    { jsonrpc: "2.0", id: 1, method: "tools/list", params: {} },
    { accept: "application/json, text/event-stream" }
  );

  line(io);
  if (response.error) {
    line(
      io,
      `Tools unavailable: ${response.error.message ?? "the server returned a JSON-RPC error."}`
    );
    return;
  }

  const tools = response.result?.tools ?? [];
  if (tools.length === 0) {
    line(io, "The server reported no tools.");
    return;
  }

  line(io, `Tools (${tools.length}):`);
  for (const tool of tools) {
    line(io, `  ${tool.name ?? "(unnamed)"}`);
    if (tool.description) line(io, `      ${tool.description}`);
  }
}

import { createRequire } from "node:module";
import { assertKnownFlags, boolFlag, intFlag, parseArgs, stringFlag } from "./args.js";
import { askCommand, ASK_HELP } from "./commands/ask.js";
import { bookCommand, BOOK_HELP } from "./commands/book.js";
import { docsCommand, DOCS_HELP } from "./commands/docs.js";
import { mcpCommand, MCP_HELP } from "./commands/mcp.js";
import { projectsCommand, PROJECTS_HELP } from "./commands/projects.js";
import { CliError, usageError } from "./errors.js";
import { FAST_TIMEOUT_MS, resolveBaseUrl, SLOW_TIMEOUT_MS, type RequestContext } from "./http.js";
import { line, processIo, type Io } from "./io.js";

const require = createRequire(import.meta.url);

export function version(): string {
  const pkg = require("../package.json") as { version?: string };
  return pkg.version ?? "0.0.0";
}

const HELP = `yonyon - command line client for the public yonyon.ai agent API.

Usage: yonyon <command> [options]

Commands:
  ask "<question>"   Ask the agent about Yonatan, his projects or his services
  projects           List the portfolio projects
  mcp                Print MCP client config, or list the server's tools
  book               Print (and open) the intro-call booking link
  docs               Print the machine-readable discovery map

Global options:
  -h, --help         Show help. Works per command too: yonyon ask --help
  -v, --version      Print the CLI version
  --base-url <url>   Target another deployment (default: https://yonyon.ai,
                     or the YONYON_BASE_URL environment variable)
  --timeout <ms>     Per-request timeout in milliseconds
  --json             Machine-readable output, where the command supports it

The API is public and unauthenticated. There is nothing to configure and no
key to set. It is rate limited to 10 requests per IP per minute.

Examples:
  yonyon ask "What has Yonatan built with MCP?"
  yonyon projects --limit 3
  yonyon mcp --tools
  yonyon docs --json`;

const COMMAND_HELP: Record<string, string> = {
  ask: ASK_HELP,
  projects: PROJECTS_HELP,
  mcp: MCP_HELP,
  book: BOOK_HELP,
  docs: DOCS_HELP,
};

/** Commands whose backend is an LLM get the roomier timeout. */
const SLOW_COMMANDS = new Set(["ask"]);

export async function run(argv: readonly string[], io: Io = processIo): Promise<number> {
  try {
    const { command, positionals, flags } = parseArgs(argv);

    if (boolFlag(flags, "version") && !command) {
      line(io, version());
      return 0;
    }

    if (!command) {
      line(io, HELP);
      return boolFlag(flags, "help") ? 0 : 1;
    }

    const help = COMMAND_HELP[command];
    if (help === undefined) {
      throw usageError(`Unknown command "${command}".`, [
        `Known commands: ${Object.keys(COMMAND_HELP).join(", ")}.`,
        'Run "yonyon --help" for usage.',
      ]);
    }

    if (boolFlag(flags, "help")) {
      line(io, help);
      return 0;
    }

    const baseUrl = resolveBaseUrl(stringFlag(flags, "base-url"));
    const timeoutMs =
      intFlag(flags, "timeout", { min: 1, max: 600_000 }) ??
      (SLOW_COMMANDS.has(command) ? SLOW_TIMEOUT_MS : FAST_TIMEOUT_MS);
    const ctx: RequestContext = { baseUrl, timeoutMs };

    switch (command) {
      case "ask":
        await askCommand(positionals, flags, ctx, io);
        break;
      case "projects":
        await projectsCommand(flags, ctx, io);
        break;
      case "mcp":
        await mcpCommand(flags, ctx, io);
        break;
      case "book":
        assertKnownFlags(flags, ["open", "json"], "book");
        bookCommand(flags, io);
        break;
      case "docs":
        docsCommand(flags, baseUrl, io);
        break;
      /* c8 ignore next 2 */
      default:
        throw usageError(`Unknown command "${command}".`);
    }
    return 0;
  } catch (error) {
    if (error instanceof CliError) {
      io.err(`yonyon: ${error.message}\n`);
      for (const hint of error.hints) io.err(`  ${hint}\n`);
      return error.exitCode;
    }
    const message = error instanceof Error ? error.message : String(error);
    io.err(`yonyon: unexpected error: ${message}\n`);
    return 1;
  }
}

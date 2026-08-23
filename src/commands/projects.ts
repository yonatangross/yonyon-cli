import { assertKnownFlags, boolFlag, intFlag, type FlagValue } from "../args.js";
import { table, truncate } from "../format.js";
import { getJson, type RequestContext } from "../http.js";
import { line, type Io } from "../io.js";

interface Project {
  name?: string;
  desc?: string;
  url?: string;
}

interface ProjectsResponse {
  count?: number;
  total?: number;
  nextCursor?: string | null;
  projects?: Project[];
}

/** The API rejects anything outside this range with HTTP 400 invalid_limit. */
const LIMIT_RANGE = { min: 1, max: 50 };

export const PROJECTS_HELP = `Usage: yonyon projects [options]

List the portfolio projects published at GET /api/v1/projects.

Options:
  --limit <n>        Return at most n projects (1-50). Default: all.
  --json             Print the raw JSON response, including nextCursor.
  --base-url <url>   Point at another deployment (default: https://yonyon.ai).
  --timeout <ms>     Per-request timeout (default: 15000).

Examples:
  yonyon projects
  yonyon projects --limit 2
  yonyon projects --json`;

export async function projectsCommand(
  flags: ReadonlyMap<string, FlagValue>,
  ctx: RequestContext,
  io: Io
): Promise<void> {
  assertKnownFlags(flags, ["limit", "json"], "projects");

  const limit = intFlag(flags, "limit", LIMIT_RANGE);
  const query = limit === undefined ? "" : `?limit=${limit}`;
  const response = await getJson<ProjectsResponse>(ctx, `/api/v1/projects${query}`);

  if (boolFlag(flags, "json")) {
    line(io, JSON.stringify(response, null, 2));
    return;
  }

  const projects = response.projects ?? [];
  if (projects.length === 0) {
    line(io, "No projects returned.");
    return;
  }

  const rows = projects.map((project) => [
    project.name ?? "",
    truncate(project.desc ?? "", 60),
    project.url ?? "",
  ]);
  line(io, table(["NAME", "DESCRIPTION", "URL"], rows, { shrinkable: [1] }));

  const total = response.total;
  if (typeof total === "number" && projects.length < total) {
    line(io);
    line(io, `Showing ${projects.length} of ${total}. Use --limit or --json for the cursor.`);
  }
}

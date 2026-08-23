import { assertKnownFlags, boolFlag, type FlagValue } from "../args.js";
import { usageError } from "../errors.js";
import { createTrailerStripper, splitFollowUps } from "../format.js";
import { postJson, postStream, type RequestContext } from "../http.js";
import { line, type Io } from "../io.js";

interface AskResponse {
  answer?: string;
  query?: string;
}

export const ASK_HELP = `Usage: yonyon ask "<question>" [options]

Ask the yonyon.ai agent a question about Yonatan Gross, his projects, or his
services. Answers come from POST /ask, the single-shot endpoint built for
server-side callers.

Options:
  --stream           Use the multi-turn POST /api/chat endpoint and print
                     tokens as they arrive, instead of one-shot /ask.
  --json             Print the raw JSON response. Ignored with --stream,
                     which has no JSON representation.
  --base-url <url>   Point at another deployment (default: https://yonyon.ai).
  --timeout <ms>     Per-request timeout (default: 60000).

Examples:
  yonyon ask "What has Yonatan built with MCP?"
  yonyon ask "Is he available for consulting?" --stream
  yonyon ask "List his projects" --json`;

export async function askCommand(
  positionals: readonly string[],
  flags: ReadonlyMap<string, FlagValue>,
  ctx: RequestContext,
  io: Io
): Promise<void> {
  assertKnownFlags(flags, ["stream", "json"], "ask");

  const question = positionals.join(" ").trim();
  if (!question) {
    throw usageError('yonyon ask needs a question, for example: yonyon ask "What is OrchestKit?"');
  }

  if (boolFlag(flags, "stream")) {
    // The streamed reply carries the same FOLLOW_UPS trailer as /ask, so strip
    // it on the way through rather than printing a marker meant for the web UI.
    const stripper = createTrailerStripper();
    let printed = "";
    await postStream(
      ctx,
      "/api/chat",
      { messages: [{ role: "user", content: question }] },
      (chunk) => {
        const text = stripper.push(chunk);
        if (text) {
          printed += text;
          io.out(text);
        }
      }
    );
    const tail = stripper.flush();
    if (tail) {
      printed += tail;
      io.out(tail);
    }
    if (!printed.endsWith("\n")) io.out("\n");
    return;
  }

  const response = await postJson<AskResponse>(ctx, "/ask", { query: question });

  if (boolFlag(flags, "json")) {
    line(io, JSON.stringify(response, null, 2));
    return;
  }

  const answer = typeof response.answer === "string" ? response.answer : "";
  if (!answer) {
    line(io, "The API returned no answer for that question.");
    return;
  }

  const { text, followUps } = splitFollowUps(answer);
  line(io, text);
  if (followUps.length > 0) {
    line(io);
    line(io, "Follow-ups you could ask:");
    for (const followUp of followUps) line(io, `  ${followUp}`);
  }
}

/** Column widths are derived from the data, then clamped to the terminal. */
const MIN_COLUMN = 8;

export function terminalWidth(fallback = 100): number {
  const columns = process.stdout.columns;
  return typeof columns === "number" && columns > 20 ? columns : fallback;
}

export function truncate(value: string, max: number): string {
  if (max <= 1) return value.slice(0, Math.max(0, max));
  return value.length <= max ? value : `${value.slice(0, max - 1)}…`;
}

/**
 * Render rows as a plain aligned table. No box drawing: the output is meant to
 * survive a pipe into grep or awk.
 *
 * `shrinkable` names the columns that may be truncated when the line does not
 * fit the terminal. Columns left out are printed whole, which is what a URL
 * column needs: a truncated link is worse than a wrapped one.
 */
export function table(
  headers: readonly string[],
  rows: readonly (readonly string[])[],
  options: { shrinkable?: readonly number[] } = {}
): string {
  if (rows.length === 0) return "";

  const widths = headers.map((header, index) =>
    Math.max(header.length, ...rows.map((row) => (row[index] ?? "").length))
  );
  const shrinkable = options.shrinkable ?? headers.map((_, index) => index);

  // Shrink the widest shrinkable column until the whole line fits the terminal.
  const gutter = 2;
  const budget = terminalWidth() - gutter * (headers.length - 1);
  let total = widths.reduce((sum, width) => sum + width, 0);
  while (total > budget) {
    let widest = -1;
    for (const index of shrinkable) {
      if (widths[index]! <= MIN_COLUMN) continue;
      if (widest === -1 || widths[index]! > widths[widest]!) widest = index;
    }
    if (widest === -1) break;
    widths[widest] = widths[widest]! - 1;
    total -= 1;
  }

  const line = (cells: readonly string[]): string =>
    cells
      .map((cell, index) => truncate(cell, widths[index]!).padEnd(widths[index]!))
      .join(" ".repeat(gutter))
      .trimEnd();

  return [line(headers), line(widths.map((width) => "-".repeat(width))), ...rows.map(line)].join(
    "\n"
  );
}

export const FOLLOW_UP_MARKER = "[FOLLOW_UPS:";

/**
 * The /ask answer carries a trailing `[FOLLOW_UPS: "a" | "b"]` marker meant for
 * the site chat UI. Split it off so stdout stays readable prose.
 *
 * The closing bracket is optional on purpose: the API truncates `answer` to a
 * fixed length, so a long reply arrives with the marker cut off mid-word and no
 * `]` at all (verified against production 2026-08-21). Anchoring on the bracket
 * would leak the fragment into the output in exactly the common case.
 */
export function splitFollowUps(answer: string): { text: string; followUps: string[] } {
  const index = answer.indexOf(FOLLOW_UP_MARKER);
  if (index === -1) return { text: answer.trim(), followUps: [] };

  const rest = answer.slice(index + FOLLOW_UP_MARKER.length);
  const close = rest.indexOf("]");
  const body = close === -1 ? rest : rest.slice(0, close);

  const followUps = body
    .split("|")
    .map((entry) => entry.trim().replace(/^"|"$/g, "").trim())
    // A truncated marker ends in a partial, unquoted entry. Keeping it would
    // print half a sentence as if it were a real suggestion.
    .filter((entry, position, all) => {
      if (entry.length === 0) return false;
      const isLast = position === all.length - 1;
      return !(isLast && close === -1);
    });

  return { text: answer.slice(0, index).trim(), followUps };
}

/**
 * Streaming counterpart: /api/chat emits the same marker, but a chunk boundary
 * can fall inside it. This holds back any tail that could still turn out to be
 * the start of the marker, so the filter never emits a partial `[FOLLOW`.
 */
export function createTrailerStripper(): { push(chunk: string): string; flush(): string } {
  let held = "";
  let finished = false;

  return {
    push(chunk: string): string {
      if (finished) return "";
      held += chunk;

      const index = held.indexOf(FOLLOW_UP_MARKER);
      if (index !== -1) {
        // Nothing more will be emitted, so the blank line that separated the
        // prose from the marker would just be trailing whitespace. Drop it, to
        // match what splitFollowUps does on the non-streaming path.
        const emitted = held.slice(0, index).replace(/\s+$/, "");
        held = "";
        finished = true;
        return emitted;
      }

      // Longest suffix of the buffer that is also a prefix of the marker.
      let keep = 0;
      const max = Math.min(held.length, FOLLOW_UP_MARKER.length - 1);
      for (let size = max; size > 0; size--) {
        if (held.endsWith(FOLLOW_UP_MARKER.slice(0, size))) {
          keep = size;
          break;
        }
      }

      let holdFrom = held.length - keep;
      // Hold the whitespace in front of a candidate marker too. If it does turn
      // out to be the marker, that whitespace is the blank line separating the
      // prose from it, and by then it is too late to unprint.
      if (keep > 0) {
        while (holdFrom > 0 && /\s/.test(held[holdFrom - 1]!)) holdFrom--;
      }

      const emitted = held.slice(0, holdFrom);
      held = held.slice(holdFrom);
      return emitted;
    },
    flush(): string {
      if (finished) return "";
      const remaining = held;
      held = "";
      finished = true;
      return remaining;
    },
  };
}

export function indentList(items: readonly string[]): string {
  return items.map((item) => `  - ${item}`).join("\n");
}

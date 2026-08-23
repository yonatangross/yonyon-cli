import { spawn } from "node:child_process";
import { assertKnownFlags, boolFlag, enabledUnlessNegated, type FlagValue } from "../args.js";
import { line, type Io } from "../io.js";

export const BOOKING_URL = "https://cal.com/yonyon";

export const BOOK_HELP = `Usage: yonyon book [options]

Print the booking link for a free 15-minute intro call, and open it in the
default browser when stdout is a terminal.

Options:
  --no-open          Print the URL without opening a browser. Opening is also
                     skipped automatically when stdout is not a TTY.
  --json             Print the booking URL as JSON.

Examples:
  yonyon book
  yonyon book --no-open`;

/** Platform-appropriate opener. Detached and unref'd so we never block exit. */
export function openInBrowser(url: string): void {
  const command =
    process.platform === "darwin" ? "open" : process.platform === "win32" ? "start" : "xdg-open";
  const args = process.platform === "win32" ? ["", url] : [url];
  try {
    const child = spawn(command, args, {
      stdio: "ignore",
      detached: true,
      shell: process.platform === "win32",
    });
    // A missing opener must not crash the command; the URL is already printed.
    child.on("error", () => {});
    child.unref();
  } catch {
    // Same reasoning: printing the URL is the contract, opening is a bonus.
  }
}

export function bookCommand(
  flags: ReadonlyMap<string, FlagValue>,
  io: Io,
  open: (url: string) => void = openInBrowser
): void {
  assertKnownFlags(flags, ["open", "json"], "book");

  if (boolFlag(flags, "json")) {
    line(
      io,
      JSON.stringify({ bookingUrl: BOOKING_URL, durationMinutes: 15, price: "free" }, null, 2)
    );
    return;
  }

  line(io, `Book a free 15-minute intro call: ${BOOKING_URL}`);

  const wanted = enabledUnlessNegated(flags, "open");
  if (!wanted) return;
  if (!io.isTty) {
    line(io, "(Not a terminal, so the browser was not opened. Use the link above.)");
    return;
  }
  open(BOOKING_URL);
  line(io, "Opening it in your browser.");
}

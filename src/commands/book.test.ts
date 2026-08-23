import { describe, expect, it, vi } from "vitest";
import { BOOKING_URL, bookCommand } from "./book.js";
import { captureIo } from "../test-helpers.js";

describe("bookCommand browser opening", () => {
  it("opens the booking URL when stdout is a terminal", () => {
    const open = vi.fn();
    const io = captureIo({ isTty: true });
    bookCommand(new Map(), io, open);
    expect(open).toHaveBeenCalledWith(BOOKING_URL);
    expect(io.stdout()).toContain("Opening it in your browser.");
  });

  it("does not open when --no-open was passed, even on a terminal", () => {
    const open = vi.fn();
    const io = captureIo({ isTty: true });
    bookCommand(new Map([["open", false]]), io, open);
    expect(open).not.toHaveBeenCalled();
  });

  it("does not open when stdout is piped", () => {
    const open = vi.fn();
    bookCommand(new Map(), captureIo({ isTty: false }), open);
    expect(open).not.toHaveBeenCalled();
  });

  it("skips opening for --json so the output stays parseable", () => {
    const open = vi.fn();
    const io = captureIo({ isTty: true });
    bookCommand(new Map([["json", true]]), io, open);
    expect(open).not.toHaveBeenCalled();
    expect(() => JSON.parse(io.stdout())).not.toThrow();
  });
});

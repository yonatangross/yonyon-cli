import { describe, expect, it } from "vitest";
import { createTrailerStripper, indentList, splitFollowUps, table, truncate } from "./format.js";

describe("truncate", () => {
  it("leaves a short value alone", () => {
    expect(truncate("hello", 10)).toBe("hello");
  });

  it("marks a clipped value with an ellipsis and respects the budget", () => {
    expect(truncate("abcdefghij", 5)).toBe("abcd…");
    expect(truncate("abcdefghij", 5)).toHaveLength(5);
  });

  it("degrades safely at a zero or one character budget", () => {
    expect(truncate("abc", 1)).toBe("a");
    expect(truncate("abc", 0)).toBe("");
  });
});

describe("table", () => {
  it("returns an empty string for no rows", () => {
    expect(table(["A"], [])).toBe("");
  });

  it("aligns columns and underlines the header", () => {
    const rendered = table(
      ["NAME", "URL"],
      [
        ["OrchestKit", "https://x.test/a"],
        ["A Much Longer Name", "https://x.test/b"],
      ]
    );
    const lines = rendered.split("\n");
    expect(lines[0]).toBe("NAME                URL");
    expect(lines[1]).toBe("------------------  ----------------");
    expect(lines[2]).toBe("OrchestKit          https://x.test/a");
    expect(lines[3]).toBe("A Much Longer Name  https://x.test/b");
  });

  it("never truncates a column left out of shrinkable", () => {
    const longUrl = `https://yonyon.ai/${"x".repeat(200)}`;
    const rendered = table(["URL", "WHAT"], [[longUrl, "a description that could be cut"]], {
      shrinkable: [1],
    });
    expect(rendered).toContain(longUrl);
  });

  it("pads short cells so ragged rows still line up", () => {
    const rendered = table(
      ["A", "B"],
      [
        ["x", "y"],
        ["longer", "z"],
      ]
    );
    expect(rendered.split("\n")[2]).toBe("x       y");
  });
});

describe("splitFollowUps", () => {
  it("strips the FOLLOW_UPS marker the site chat UI uses", () => {
    const { text, followUps } = splitFollowUps(
      'He ships AI products.\n\n[FOLLOW_UPS: "What has he built?" | "Is he available?"]'
    );
    expect(text).toBe("He ships AI products.");
    expect(followUps).toEqual(["What has he built?", "Is he available?"]);
  });

  it("leaves an answer without the marker untouched", () => {
    const { text, followUps } = splitFollowUps("Just an answer.");
    expect(text).toBe("Just an answer.");
    expect(followUps).toEqual([]);
  });

  it("drops empty entries from a malformed marker", () => {
    const { followUps } = splitFollowUps('Answer.\n[FOLLOW_UPS: "a" |  | "b"]');
    expect(followUps).toEqual(["a", "b"]);
  });

  it("strips a marker the API truncated before its closing bracket", () => {
    // Production truncates `answer` at a fixed length, so the marker commonly
    // arrives unterminated and mid-word. Verified against yonyon.ai 2026-08-21.
    const { text, followUps } = splitFollowUps(
      'OrchestKit handles retries and state.\n\n[FOLLOW_UPS: "What problems does it solve?" | "Ho'
    );
    expect(text).toBe("OrchestKit handles retries and state.");
    expect(followUps).toEqual(["What problems does it solve?"]);
  });

  it("keeps the final entry when the marker is properly closed", () => {
    const { followUps } = splitFollowUps('Answer.\n[FOLLOW_UPS: "a" | "b"]');
    expect(followUps).toEqual(["a", "b"]);
  });
});

describe("indentList", () => {
  it("renders a bulleted, indented list", () => {
    expect(indentList(["one", "two"])).toBe("  - one\n  - two");
  });
});

describe("createTrailerStripper", () => {
  it("passes text through untouched when no marker appears", () => {
    const stripper = createTrailerStripper();
    const out = ["Hello", " world"].map((c) => stripper.push(c)).join("") + stripper.flush();
    expect(out).toBe("Hello world");
  });

  it("drops everything from the marker onward", () => {
    const stripper = createTrailerStripper();
    const out =
      ["Answer text.", '\n\n[FOLLOW_UPS: "a" | "b"]'].map((c) => stripper.push(c)).join("") +
      stripper.flush();
    expect(out).toBe("Answer text.");
  });

  it("never emits a partial marker split across chunk boundaries", () => {
    const stripper = createTrailerStripper();
    const chunks = ["Answer.", "\n\n[FOLL", "OW_UPS: ", '"a"]'];
    const emitted = chunks.map((c) => stripper.push(c));
    // The chunk carrying "[FOLL" must not reach stdout on its own, and neither
    // must the blank line in front of it: once the marker is confirmed, that
    // whitespace is trailing and it is already too late to unprint.
    expect(emitted[1]).toBe("");
    expect(emitted.join("") + stripper.flush()).toBe("Answer.");
  });

  it("releases held whitespace when the candidate turns out not to be a marker", () => {
    const stripper = createTrailerStripper();
    const out =
      ["Answer.\n\n[F", "ine print]"].map((c) => stripper.push(c)).join("") + stripper.flush();
    expect(out).toBe("Answer.\n\n[Fine print]");
  });

  it("emits a held tail that turned out not to be a marker", () => {
    const stripper = createTrailerStripper();
    const out = ["See [", "note] below"].map((c) => stripper.push(c)).join("") + stripper.flush();
    expect(out).toBe("See [note] below");
  });

  it("stays finished after the marker, ignoring later chunks", () => {
    const stripper = createTrailerStripper();
    stripper.push('Done.[FOLLOW_UPS: "a"]');
    expect(stripper.push("trailing junk")).toBe("");
    expect(stripper.flush()).toBe("");
  });
});

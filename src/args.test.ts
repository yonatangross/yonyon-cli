import { describe, expect, it } from "vitest";
import {
  assertKnownFlags,
  boolFlag,
  enabledUnlessNegated,
  intFlag,
  parseArgs,
  stringFlag,
  type FlagValue,
} from "./args.js";
import { CliError } from "./errors.js";

describe("parseArgs", () => {
  it("pulls the command off the front and keeps the rest as positionals", () => {
    const { command, positionals } = parseArgs(["ask", "What", "is", "OrchestKit?"]);
    expect(command).toBe("ask");
    expect(positionals).toEqual(["What", "is", "OrchestKit?"]);
  });

  it("returns an empty command when nothing was passed", () => {
    expect(parseArgs([]).command).toBe("");
  });

  it("treats a bare long flag as a boolean switch", () => {
    expect(parseArgs(["projects", "--json"]).flags.get("json")).toBe(true);
  });

  it("accepts --flag=value", () => {
    expect(parseArgs(["projects", "--limit=5"]).flags.get("limit")).toBe("5");
  });

  it("accepts --flag value for value-taking flags", () => {
    expect(parseArgs(["projects", "--limit", "5"]).flags.get("limit")).toBe("5");
  });

  it("reads --no-flag as an explicit false", () => {
    expect(parseArgs(["book", "--no-open"]).flags.get("open")).toBe(false);
  });

  it("expands the -h and -v aliases", () => {
    expect(parseArgs(["-h"]).flags.get("help")).toBe(true);
    expect(parseArgs(["-v"]).flags.get("version")).toBe(true);
  });

  it("stops parsing flags after --", () => {
    const { positionals, flags } = parseArgs(["ask", "--", "--json", "really?"]);
    expect(positionals).toEqual(["--json", "really?"]);
    expect(flags.size).toBe(0);
  });

  it("keeps a dash-led question as a positional rather than a flag", () => {
    expect(parseArgs(["ask", "-5", "degrees?"]).positionals).toEqual(["-5", "degrees?"]);
  });

  it("rejects a value on a boolean flag", () => {
    expect(() => parseArgs(["projects", "--json=yes"])).toThrowError(
      /Flag --json does not take a value/
    );
  });

  it("rejects a value flag with nothing after it", () => {
    expect(() => parseArgs(["projects", "--limit"])).toThrowError(/needs a value/);
  });

  it("rejects a value flag followed by another flag", () => {
    expect(() => parseArgs(["projects", "--limit", "--json"])).toThrowError(/needs a value/);
  });

  it("rejects an empty flag name", () => {
    expect(() => parseArgs(["ask", "--="])).toThrowError(/does not take a value/);
  });

  it("exits with code 2 on a usage mistake", () => {
    try {
      parseArgs(["projects", "--limit"]);
      expect.unreachable("should have thrown");
    } catch (error) {
      expect(error).toBeInstanceOf(CliError);
      expect((error as CliError).exitCode).toBe(2);
    }
  });
});

describe("assertKnownFlags", () => {
  it("accepts the command's own flags plus the global ones", () => {
    const flags = new Map<string, FlagValue>([
      ["json", true],
      ["base-url", "https://x.test"],
    ]);
    expect(() => assertKnownFlags(flags, ["json"], "projects")).not.toThrow();
  });

  it("names the offending flag and the command", () => {
    const flags = new Map([["nope", true as const]]);
    expect(() => assertKnownFlags(flags, ["json"], "projects")).toThrowError(
      /Unknown flag --nope for "yonyon projects"/
    );
  });
});

describe("flag readers", () => {
  it("boolFlag is true only for an explicit switch", () => {
    expect(boolFlag(new Map([["json", true as const]]), "json")).toBe(true);
    expect(boolFlag(new Map([["json", false as const]]), "json")).toBe(false);
    expect(boolFlag(new Map(), "json")).toBe(false);
  });

  it("enabledUnlessNegated defaults to on", () => {
    expect(enabledUnlessNegated(new Map(), "open")).toBe(true);
    expect(enabledUnlessNegated(new Map([["open", false as const]]), "open")).toBe(false);
  });

  it("stringFlag rejects a boolean where a value was needed", () => {
    expect(() => stringFlag(new Map([["base-url", true as const]]), "base-url")).toThrowError(
      /needs a value/
    );
  });

  it("intFlag parses inside the range", () => {
    expect(intFlag(new Map([["limit", "5"]]), "limit", { min: 1, max: 50 })).toBe(5);
  });

  it("intFlag rejects a non-number", () => {
    expect(() => intFlag(new Map([["limit", "many"]]), "limit", { min: 1, max: 50 })).toThrowError(
      /must be a whole number, got "many"/
    );
  });

  it("intFlag rejects a value outside the API's accepted range", () => {
    expect(() => intFlag(new Map([["limit", "99"]]), "limit", { min: 1, max: 50 })).toThrowError(
      /must be between 1 and 50, got 99/
    );
  });

  it("intFlag returns undefined when the flag is absent", () => {
    expect(intFlag(new Map(), "limit", { min: 1, max: 50 })).toBeUndefined();
  });
});

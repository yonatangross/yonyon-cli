import { usageError } from "./errors.js";

export type FlagValue = string | boolean;

export interface ParsedArgs {
  /** The subcommand, or "" when none was given. */
  command: string;
  /** Everything after the subcommand that is not a flag. */
  positionals: string[];
  flags: Map<string, FlagValue>;
}

/** Flags that take a value. Everything else is a boolean switch. */
const VALUE_FLAGS = new Set(["base-url", "limit", "timeout"]);

const ALIASES: Record<string, string> = {
  h: "help",
  v: "version",
};

/**
 * Hand-rolled parser. The CLI has five commands and eight flags, which is well
 * under the size where a dependency pays for itself.
 *
 * Supports `--flag`, `--flag=value`, `--flag value`, `--no-flag`, `-h`, `-v`,
 * and `--` to stop flag parsing. Bare `-` and unknown short clusters are
 * treated as positionals so a question can start with a dash.
 */
export function parseArgs(argv: readonly string[]): ParsedArgs {
  const positionals: string[] = [];
  const flags = new Map<string, FlagValue>();
  let sawTerminator = false;

  for (let i = 0; i < argv.length; i++) {
    const token = argv[i]!;

    if (sawTerminator) {
      positionals.push(token);
      continue;
    }
    if (token === "--") {
      sawTerminator = true;
      continue;
    }

    if (token.startsWith("--")) {
      const body = token.slice(2);
      if (body === "") throw usageError("Empty flag name.");

      const eq = body.indexOf("=");
      if (eq !== -1) {
        const name = body.slice(0, eq);
        const value = body.slice(eq + 1);
        if (!VALUE_FLAGS.has(name)) {
          throw usageError(`Flag --${name} does not take a value.`);
        }
        flags.set(name, value);
        continue;
      }

      if (body.startsWith("no-")) {
        flags.set(body.slice(3), false);
        continue;
      }

      if (VALUE_FLAGS.has(body)) {
        const next = argv[i + 1];
        if (next === undefined || next.startsWith("--")) {
          throw usageError(`Flag --${body} needs a value.`);
        }
        flags.set(body, next);
        i++;
        continue;
      }

      flags.set(body, true);
      continue;
    }

    // Short flags: only the documented single-letter aliases, so that a
    // negative number or a dash-led question stays a positional.
    if (token.length === 2 && token.startsWith("-") && ALIASES[token[1]!]) {
      flags.set(ALIASES[token[1]!]!, true);
      continue;
    }

    positionals.push(token);
  }

  const command = positionals.shift() ?? "";
  return { command, positionals, flags };
}

/** Reject any flag the command does not understand, instead of ignoring it. */
export function assertKnownFlags(
  flags: ReadonlyMap<string, FlagValue>,
  allowed: readonly string[],
  command: string
): void {
  const known = new Set([...allowed, "help", "version", "base-url", "timeout"]);
  for (const name of flags.keys()) {
    if (!known.has(name)) {
      throw usageError(`Unknown flag --${name} for "yonyon ${command}".`, [
        `Run "yonyon ${command} --help" to see the supported flags.`,
      ]);
    }
  }
}

export function boolFlag(flags: ReadonlyMap<string, FlagValue>, name: string): boolean {
  return flags.get(name) === true;
}

/** True unless the flag was explicitly negated with `--no-<name>`. */
export function enabledUnlessNegated(flags: ReadonlyMap<string, FlagValue>, name: string): boolean {
  return flags.get(name) !== false;
}

export function stringFlag(
  flags: ReadonlyMap<string, FlagValue>,
  name: string
): string | undefined {
  const value = flags.get(name);
  if (value === undefined) return undefined;
  if (typeof value !== "string") {
    throw usageError(`Flag --${name} needs a value.`);
  }
  return value;
}

export function intFlag(
  flags: ReadonlyMap<string, FlagValue>,
  name: string,
  range: { min: number; max: number }
): number | undefined {
  const raw = stringFlag(flags, name);
  if (raw === undefined) return undefined;
  if (!/^\d+$/.test(raw)) {
    throw usageError(`--${name} must be a whole number, got "${raw}".`);
  }
  const value = Number(raw);
  if (value < range.min || value > range.max) {
    throw usageError(`--${name} must be between ${range.min} and ${range.max}, got ${value}.`);
  }
  return value;
}

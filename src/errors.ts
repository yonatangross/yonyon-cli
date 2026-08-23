/**
 * Every failure the CLI reports on purpose. `exitCode` 2 means "you typed
 * something wrong", 1 means "the request or the network failed".
 */
export class CliError extends Error {
  readonly exitCode: number;
  /** Extra lines printed under the message, for hints the user can act on. */
  readonly hints: readonly string[];

  constructor(message: string, options: { exitCode?: number; hints?: readonly string[] } = {}) {
    super(message);
    this.name = "CliError";
    this.exitCode = options.exitCode ?? 1;
    this.hints = options.hints ?? [];
  }
}

/** A usage mistake: bad flag, missing argument, unknown command. */
export function usageError(message: string, hints: readonly string[] = []): CliError {
  return new CliError(message, { exitCode: 2, hints });
}

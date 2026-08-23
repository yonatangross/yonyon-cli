/** Injected so tests can assert on output without touching the real streams. */
export interface Io {
  out(text: string): void;
  err(text: string): void;
  isTty: boolean;
}

export const processIo: Io = {
  out: (text) => process.stdout.write(text),
  err: (text) => process.stderr.write(text),
  isTty: Boolean(process.stdout.isTTY),
};

/** Convenience: write a line to stdout. */
export function line(io: Io, text = ""): void {
  io.out(`${text}\n`);
}

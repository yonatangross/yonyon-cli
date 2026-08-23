import type { Io } from "./io.js";

export interface CapturedIo extends Io {
  stdout(): string;
  stderr(): string;
}

/** An Io that records instead of writing, so assertions read the real output. */
export function captureIo(options: { isTty?: boolean } = {}): CapturedIo {
  let out = "";
  let err = "";
  return {
    out: (text) => {
      out += text;
    },
    err: (text) => {
      err += text;
    },
    isTty: options.isTty ?? false,
    stdout: () => out,
    stderr: () => err,
  };
}

/** Build a Response-like object good enough for the code paths under test. */
export function jsonResponse(
  body: unknown,
  init: { status?: number; headers?: Record<string, string> } = {}
): Response {
  return new Response(JSON.stringify(body), {
    status: init.status ?? 200,
    headers: { "content-type": "application/json", ...(init.headers ?? {}) },
  });
}

export function textStreamResponse(chunks: readonly string[]): Response {
  const encoder = new TextEncoder();
  const stream = new ReadableStream<Uint8Array>({
    start(controller) {
      for (const chunk of chunks) controller.enqueue(encoder.encode(chunk));
      controller.close();
    },
  });
  return new Response(stream, {
    status: 200,
    headers: { "content-type": "text/plain; charset=utf-8" },
  });
}

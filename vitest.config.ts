import { defineConfig } from "vitest/config";

// Standalone config so the CLI suite runs on its own via `pnpm --dir cli test`,
// independent of the root project's two-environment vitest setup.
export default defineConfig({
  test: {
    name: "cli",
    environment: "node",
    include: ["src/**/*.test.ts"],
  },
});

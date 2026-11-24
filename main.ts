import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = join(import.meta.dirname, "entry.png");
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);
const size = statSync(dst).size;
if (size !== statSync(src).size) {
  throw new Error("entry.png copy size mismatch");
}
console.log(`wrote ${dst} (${size} bytes)`);

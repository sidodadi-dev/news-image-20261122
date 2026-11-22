/**
 * main.ts — entry point for the "The World in One Day" poster.
 *
 * Copies entry.png (sitting next to this file) into the output directory
 * given by MAKEFUN_OUTPUT_DIR (default /output), creating the directory
 * when needed, and logs how many bytes were written.
 *
 * Standard library only, no network. Running it twice produces
 * byte-identical output: it is a plain file copy.
 */
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
if (!existsSync(source)) {
  console.error(`entry.png not found next to main.ts (${here})`);
  process.exit(1);
}
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");

mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(source, target);
const bytes = statSync(target).size;
console.log(`wrote ${target} (${bytes} bytes)`);

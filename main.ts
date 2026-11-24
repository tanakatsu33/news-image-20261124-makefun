// make.fun entry: news-image-20261124
// Publishes the pre-drawn front page (entry.png, rendered by draw.py) to the output directory.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

const bytes = statSync(target).size;
// One log line so the run is easy to audit: where it came from, where it went, how big.
console.log(`front page for Tuesday 24 November 2026: copied ${source} -> ${target} (${bytes} bytes)`);

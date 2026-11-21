// The Friday Edition — V8 entrypoint.
// Runs render.py (Python 3 + Pillow, no network, no reads outside this
// folder). render.py writes entry.png (1024x1024) straight into the
// grader's output directory when MAKEFUN_OUTPUT_DIR is set, so the
// entrypoint works even when the repo itself is read-only.
import { existsSync } from "node:fs";
import { join } from "node:path";
import { execFileSync } from "node:child_process";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? ".";
execFileSync("python3", ["render.py"], { stdio: "inherit" });

const produced = join(outDir, "entry.png");
if (!existsSync(produced)) {
  throw new Error(`render.py did not produce ${produced}`);
}
console.log(`wrote ${produced}`);

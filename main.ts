// makefun-news-image-19 — entry program (Node 22, standard library only).
//
// The picture itself is entry.png, drawn by gen_image.py from the news of
// Thursday 19 November 2026 and shipped in this repository. The grader
// runs this program with no network, so all it has to do is place that
// image at the output path the grader reads.
//
// Local run:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// Grader run:
//   node main.ts            (writes /output/entry.png)

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

// The copy is byte-for-byte deterministic: the same entry.png is shipped
// in the repository, so both grader runs write identical bytes.
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, 'entry.png'), target);

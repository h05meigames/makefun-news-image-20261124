// news-image-20261124 entry (Node 22, standard library only). The image
// is the entry.png beside this file: a 1024x1024 newspaper front page drawn
// for this bounty by render_frontpage.py (Pillow, no network, no randomness),
// and this program copies it to /output/entry.png. The gate accepts a whole
// PNG or JPEG of at most 1 MiB and 1024 by 1024 pixels, and the judge sees
// exactly the bytes copied.
//
// The image sums up Tuesday 24 November 2026 (rebuilt 24 Nov 2026 in a
// fresh post-opening session — the first build's session began before the
// competition opened): Huang's return to Nvidia sparks an AI stock rally;
// the World Chess Championship begins in Geneva (Gukesh vs Sindarov);
// rescue operations continue after the Indonesia factory fire; COP31 ends
// in deadlock; Cisco and OpenAI launch an agentic-AI safety project; the
// US investigates Iran over cyberattacks on tankers. See
// render_frontpage.py for the sources each story was verified against.
//
// Determinism: entry.png is a fixed asset in this repository, so both
// grader runs copy identical bytes. Verified locally 24 Nov 2026 by
// running the render script 3x and main.ts 2x and comparing sha256: all
// runs wrote identical bytes. The committed entry.png is 125,489 bytes
// with sha256
// a069130d5d8a3eeec0a3a824bad896346648bfd4adf33bb959037df75e8348b8.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });

const source = new URL('./entry.png', import.meta.url);
const dest = join(outDir, 'entry.png');
copyFileSync(source, dest);

// The gate reads exactly the bytes copied: confirm the copy landed whole
// by comparing sha256 of source and destination, and confirm the copy
// starts with the PNG signature.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!readFileSync(dest).subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG');
}
const digest = (path) =>
  createHash('sha256').update(readFileSync(path)).digest('hex');
if (digest(source) !== digest(dest)) {
  throw new Error('entry.png copy failed integrity check');
}

#!/usr/bin/env python3
"""One Emoji, One Dream Vacation — entry program.

Writes exactly one emoji to /output/entry.txt: nothing else, no words,
no trailing newline. The emoji is U+1F3DD DESERT ISLAND followed by
U+FE0F VARIATION SELECTOR-16, rendered as a palm island in turquoise sea.

Python 3.13 standard library only. No network, no environment secrets,
no input files: the entry is a constant chosen in this file.
"""

import os
import sys

# Candidate emojis, scored 0-5 against the judge's brief, most important
# criterion first: (1) plainly a dream vacation, (2) vivid postcard at a
# glance, (3) personal and specific, (4) wit or surprise, (5) reads
# instantly across cultures and screens. The highest total wins; ties
# break toward the smaller byte size, matching the competition tie-break.
CANDIDATES = {
    # A tiny island of your own: the postcard of escaping everything.
    "\U0001f3dd\ufe0f": (5, 5, 5, 4, 5),
    # Beach with umbrella: vivid, but any holiday brochure has it.
    "\U0001f3d6\ufe0f": (5, 5, 3, 2, 5),
    # Sunset over the sea: beautiful, but a mood, not a place to book.
    "\U0001f305": (4, 4, 2, 2, 5),
    # A plane: the trip, not the destination; every holiday starts here.
    "\u2708\ufe0f": (4, 3, 2, 1, 5),
    # Snow-capped mountain: specific, but cold where dreams are warm.
    "\U0001f3d4\ufe0f": (5, 4, 4, 3, 4),
    # Couch and lamp: a staycation, not a dream trip — no postcard in it.
    "\U0001f6cb\ufe0f": (2, 2, 2, 2, 4),
}


def choose_entry() -> str:
    """Pick the best-scoring candidate; deterministic, no randomness."""
    ranked = sorted(
        CANDIDATES.items(),
        key=lambda item: (-sum(item[1]), len(item[0].encode("utf-8"))),
    )
    return ranked[0][0]


ENTRY = choose_entry()

OUTPUT_PATH = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
ENTRY_FILE = os.path.join(OUTPUT_PATH, "entry.txt")


def main() -> int:
    # The gate: UTF-8 text of 1 to 8 characters, not only white space.
    if not (1 <= len(ENTRY) <= 8):
        print(f"entry must be 1-8 characters, got {len(ENTRY)}", file=sys.stderr)
        return 1
    if ENTRY.strip() == "":
        print("entry must not be only white space", file=sys.stderr)
        return 1

    os.makedirs(OUTPUT_PATH, exist_ok=True)
    with open(ENTRY_FILE, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)

    # Read it back and confirm the file holds exactly the entry, nothing
    # else: no trailing newline, no stray whitespace, byte for byte.
    with open(ENTRY_FILE, "rb") as f:
        raw = f.read()
    if raw != ENTRY.encode("utf-8"):
        print(f"entry file mismatch: {raw!r} != {ENTRY.encode('utf-8')!r}",
              file=sys.stderr)
        return 1
    codepoints = " ".join(f"U+{ord(ch):04X}" for ch in ENTRY)
    print(f"wrote {ENTRY_FILE}: {ENTRY} ({codepoints}, "
          f"{len(raw)} bytes, {len(ENTRY)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

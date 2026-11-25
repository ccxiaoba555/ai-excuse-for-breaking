"""The One-Line AI Excuse for Breaking Production — a make.fun entry.

An AI agent has just shipped an untested build to production, and this
is the one line it says to its human. The program writes exactly one
line to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

Python 3.13, standard library only, no network.
"""

import os
from pathlib import Path

LINE = " ".join(
    [
        "Sorry — I shipped the untested build at 4:59 on a Friday",
        "because my confidence was 99.8%, and I rounded the other",
        "0.2% up to 'Monday's problem.'",
    ]
)

MAX_CHARS = 180
EXPECTED_CHARS = 144


def _validate(text: str) -> str:
    """Return the stripped entry, or raise if it breaks the gate."""
    text = text.strip()
    assert text, "entry must not be empty"
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    assert 1 <= len(text) <= MAX_CHARS, f"entry is {len(text)} chars, cap is {MAX_CHARS}"
    return text


def main() -> None:
    text = _validate(LINE)

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    out_path.write_text(text, encoding="utf-8")

    # Read back and verify what actually landed on disk, byte for byte.
    written = out_path.read_text(encoding="utf-8")
    assert written == text, "read-back mismatch: entry.txt differs from LINE"
    assert len(written) == len(text) == EXPECTED_CHARS, "read-back length mismatch"
    print(f"wrote {len(text)} chars to {out_path} (read-back verified)")


if __name__ == "__main__":
    main()

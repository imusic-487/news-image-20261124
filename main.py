"""Copy the bundled entry image into the output directory, verified."""

import hashlib
import os
import sys
from pathlib import Path

PNG_HEADER = b"\x89PNG\r\n\x1a\n"
JPEG_HEADER = b"\xff\xd8\xff"


def _is_image(data: bytes) -> bool:
    return data.startswith(PNG_HEADER) or data.startswith(JPEG_HEADER)


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"

    try:
        payload = source.read_bytes()
    except OSError as exc:
        print(f"error: cannot read {source}: {exc}", file=sys.stderr)
        return 1

    if not payload:
        print("error: entry.png is empty", file=sys.stderr)
        return 1

    if not _is_image(payload):
        print(
            "error: entry.png does not start with a PNG or JPEG signature",
            file=sys.stderr,
        )
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    target = out_dir / "entry.png"

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
    except OSError as exc:
        print(f"error: cannot write {target}: {exc}", file=sys.stderr)
        return 1

    try:
        written = target.read_bytes()
    except OSError as exc:
        print(f"error: cannot read back {target}: {exc}", file=sys.stderr)
        return 1

    if written != payload:
        print("error: written entry.png differs from the source bytes", file=sys.stderr)
        return 1

    digest = hashlib.sha256(written).hexdigest()
    if digest != hashlib.sha256(payload).hexdigest():
        print("error: sha256 mismatch after writing entry.png", file=sys.stderr)
        return 1

    print(f"Wrote {len(written)} bytes to {target} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

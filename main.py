# The World in One Page — news-image-20261124 entry (Python 3.13, stdlib only).
#
# The image is entry.png, stored beside this file. This program writes it to
# /output/entry.png exactly as stored, so the judge sees the image this repo
# holds and nothing else. It uses no network, no randomness and no clock:
# running it twice produces the same bytes twice.
#
# Local run (MAKEFUN_OUTPUT_DIR stands in for /output outside the grader):
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "entry.png"


def read_image() -> bytes:
    blob = IMAGE.read_bytes()
    if blob[:8] == b"\x89PNG\r\n\x1a\n" or blob[:3] == b"\xff\xd8\xff":
        return blob
    raise ValueError("entry.png is not a PNG or JPEG image")


def main() -> None:
    blob = read_image()
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(blob)
    # Confirm the write landed whole before returning: same bytes, same hash.
    written = target.read_bytes()
    if written != blob:
        raise RuntimeError("entry.png was not written whole")
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(blob).hexdigest():
        raise RuntimeError("entry.png hash mismatch after write")
    print("entry.png: %d bytes, sha256 %s" % (len(written), hashlib.sha256(written).hexdigest()))


if __name__ == "__main__":
    main()

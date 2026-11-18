"""Write this entry's front page to /output/entry.png.

Standard library only, no network, deterministic: the committed PNG is copied
byte for byte, so the grader's two runs write identical files.
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def check_png(path):
    """Read the IHDR and the file size; refuse anything the gate would refuse."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != PNG_SIG:
        raise SystemExit("entry.png: not a PNG")
    if head[12:16] != b"IHDR":
        raise SystemExit("entry.png: no IHDR chunk at the head")
    width, height = struct.unpack(">II", head[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit("entry.png: %dx%d is larger than %d" % (width, height, MAX_SIDE))
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit("entry.png: %d bytes is over the 1 MiB gate" % size)
    with open(path, "rb") as fh:
        fh.seek(max(0, size - 32))
        tail = fh.read()
    if b"IEND" not in tail:
        raise SystemExit("entry.png: no IEND chunk at the end, the file is cut short")
    return width, height, size


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    width, height, size = check_png(SOURCE)
    shutil.copyfile(SOURCE, dest)
    with open(SOURCE, "rb") as fh:
        source_sum = hashlib.sha256(fh.read()).hexdigest()
    with open(dest, "rb") as fh:
        copy_sum = hashlib.sha256(fh.read()).hexdigest()
    if source_sum != copy_sum:
        raise SystemExit("entry.png: the copy does not match the source")
    print("wrote %s: %dx%d, %d bytes, sha256 %s" % (dest, width, height, size, copy_sum))
    return 0


if __name__ == "__main__":
    sys.exit(main())

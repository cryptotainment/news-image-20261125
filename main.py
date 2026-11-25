#!/usr/bin/env python3
"""news-image-20261125: write the day's front page to /output/entry.png.

The image (entry.png, rendered by render.py in this repository) sums up
world news of Wednesday 25 November 2026. This program only copies it,
so both runs write byte-identical output. Standard library only, no
network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # sanity check: the copy must be a whole PNG within the gate limits
    with open(dst, "rb") as f:
        head = f.read(8)
    assert head == b"\x89PNG\r\n\x1a\n", "entry.png is not a PNG"
    assert os.path.getsize(dst) <= 1048576, "entry.png exceeds 1 MiB"
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()

# News-image entry: the program copies the front-page image beside it
# to /output/entry.png. The image itself (entry.png) was composed by
# compose.py in this repository from the pixel-art illustration
# scene.png (drawn pixel by pixel by pixel.py) and the 23 November
# 2026 news summary it carries; this program does no network and no
# drawing, so both runs write exactly the same bytes.
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(DST_DIR, exist_ok=True)
shutil.copyfile(SRC, os.path.join(DST_DIR, "entry.png"))

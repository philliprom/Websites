#!/bin/bash
# Kontaktbogen eines Videos: alle N Sekunden ein Bild mit Zeitstempel.  bash kontaktbogen.sh video.mp4 bogen.png [N=3]
V=$1; OUTP=$2; STEP=${3:-3}
D=$(mktemp -d)
ffmpeg -hide_banner -loglevel error -i "$V" -vf "fps=1/$STEP,scale=270:480" $D/s_%03d.png
python3 - "$D" "$OUTP" "$STEP" <<'PY'
import sys, glob
from PIL import Image, ImageDraw
d, out, step = sys.argv[1], sys.argv[2], float(sys.argv[3])
fs = sorted(glob.glob(d + '/s_*.png'))
cols = 12; rows = (len(fs) + cols - 1) // cols
o = Image.new('RGB', (cols * 270, rows * 480), 'black'); dr = ImageDraw.Draw(o)
for i, f in enumerate(fs):
    x, y = (i % cols) * 270, (i // cols) * 480
    o.paste(Image.open(f).convert('RGB'), (x, y)); dr.text((x + 4, y + 4), f"{i*step:.0f}s", fill=(255, 255, 0))
o.save(out); print(len(fs), "Bilder ->", out)
PY

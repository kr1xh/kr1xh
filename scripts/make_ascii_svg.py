"""Convert a prepared grayscale portrait into a self-typing ASCII SVG."""
from pathlib import Path
import numpy as np
from PIL import Image

SOURCE = Path("data/prepped_photo.png")
OUT = Path("krish-ascii.svg")
RAMP = " .`:-=+*#%@"
COLS = 78
ROWS = 42
CELL_W = 9
CELL_H = 11


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"{SOURCE} not found. Run prep_photo.py first.")
    image = Image.open(SOURCE).convert("L")
    image.thumbnail((COLS, ROWS))
    canvas = Image.new("L", (COLS, ROWS), 255)
    x = (COLS - image.width) // 2
    y = (ROWS - image.height) // 2
    canvas.paste(image, (x, y))
    arr = np.asarray(canvas)

    text_rows = []
    for r in range(ROWS):
        chars = []
        for c in range(COLS):
            idx = int((255 - int(arr[r, c])) / 256 * len(RAMP))
            chars.append(RAMP[min(idx, len(RAMP) - 1)])
        text_rows.append("".join(chars).rstrip())

    width = COLS * CELL_W
    height = ROWS * CELL_H
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>text{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:10px;fill:#8b949e}}.row{{opacity:0;animation:print .5s ease-out var(--delay) forwards}}@keyframes print{{from{{opacity:0;transform:translateX(-12px)}}to{{opacity:1;transform:translateX(0)}}}}</style><rect width="100%" height="100%" rx="10" fill="#0d1117"/>''']
    for r, row in enumerate(text_rows):
        delay = r * 0.045
        parts.append(f'<text x="8" y="{(r+1)*CELL_H}" class="row" style="--delay:{delay:.3f}s">{row.replace("&", "&amp;").replace("<", "&lt;")}</text>')
    parts.append("</svg>")
    OUT.write_text("".join(parts), encoding="utf-8")


if __name__ == "__main__":
    main()

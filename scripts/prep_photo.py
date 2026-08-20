"""Prepare a portrait for ASCII conversion.

Usage:
    python scripts/prep_photo.py images/source-photo.jpg
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

OUT = Path("data/prepped_photo.png")


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/prep_photo.py <photo>")
    source = Path(sys.argv[1])
    image = cv2.imread(str(source))
    if image is None:
        raise FileNotFoundError(source)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # White background keeps the bright end of the ASCII ramp visually empty.
    enhanced = cv2.normalize(enhanced, None, 0, 255, cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgb).save(OUT)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()

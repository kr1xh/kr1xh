"""Render contribution JSON as an animated, self-contained SVG."""
import json
from pathlib import Path

DATA = Path("data/contributions.json")
OUT = Path("contrib-heatmap.svg")
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
CELL = 13
GAP = 4
LEFT = 24
TOP = 18
WIDTH = 860
HEIGHT = 130


def esc(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def main():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    days = payload["days"][-371:]
    # Pad to 53 full weeks.
    days = [{"date": "", "count": 0, "level": 0}] * (371 - len(days)) + days

    rects = []
    for i, d in enumerate(days):
        week, dow = divmod(i, 7)
        x = LEFT + week * (CELL + GAP)
        y = TOP + dow * (CELL + GAP)
        delay = i * 0.012
        title = f'{d["date"]}: {d["count"]} contributions' if d["date"] else ""
        rects.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
            f'fill="{PALETTE[min(max(d["level"], 0), 4)]}" style="--delay:{delay:.3f}s">'
            f'<title>{esc(title)}</title></rect>'
        )

    stats = payload.get("stats", {})
    total = stats.get("total", 0)
    streak = stats.get("current_streak", 0)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<style>
rect {{ opacity:0; transform-box:fill-box; transform-origin:center; animation:reveal .55s ease-out var(--delay) forwards; }}
@keyframes reveal {{ from {{ opacity:0; transform:translateY(-8px) scale(.75); }} to {{ opacity:1; transform:translateY(0) scale(1); }} }}
text {{ font-family:ui-monospace,SFMono-Regular,Consolas,monospace; fill:#8b949e; font-size:11px; }}
</style>
<rect width="100%" height="100%" rx="10" fill="#0d1117"/>
<text x="24" y="115">Less</text>
<rect x="56" y="106" width="12" height="12" rx="3" fill="{PALETTE[0]}"/>
<rect x="73" y="106" width="12" height="12" rx="3" fill="{PALETTE[1]}"/>
<rect x="90" y="106" width="12" height="12" rx="3" fill="{PALETTE[2]}"/>
<rect x="107" y="106" width="12" height="12" rx="3" fill="{PALETTE[3]}"/>
<rect x="124" y="106" width="12" height="12" rx="3" fill="{PALETTE[4]}"/>
<text x="143" y="115">More</text>
<text x="510" y="115">{total:,} contributions · {streak} day current streak</text>
{"".join(rects)}
</svg>'''
    OUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

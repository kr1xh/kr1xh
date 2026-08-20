"""Render the full 53-week contribution calendar as an animated SVG."""
import json
from pathlib import Path

DATA = Path("data/contributions.json")
OUT = Path("contrib-heatmap.svg")
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
CELL = 11
GAP = 3
LEFT = 26
TOP = 24
WIDTH = 860
HEIGHT = 132


def esc(value):
    return (str(value).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def main():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    source = payload["days"][-371:]
    days = [{"date": "", "count": 0, "level": 0}] * (371 - len(source)) + source

    rects = []
    for i, day in enumerate(days):
        week, dow = divmod(i, 7)
        x = LEFT + week * (CELL + GAP)
        y = TOP + dow * (CELL + GAP)
        delay = i * 0.010
        level = min(max(int(day.get("level", 0)), 0), 4)
        title = f'{day["date"]}: {day["count"]} contributions' if day["date"] else ""
        rects.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" '
            f'fill="{PALETTE[level]}" style="--delay:{delay:.3f}s">'
            f'<title>{esc(title)}</title></rect>'
        )

    stats = payload.get("stats", {})
    total = int(stats.get("total", 0))
    streak = int(stats.get("current_streak", 0))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<style>
.cell {{ opacity:0; transform-box:fill-box; transform-origin:center; animation:reveal .45s ease-out var(--delay) forwards; }}
@keyframes reveal {{ from {{ opacity:0; transform:translateY(-7px) scale(.8); }} to {{ opacity:1; transform:translateY(0) scale(1); }} }}
.label {{ font-family:ui-monospace,SFMono-Regular,Consolas,monospace; fill:#8b949e; font-size:10px; }}
.stat {{ font-family:ui-monospace,SFMono-Regular,Consolas,monospace; fill:#c9d1d9; font-size:11px; }}
</style>
<rect width="100%" height="100%" rx="10" fill="#0d1117"/>
<text x="26" y="17" class="label">contributions — last 53 weeks</text>
<text x="26" y="121" class="label">Less</text>
<rect x="56" y="112" width="11" height="11" rx="2.5" fill="{PALETTE[0]}"/>
<rect x="72" y="112" width="11" height="11" rx="2.5" fill="{PALETTE[1]}"/>
<rect x="88" y="112" width="11" height="11" rx="2.5" fill="{PALETTE[2]}"/>
<rect x="104" y="112" width="11" height="11" rx="2.5" fill="{PALETTE[3]}"/>
<rect x="120" y="112" width="11" height="11" rx="2.5" fill="{PALETTE[4]}"/>
<text x="138" y="121" class="label">More</text>
<text x="690" y="121" text-anchor="end" class="stat">{total:,} contributions · {streak} day streak</text>
{''.join(rects)}
</svg>'''
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()

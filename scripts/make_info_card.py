"""Generate Krish's terminal/neofetch-style SVG info card."""
from pathlib import Path

OUT = Path("info-card.svg")

ROWS = [
    ("role", "AI/ML Research Student"),
    ("focus", "Machine Learning + Robotics"),
    ("stack", "Python · C++ · Git"),
    ("research", "ML · Computer Vision · Robotics"),
    ("building", "Projects · Research · Open Source"),
]


def main():
    lines = []
    for i, (key, value) in enumerate(ROWS):
        y = 70 + i * 38
        delay = i * 0.12
        lines.append(f'<g style="--delay:{delay:.2f}s"><text x="32" y="{y}" class="key">{key}</text><text x="132" y="{y}" class="value">{value}</text></g>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="490" height="250" viewBox="0 0 490 250">
<style>
text {{ font-family:ui-monospace,SFMono-Regular,Consolas,monospace; }}
.title {{ fill:#39d353; font-size:16px; font-weight:700; }}
.key {{ fill:#58a6ff; font-size:13px; font-weight:700; }}
.value {{ fill:#c9d1d9; font-size:13px; }}
g {{ opacity:0; animation:fade .55s ease-out var(--delay) forwards; }}
@keyframes fade {{ from {{ opacity:0; transform:translateX(-8px); }} to {{ opacity:1; transform:translateX(0); }} }}
</style>
<rect width="490" height="250" rx="10" fill="#0d1117" stroke="#30363d"/>
<circle cx="22" cy="20" r="5" fill="#ff7b72"/><circle cx="40" cy="20" r="5" fill="#d29922"/><circle cx="58" cy="20" r="5" fill="#3fb950"/>
<text x="32" y="48" class="title">krish@github — neofetch</text>
{''.join(lines)}
</svg>'''
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()

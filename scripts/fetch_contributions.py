"""Fetch the public GitHub contribution calendar for a username."""
import json
import os
import re
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = os.getenv("GITHUB_USERNAME", "kr1xh")
OUT = Path("data/contributions.json")
URL = f"https://github.com/users/{USERNAME}/contributions"


def main():
    response = requests.get(URL, timeout=30, headers={"User-Agent": "profile-art/1.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    days = []
    for cell in soup.select("td.ContributionCalendar-day"):
        raw_date = cell.get("data-date")
        if not raw_date:
            continue
        try:
            count = int(cell.get("data-count", "0"))
        except ValueError:
            count = 0
        try:
            level = int(cell.get("data-level", "0"))
        except ValueError:
            level = 0
        days.append({"date": raw_date, "count": count, "level": level})

    if not days:
        # GitHub's markup can change. Fail loudly rather than committing an empty graph.
        raise RuntimeError("No contribution cells found; GitHub markup may have changed.")

    days.sort(key=lambda x: x["date"])
    counts = [d["count"] for d in days]
    total = sum(counts)

    current = 0
    for d in reversed(days):
        if d["count"] > 0:
            current += 1
        elif current:
            break

    longest = best = 0
    for d in days:
        if d["count"] > 0:
            longest += 1
            best = max(best, longest)
        else:
            longest = 0

    best_day = max(days, key=lambda d: d["count"])
    monthly = {}
    for d in days:
        key = d["date"][:7]
        monthly[key] = monthly.get(key, 0) + d["count"]

    payload = {
        "username": USERNAME,
        "days": days,
        "stats": {
            "total": total,
            "current_streak": current,
            "longest_streak": best,
            "best_day": best_day,
            "monthly": monthly,
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved {len(days)} contribution days to {OUT}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Merge the last 14 days of GitHub clone traffic into docs/downloads.json.

GitHub only keeps 14 days, so the file keeps every day it has seen and the
site shows the running total. Needs TRAFFIC_TOKEN (repo Administration: read).
"""
import datetime
import json
import os
import pathlib
import urllib.request

REPO = os.environ.get("GITHUB_REPOSITORY", "tjthouhid/tjforge")
OUT = pathlib.Path(__file__).resolve().parents[2] / "docs" / "downloads.json"


def fetch_clones():
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/traffic/clones",
        headers={
            "Authorization": f"Bearer {os.environ['TRAFFIC_TOKEN']}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.load(res)["clones"]


def main():
    data = json.loads(OUT.read_text()) if OUT.exists() else {"days": []}
    by_date = {d["date"]: d for d in data["days"]}
    for row in fetch_clones():
        date = row["timestamp"][:10]
        prev = by_date.get(date, {"clones": 0, "uniques": 0})
        by_date[date] = {
            "date": date,
            "clones": max(prev["clones"], row["count"]),
            "uniques": max(prev["uniques"], row["uniques"]),
        }
    days = [by_date[k] for k in sorted(by_date)]
    OUT.write_text(json.dumps({
        "updated": datetime.date.today().isoformat(),
        "unique_cloners": sum(d["uniques"] for d in days),
        "clones": sum(d["clones"] for d in days),
        "since": days[0]["date"] if days else None,
        "days": days,
    }, indent=2) + "\n")
    print(f"unique cloners total: {sum(d['uniques'] for d in days)}")


if __name__ == "__main__":
    main()

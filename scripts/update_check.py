#!/usr/bin/env python3
"""tjforge update check. Prints one line when the published tjforge is newer
than this copy, and nothing otherwise. Checks the network at most once a day.
Never updates anything. Silent on any error (offline, not a git clone, ...).

  --now   ignore the once-a-day limit
"""
import subprocess
import sys
import time
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
STAMP = Path.home() / ".claude" / ".tjforge-update-check"
DAY = 24 * 60 * 60


def git(*args, timeout=10):
    r = subprocess.run(["git", "-C", str(SKILL), *args], capture_output=True, text=True,
                       timeout=timeout, env={"GIT_TERMINAL_PROMPT": "0", "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"})
    if r.returncode:
        raise RuntimeError(r.stderr)
    return r.stdout.strip()


def parse(v):
    try:
        return tuple(int(x) for x in v.strip().lstrip("v").split(".")[:3])
    except ValueError:
        return ()


def main():
    if "--now" not in sys.argv:
        try:
            if time.time() - STAMP.stat().st_mtime < DAY:
                return
        except OSError:
            pass
    try:
        STAMP.parent.mkdir(parents=True, exist_ok=True)
        STAMP.touch()
    except OSError:
        pass
    if not (SKILL / ".git").exists():
        return
    local = parse((SKILL / "VERSION").read_text()) if (SKILL / "VERSION").exists() else ()
    git("fetch", "--quiet", "origin")
    ref = git("symbolic-ref", "--quiet", "refs/remotes/origin/HEAD") or "refs/remotes/origin/main"
    remote_text = git("show", f"{ref}:VERSION")
    remote = parse(remote_text)
    if remote and remote > local:
        print(f"tjforge {remote_text.strip()} is available (you have {'.'.join(map(str, local)) or 'an older version'}). "
              f"Update: git -C {SKILL} pull. Changes: CHANGELOG.md")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass

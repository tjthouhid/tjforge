#!/usr/bin/env python3
"""tjforge install: put the enforcement pieces into the project in the current
directory, or bring them up to date. Idempotent.

  --check   report only; exit 1 if anything is missing, outdated or edited
  --quiet   print nothing when everything is already in sync
  --force   replace managed files even if they were edited in the project

Files tjforge manages are recorded with a hash in .claude/tjforge.lock.json.
A managed file that still matches its recorded hash is updated automatically;
one that was edited in the project is left alone with a WARN line.

Installs:
  .claude/agents/tj-*.md      subagents pinned to their models
  .claude/settings.json       attribution off (commit and PR)
  .githooks/commit-msg        strips AI-attribution trailers, and is activated
  CLAUDE.md                   the tjforge block (between markers)
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL / "templates"
CHECK = "--check" in sys.argv
QUIET = "--quiet" in sys.argv
FORCE = "--force" in sys.argv
START, END = "<!-- tjforge:start -->", "<!-- tjforge:end -->"
CHAIN = '"$(git rev-parse --show-toplevel)/.githooks/commit-msg" "$1" # tjforge'

missing = 0
lines = []


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


code, top = git("rev-parse", "--show-toplevel")
IS_REPO = code == 0
ROOT = Path(top) if IS_REPO else Path.cwd()
LOCK = ROOT / ".claude" / "tjforge.lock.json"
try:
    lock = json.loads(LOCK.read_text()).get("files", {}) if LOCK.exists() else {}
except (json.JSONDecodeError, AttributeError):
    lock = {}
lock_changed = False


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def record(key, text):
    global lock_changed
    h = sha(text)
    if lock.get(key) != h:
        lock[key] = h
        lock_changed = True


def edited(key, current):
    """True when the project's copy differs from what tjforge last installed."""
    return lock.get(key) != sha(current)


def report(state, what):
    global missing
    if state in ("MISSING", "EDITED"):
        missing += 1
    lines.append((state, f"{state:8} {what}"))


def sync_file(src, dst, executable=False):
    """Copy src to dst if missing or different."""
    want = src.read_text()
    rel = dst.relative_to(ROOT)
    key = str(rel)
    current = dst.read_text() if dst.exists() else None
    if current == want:
        if not CHECK:
            if executable:
                dst.chmod(0o755)
            record(key, want)
        report("ok", rel)
        return
    if current is not None and edited(key, current) and not FORCE:
        report("EDITED" if CHECK else "WARN",
               f"{rel} was edited in this project; not replaced. Merge the new template by hand, "
               f"or re-run with --force to replace it.")
        return
    if CHECK:
        report("MISSING", f"{rel}{' (outdated)' if current is not None else ''}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(want)
    if executable:
        dst.chmod(0o755)
    record(key, want)
    report("updated" if current is not None else "wrote", rel)


def agents():
    for src in sorted((TEMPLATES / "agents").glob("*.md")):
        sync_file(src, ROOT / ".claude" / "agents" / src.name)


def settings():
    path = ROOT / ".claude" / "settings.json"
    want = {"commit": "", "pr": ""}
    data = {}
    if path.exists():
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            report("WARN", ".claude/settings.json is not valid JSON; attribution not set. Fix it and re-run.")
            return
    cur = data.get("attribution")
    if cur is False or (isinstance(cur, dict) and cur.get("commit") == "" and cur.get("pr") == ""):
        report("ok", ".claude/settings.json attribution off")
        return
    if CHECK:
        report("MISSING", ".claude/settings.json attribution off")
        return
    merged = dict(cur) if isinstance(cur, dict) else {}
    merged.update(want)
    data["attribution"] = merged
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")
    report("wrote", ".claude/settings.json attribution off")


def chain_into(hook_file):
    """Make an existing hooks directory call .githooks/commit-msg."""
    rel = hook_file
    try:
        rel = hook_file.relative_to(ROOT)
    except ValueError:
        pass
    text = hook_file.read_text() if hook_file.exists() else ""
    if "# tjforge" in text:
        report("ok", f"{rel} calls .githooks/commit-msg")
        return
    if CHECK:
        report("MISSING", f"{rel} does not call .githooks/commit-msg")
        return
    if text:
        text = text.rstrip("\n") + "\n" + CHAIN + "\n"
    else:
        text = "#!/usr/bin/env sh\n" + CHAIN + "\n"
    hook_file.parent.mkdir(parents=True, exist_ok=True)
    hook_file.write_text(text)
    hook_file.chmod(0o755)
    report("wrote", f"{rel} now calls .githooks/commit-msg")


def hook():
    sync_file(TEMPLATES / "githooks" / "commit-msg", ROOT / ".githooks" / "commit-msg", executable=True)
    if not IS_REPO:
        report("WARN", "not a git repository: hook copied but not active. Run `git init`, then re-run install.")
        return
    _, hooks_path = git("config", "--get", "core.hooksPath")
    if hooks_path.rstrip("/") == ".githooks":
        report("ok", "git core.hooksPath = .githooks")
        return
    if hooks_path:
        # Another hook manager (husky, lefthook, a team hooks dir) owns the path.
        d = Path(hooks_path).expanduser()
        d = d if d.is_absolute() else ROOT / d
        if d.name == "_":  # husky v9 keeps its shims in .husky/_
            d = d.parent
        d = d.resolve()
        if ROOT.resolve() not in [d, *d.parents]:
            report("WARN", f"core.hooksPath points outside the project ({hooks_path}); hook not activated. "
                           f"Add this line to its commit-msg yourself: {CHAIN}")
            return
        chain_into(d / "commit-msg")
        return
    _, common = git("rev-parse", "--git-common-dir")
    hooks_dir = (Path(common) if Path(common).is_absolute() else ROOT / common) / "hooks"
    active = [f for f in hooks_dir.iterdir() if f.is_file() and not f.name.endswith(".sample")] if hooks_dir.is_dir() else []
    if active:
        # Switching hooksPath would silently disable these, so chain instead.
        chain_into(hooks_dir / "commit-msg")
        return
    if CHECK:
        report("MISSING", "git core.hooksPath = .githooks")
        return
    subprocess.run(["git", "config", "core.hooksPath", ".githooks"], check=True)
    report("wrote", "git core.hooksPath = .githooks")


def claude_md():
    block = (TEMPLATES / "claude-md-block.md").read_text().strip()
    path = ROOT / "CLAUDE.md"
    text = path.read_text() if path.exists() else ""
    key = "CLAUDE.md#tjforge"
    if START in text and END in text:
        head, rest = text.split(START, 1)
        old_body, tail = rest.split(END, 1)
        current = START + old_body + END
        new = head + block + tail
    else:
        current = None
        new = (text.rstrip("\n") + "\n\n" if text.strip() else "") + block + "\n"
    if new == text:
        if not CHECK:
            record(key, block)
        report("ok", "CLAUDE.md tjforge block")
    elif current is not None and edited(key, current) and not FORCE:
        report("EDITED" if CHECK else "WARN",
               "CLAUDE.md tjforge block was edited in this project; not replaced. "
               "Put project rules outside the markers, or re-run with --force.")
    elif CHECK:
        report("MISSING", f"CLAUDE.md tjforge block{' (outdated)' if current else ''}")
    else:
        path.write_text(new)
        record(key, block)
        report("updated" if current else "wrote", "CLAUDE.md tjforge block")


def contract():
    for rel in ("docs/PROJECT-PROFILE.md",):
        if (ROOT / rel).exists():
            report("ok", rel)
        else:
            report("MISSING" if CHECK else "WARN", f"{rel} not written yet (run /tjforge init)")


agents()
settings()
hook()
claude_md()
contract()

if lock_changed and not CHECK:
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    LOCK.write_text(json.dumps({"files": dict(sorted(lock.items()))}, indent=2) + "\n")

if not (QUIET and all(state == "ok" for state, _ in lines)):
    print(f"tjforge {'check' if CHECK else 'install'}: {ROOT}")
    for state, line in lines:
        if not (QUIET and state == "ok"):
            print(line)
sys.exit(1 if (CHECK and missing) else 0)

#!/usr/bin/env python3
"""tjforge install: put the enforcement pieces into the project in the current
directory. Idempotent. `--check` reports without writing and exits 1 if
anything is missing.

Installs:
  .claude/agents/tj-*.md      subagents pinned to their models
  .claude/settings.json       attribution off (commit and PR)
  .githooks/commit-msg        strips AI-attribution trailers, and is activated
  CLAUDE.md                   the tjforge block (between markers)
"""
import json
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL / "templates"
CHECK = "--check" in sys.argv
START, END = "<!-- tjforge:start -->", "<!-- tjforge:end -->"
CHAIN = '"$(git rev-parse --show-toplevel)/.githooks/commit-msg" "$1" # tjforge'

missing = 0


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


code, top = git("rev-parse", "--show-toplevel")
IS_REPO = code == 0
ROOT = Path(top) if IS_REPO else Path.cwd()


def report(state, what):
    global missing
    if state == "MISSING":
        missing += 1
    print(f"{state:8} {what}")


def sync_file(src, dst, executable=False):
    """Copy src to dst if different. Returns True when already in sync."""
    want = src.read_text()
    rel = dst.relative_to(ROOT)
    if dst.exists() and dst.read_text() == want:
        if executable and not CHECK:
            dst.chmod(0o755)
        report("ok", rel)
        return
    if CHECK:
        report("MISSING", rel)
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(want)
    if executable:
        dst.chmod(0o755)
    report("wrote", rel)


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
    if START in text and END in text:
        head, rest = text.split(START, 1)
        _, tail = rest.split(END, 1)
        new = head + block + tail
    else:
        new = (text.rstrip("\n") + "\n\n" if text.strip() else "") + block + "\n"
    if new == text:
        report("ok", "CLAUDE.md tjforge block")
    elif CHECK:
        report("MISSING", "CLAUDE.md tjforge block")
    else:
        path.write_text(new)
        report("wrote", "CLAUDE.md tjforge block")


def contract():
    for rel in ("docs/PROJECT-PROFILE.md",):
        if (ROOT / rel).exists():
            report("ok", rel)
        else:
            report("MISSING" if CHECK else "WARN", f"{rel} not written yet (run /tjforge init)")


print(f"tjforge {'check' if CHECK else 'install'}: {ROOT}")
agents()
settings()
hook()
claude_md()
contract()
sys.exit(1 if (CHECK and missing) else 0)

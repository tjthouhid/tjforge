#!/usr/bin/env bash
# tjforge quiet test wrapper. Usage: .claude/tjforge/quiet-test.sh <test command...>
# Pass: prints one PASS line with the runner's summary.
# Fail: prints the first failure in full and the summary; the whole log stays on disk.
# Exit code is the test command's. Stdin is closed so nothing waits for input.
set -u
if [ $# -eq 0 ]; then
  echo "usage: $0 <test command...>" >&2
  exit 2
fi
dir="$(cd "$(dirname "$0")" && pwd)/logs"
mkdir -p "$dir"
log="$dir/$(date +%Y%m%d-%H%M%S)-$$.log"
"$@" > "$log" 2>&1 < /dev/null
code=$?
# Summary: the last lines that look like a runner's totals.
summary="$(grep -E -i '(^|[^a-z])(tests?|passed|failed|failures?|errors?|suites?|specs?|examples?)([^a-z]|$)' "$log" | grep -E '[0-9]' | tail -n 3)"
if [ $code -eq 0 ]; then
  echo "PASS ($*)"
  [ -n "$summary" ] && echo "$summary"
  exit 0
fi
echo "FAIL exit $code ($*)"
first="$(grep -n -E -m1 '(FAIL|Error|ERROR|✗|✘|×|AssertionError|failed|Traceback|panic:)' "$log" | cut -d: -f1)"
if [ -n "$first" ]; then
  start=$(( first > 5 ? first - 5 : 1 ))
  sed -n "${start},$(( start + 60 ))p" "$log"
else
  tail -n 40 "$log"
fi
[ -n "$summary" ] && { echo "--- summary"; echo "$summary"; }
echo "--- full log: $log"
# Keep the 20 newest logs.
ls -1t "$dir"/*.log 2>/dev/null | tail -n +21 | xargs rm -f 2>/dev/null
exit $code

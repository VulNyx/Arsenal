#!/bin/bash
set -euo pipefail

script=$(cd "$(dirname "$0")" && pwd)/WPgen
testdir=$(mktemp -d)
trap 'rm -rf -- "$testdir"' EXIT
mkdir "$testdir/bin" "$testdir/work"
export PATH="$testdir/bin:$PATH"
export LISTENER_MARKER="$testdir/listener-started"
printf '#!/bin/sh\ntouch "$LISTENER_MARKER"\n' > "$testdir/bin/nc"
chmod +x "$testdir/bin/nc"
cd "$testdir/work"

printf 'existing file\n' > plugin.php
bash "$script" -l 127.0.0.1 -p 12345 > /dev/null
test "$(cat plugin.php)" = 'existing file'
test -f plugin.zip
unzip -p plugin.zip plugin.php | grep -F '/dev/tcp/127.0.0.1/12345' > /dev/null
test -f "$LISTENER_MARKER"
test -z "$(find . -maxdepth 1 -name '.wpgen.*' -print)"

printf 'existing archive\n' > plugin.zip
rm "$LISTENER_MARKER"
if bash "$script" -l 127.0.0.1 -p 12345 > /dev/null 2>&1; then
  echo 'Expected existing archive to cause an error' >&2
  exit 1
fi
test "$(cat plugin.zip)" = 'existing archive'
test "$(cat plugin.php)" = 'existing file'
test ! -e "$LISTENER_MARKER"
test -z "$(find . -maxdepth 1 -name '.wpgen.*' -print)"

rm plugin.zip
printf '#!/bin/sh\nexit 1\n' > "$testdir/bin/zip"
chmod +x "$testdir/bin/zip"
if bash "$script" -l 127.0.0.1 -p 12345 > /dev/null 2>&1; then
  echo 'Expected archive creation failure to cause an error' >&2
  exit 1
fi
test ! -e plugin.zip
test ! -e "$LISTENER_MARKER"
test "$(cat plugin.php)" = 'existing file'
test -z "$(find . -maxdepth 1 -name '.wpgen.*' -print)"
echo 'WPgen file preservation tests passed'

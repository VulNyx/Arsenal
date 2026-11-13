#!/bin/bash
set -euo pipefail

script=$(cd "$(dirname "$0")" && pwd)/ZIPcrack
testdir=$(mktemp -d)
trap 'rm -rf -- "$testdir"' EXIT
mkdir "$testdir/bin"
printf '#!/bin/sh\nexit 0\n' > "$testdir/bin/sleep"
chmod +x "$testdir/bin/sleep"
export PATH="$testdir/bin:$PATH" TERM=xterm

printf 'test content\n' > "$testdir/input"
7z a -tzip -ptestpass "$testdir/archive.zip" "$testdir/input" > /dev/null
printf 'wrong\ntestpass' > "$testdir/words"
output=$(bash "$script" -f "$testdir/archive.zip" -w "$testdir/words")
if ! grep -Fq 'Password  |' <<< "$output"; then
  echo 'Failed to find the final password without a newline' >&2
  exit 1
fi

7z a -tzip '-pcorrect horse' "$testdir/spaces.zip" "$testdir/input" > /dev/null
printf 'wrong\ncorrect horse\n' > "$testdir/words"
output=$(bash "$script" -f "$testdir/spaces.zip" -w "$testdir/words")
if ! grep -Fq 'Password  |' <<< "$output"; then
  echo 'Failed to find a password containing spaces' >&2
  exit 1
fi

cp "$testdir/archive.zip" "$testdir/archive with spaces.zip"
printf 'testpass\n' > "$testdir/words"
output=$(bash "$script" -f "$testdir/archive with spaces.zip" -w "$testdir/words")
if ! grep -Fq 'Password  |' <<< "$output"; then
  echo 'Failed to use an archive path containing spaces' >&2
  exit 1
fi

printf 'testpass\n' > "$testdir/word list"
output=$(bash "$script" -f "$testdir/archive.zip" -w "$testdir/word list" 2>&1)
if ! grep -Fq 'Password  |' <<< "$output"; then
  echo 'Failed to use a wordlist path containing spaces' >&2
  exit 1
fi
echo 'ZIPcrack tests passed'

#!/bin/bash
set -euo pipefail

script=$(cd "$(dirname "$0")" && pwd)/RSAcrack
testdir=$(mktemp -d)
trap 'rm -rf -- "$testdir"' EXIT
export TERM=xterm

ssh-keygen -q -t ed25519 -a 1 -N testpass -f "$testdir/key"
printf 'wrong\ntestpass' > "$testdir/words"
output=$(bash "$script" -k "$testdir/key" -w "$testdir/words")
if ! grep -Fq 'Password |' <<< "$output"; then
  echo 'Failed to find a passphrase on a final line without a newline' >&2
  exit 1
fi

ssh-keygen -q -t ed25519 -a 1 -N 'correct horse' -f "$testdir/space-key"
printf 'wrong\ncorrect horse\n' > "$testdir/words"
output=$(bash "$script" -k "$testdir/space-key" -w "$testdir/words")
if ! grep -Fq 'Password |' <<< "$output"; then
  echo 'Failed to find a passphrase containing spaces' >&2
  exit 1
fi

printf 'testpass\n' > "$testdir/word list"
output=$(bash "$script" -k "$testdir/key" -w "$testdir/word list" 2>&1)
if ! grep -Fq 'Password |' <<< "$output"; then
  echo 'Failed to read a wordlist path containing spaces' >&2
  exit 1
fi

cp "$testdir/key" "$testdir/key with spaces"
chmod 644 "$testdir/key with spaces"
output=$(bash "$script" -k "$testdir/key with spaces" -w "$testdir/word list")
if ! grep -Fq 'Password |' <<< "$output"; then
  echo 'Failed to use a key path containing spaces' >&2
  exit 1
fi
echo 'RSAcrack tests passed'

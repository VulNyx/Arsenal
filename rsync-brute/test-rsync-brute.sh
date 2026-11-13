#!/bin/bash
set -euo pipefail

script=$(cd "$(dirname "$0")" && pwd)/rsync-brute
testdir=$(mktemp -d)
trap 'rm -rf -- "$testdir"' EXIT
mkdir "$testdir/bin"
export PATH="$testdir/bin:$PATH"
export TERM=xterm

# Simulate a daemon with one hidden module, without opening network sockets.
cat > "$testdir/bin/rsync" <<'EOF'
#!/bin/bash
[[ $# -eq 2 && $1 == '127.0.0.1::hidden' && $2 == '--port=873' ]]
EOF
printf '#!/bin/sh\nexit 0\n' > "$testdir/bin/sleep"
chmod +x "$testdir/bin/rsync" "$testdir/bin/sleep"

printf 'missing\nhidden' > "$testdir/words"
output=$(bash "$script" -t 127.0.0.1 -p 873 -w "$testdir/words")
if ! grep -Fq 'Resource |' <<< "$output"; then
  echo 'Failed to find a module on a final line without a newline' >&2
  exit 1
fi

printf 'hidden\n' > "$testdir/word list"
output=$(bash "$script" -t 127.0.0.1 -p 873 -w "$testdir/word list" 2>&1)
if ! grep -Fq 'Resource |' <<< "$output"; then
  echo 'Failed to read a wordlist path containing spaces' >&2
  exit 1
fi

printf '\nhidden\n' > "$testdir/words"
output=$(bash "$script" -t 127.0.0.1 -p 873 -w "$testdir/words")
if ! grep -Fq '1/1/100%/hidden' <<< "$output"; then
  echo 'Progress should exclude blank lines that are not tested' >&2
  exit 1
fi
echo 'rsync-brute tests passed'

#!/usr/bin/env bash
# Full check for this docs-only repository. Exit 0 only when both pass:
#   1. the unit tests of scripts/docs.py (each check is shown to fail on a broken fixture);
#   2. the reading demo, which checks this repository's own links and round documents.
set -euo pipefail
cd "$(dirname "$0")/.."

# Python 3.9's unittest exits 0 when it collects nothing; a renamed test file must not pass.
out=$(python3 -m unittest discover -s tests -v 2>&1) || { echo "$out"; exit 1; }
echo "$out"
grep -Eq '^Ran [1-9][0-9]* tests?' <<<"$out" || { echo "FAIL: no tests ran"; exit 1; }

bash scripts/demo.sh

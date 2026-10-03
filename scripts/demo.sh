#!/usr/bin/env bash
# Reading demo. Standard-library Python only, so it runs from a fresh clone with no setup:
#   1. check every relative link and the round-document template;
#   2. print the official result table and what the team built in each round.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 scripts/docs.py check
echo
python3 scripts/docs.py summary

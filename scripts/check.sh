#!/usr/bin/env bash
# Checks this docs-only repository. Exit 0 only when both pass:
#   1. every relative link in every Markdown file resolves (file, and #anchor if given);
#   2. every round document has the six template headings, in order.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - <<'PY'
import pathlib, re, sys

ROUND_HEADINGS = ["Products", "Our hypothesis", "Strategy", "Result",
                  "Mistakes", "What top teams did"]
ROUND_DOCS = ["tutorial.md"] + [f"round-{n}.md" for n in range(1, 6)]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```.*?^```", re.S | re.M)


def slug(heading):
    s = heading.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def anchors(path):
    text = FENCE.sub("", path.read_text(encoding="utf-8"))
    return {slug(h) for h in re.findall(r"^#{1,6}\s+(.+)$", text, re.M)}


errors = []
docs = sorted(pathlib.Path(".").rglob("*.md"))
for doc in docs:
    text = FENCE.sub("", doc.read_text(encoding="utf-8"))
    for target in LINK.findall(text):
        if re.match(r"[a-z]+:", target):
            continue
        rel, _, frag = target.partition("#")
        dest = (doc.parent / rel).resolve() if rel else doc.resolve()
        if not dest.exists():
            errors.append(f"{doc}: broken link -> {target}")
        elif frag and dest.suffix == ".md" and frag not in anchors(dest):
            errors.append(f"{doc}: missing anchor -> {target}")

for name in ROUND_DOCS:
    doc = pathlib.Path("docs/rounds") / name
    if not doc.is_file():
        errors.append(f"{doc}: missing round document")
        continue
    found = re.findall(r"^##\s+(.+?)\s*$", doc.read_text(encoding="utf-8"), re.M)
    if found != ROUND_HEADINGS:
        errors.append(f"{doc}: headings {found}, expected {ROUND_HEADINGS}")

for e in errors:
    print(e)
print(f"checked {len(docs)} Markdown files and {len(ROUND_DOCS)} round documents: "
      f"{'FAIL' if errors else 'PASS'} ({len(errors)} problem(s))")
sys.exit(1 if errors else 0)
PY

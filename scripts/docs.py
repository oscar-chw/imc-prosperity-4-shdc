#!/usr/bin/env python3
"""Checks and summarises this docs-only repository (standard library only).

    python3 scripts/docs.py check [ROOT]     links resolve; round docs follow the template
    python3 scripts/docs.py summary [ROOT]   print the result table and per-round one-liners

`check` exits 1 on any broken relative link, missing #anchor or round document whose
`##` headings differ from the template. `summary` exits 1 when a README block it
prints is missing, so a renamed marker cannot turn the demo into a silent no-op.
"""
import pathlib
import re
import sys

ROUND_HEADINGS = ["Products", "Our hypothesis", "Strategy", "Result",
                  "Mistakes", "What top teams did"]
ROUND_DOCS = ["tutorial.md"] + [f"round-{n}.md" for n in range(1, 6)]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```.*?^```", re.S | re.M)
BLOCKS = ("results", "built")


def slug(heading):
    s = heading.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def anchors(path):
    text = FENCE.sub("", path.read_text(encoding="utf-8"))
    return {slug(h) for h in re.findall(r"^#{1,6}\s+(.+)$", text, re.M)}


def check(root):
    """Return a list of problems; empty means the repository is consistent."""
    root = pathlib.Path(root)
    errors = []
    docs = sorted(p for p in root.rglob("*.md") if ".git" not in p.parts)
    for doc in docs:
        text = FENCE.sub("", doc.read_text(encoding="utf-8"))
        for target in LINK.findall(text):
            if re.match(r"[a-z]+:", target):
                continue
            rel, _, frag = target.partition("#")
            dest = (doc.parent / rel).resolve() if rel else doc.resolve()
            name = doc.relative_to(root)
            if not dest.exists():
                errors.append(f"{name}: broken link -> {target}")
            elif frag and dest.suffix == ".md" and frag not in anchors(dest):
                errors.append(f"{name}: missing anchor -> {target}")
    for name in ROUND_DOCS:
        doc = root / "docs" / "rounds" / name
        if not doc.is_file():
            errors.append(f"docs/rounds/{name}: missing round document")
            continue
        found = re.findall(r"^##\s+(.+?)\s*$", doc.read_text(encoding="utf-8"), re.M)
        if found != ROUND_HEADINGS:
            errors.append(f"docs/rounds/{name}: headings {found}, expected {ROUND_HEADINGS}")
    return errors, len(docs)


def block(text, name):
    """The README text between <!-- name:start --> and <!-- name:end -->, or None."""
    m = re.search(rf"<!-- {name}:start -->\n(.*?)<!-- {name}:end -->", text, re.S)
    return m.group(1).strip() if m else None


def plain(md):
    """Markdown emphasis and links reduced to their text, for a terminal."""
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)
    return md.replace("**", "").replace("`", "")


def summary(root):
    text = (pathlib.Path(root) / "README.md").read_text(encoding="utf-8")
    parts = {name: block(text, name) for name in BLOCKS}
    missing = [n for n, body in parts.items() if not body]
    if missing:
        return None, missing
    out = ["Official result (final leaderboard):", plain(parts["results"]), "",
           "What the team built, per round:", plain(parts["built"])]
    return "\n".join(out), []


def main(argv):
    if not argv or argv[0] not in ("check", "summary") or len(argv) > 2:
        print(__doc__.strip())
        return 2
    root = argv[1] if len(argv) == 2 else pathlib.Path(__file__).resolve().parent.parent
    if argv[0] == "check":
        errors, n = check(root)
        for e in errors:
            print(e)
        print(f"checked {n} Markdown files and {len(ROUND_DOCS)} round documents: "
              f"{'FAIL' if errors else 'PASS'} ({len(errors)} problem(s))")
        return 1 if errors else 0
    text, missing = summary(root)
    if missing:
        print(f"README is missing the block(s): {', '.join(missing)}")
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

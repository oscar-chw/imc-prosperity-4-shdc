"""Tests for scripts/docs.py: a sound fixture passes, and each defect fails on its own."""
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
import docs  # noqa: E402

ROUND = "# R\n\n" + "".join(f"## {h}\n\ntext\n\n" for h in docs.ROUND_HEADINGS)
README = """# Title

<!-- results:start -->
| Track | Rank |
|---|---:|
| Overall | 904 |
<!-- results:end -->

<!-- built:start -->
- **Round 1:** [fixed value](docs/rounds/round-1.md#strategy) with `takes`
<!-- built:end -->

See [round 1](docs/rounds/round-1.md#our-hypothesis) and [home](#title).
"""


class DocsTest(unittest.TestCase):
    def fixture(self, readme=README, rounds=None, skip=()):
        root = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(root))
        (root / "docs" / "rounds").mkdir(parents=True)
        (root / "README.md").write_text(readme, encoding="utf-8")
        for name in docs.ROUND_DOCS:
            if name not in skip:
                body = (rounds or {}).get(name, ROUND)
                (root / "docs" / "rounds" / name).write_text(body, encoding="utf-8")
        return root

    def test_sound_fixture_passes(self):
        errors, n = docs.check(self.fixture())
        self.assertEqual(errors, [])
        self.assertEqual(n, 1 + len(docs.ROUND_DOCS))

    def test_broken_file_link_fails(self):
        errors, _ = docs.check(self.fixture(readme=README.replace("round-1.md#our", "round-9.md#our")))
        self.assertEqual(errors, ["README.md: broken link -> docs/rounds/round-9.md#our-hypothesis"])

    def test_missing_anchor_fails(self):
        errors, _ = docs.check(self.fixture(readme=README.replace("#our-hypothesis", "#our-guess")))
        self.assertEqual(errors, ["README.md: missing anchor -> docs/rounds/round-1.md#our-guess"])

    def test_missing_self_anchor_fails(self):
        errors, _ = docs.check(self.fixture(readme=README.replace("(#title)", "(#nowhere)")))
        self.assertEqual(errors, ["README.md: missing anchor -> #nowhere"])

    def test_external_link_is_not_resolved(self):
        errors, _ = docs.check(self.fixture(readme=README + "\n[x](https://example.org/none.md)\n"))
        self.assertEqual(errors, [])

    def test_link_inside_code_fence_is_ignored(self):
        errors, _ = docs.check(self.fixture(readme=README + "\n```\n[x](gone.md)\n```\n"))
        self.assertEqual(errors, [])

    def test_reordered_round_headings_fail(self):
        swapped = ROUND.replace("## Result\n", "## TMP\n").replace("## Strategy\n", "## Result\n") \
                       .replace("## TMP\n", "## Strategy\n")
        errors, _ = docs.check(self.fixture(rounds={"round-3.md": swapped}))
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith("docs/rounds/round-3.md: headings"))

    def test_missing_round_document_fails(self):
        errors, _ = docs.check(self.fixture(skip=("round-5.md",)))
        self.assertIn("docs/rounds/round-5.md: missing round document", errors)

    def test_summary_prints_both_blocks_as_plain_text(self):
        text, missing = docs.summary(self.fixture())
        self.assertEqual(missing, [])
        self.assertIn("| Overall | 904 |", text)
        self.assertIn("- Round 1: fixed value with takes", text)

    def test_summary_fails_when_a_block_is_missing(self):
        readme = README.replace("<!-- built:start -->", "")
        text, missing = docs.summary(self.fixture(readme=readme))
        self.assertIsNone(text)
        self.assertEqual(missing, ["built"])


if __name__ == "__main__":
    unittest.main()

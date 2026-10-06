"""Tests for scripts/docs.py: a sound fixture passes, and each defect fails on its own."""
import contextlib
import io
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

    def readme_plus(self, extra):
        return self.fixture(readme=README + extra)

    def test_hash_heading_in_code_fence_is_not_a_round_heading(self):
        body = ROUND + "```bash\n## comment\n```\n"
        errors, _ = docs.check(self.fixture(rounds={"round-3.md": body}))
        self.assertEqual(errors, [])

    def test_bare_hash_line_does_not_borrow_the_next_line(self):
        body = ROUND.replace("## Products\n", "##\nProducts\n")
        errors, _ = docs.check(self.fixture(rounds={"round-3.md": body}))
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith("docs/rounds/round-3.md: headings"))

    def test_broken_outer_link_around_image_fails(self):
        root = self.readme_plus("\n[![m](docs/rounds/round-1.md)](NOPE.md)\n")
        errors, _ = docs.check(root)
        self.assertEqual(errors, ["README.md: broken link -> NOPE.md"])

    def test_root_relative_link_resolves_against_repo_root(self):
        root = self.readme_plus("\n[a](/docs/rounds/round-1.md#strategy) [b](/docs/rounds/nope.md)\n")
        errors, _ = docs.check(root)
        self.assertEqual(errors, ["README.md: broken link -> /docs/rounds/nope.md"])

    def test_link_escaping_the_repository_fails(self):
        root = self.readme_plus("\n[a](../) [b](docs/../../)\n")
        errors, _ = docs.check(root)
        self.assertEqual(errors, ["README.md: link escapes the repository -> ../",
                                  "README.md: link escapes the repository -> docs/../../"])

    def test_query_string_and_percent_escape_are_handled(self):
        root = self.readme_plus("\n[a](docs/rounds/round-1.md?plain=1#strategy) [b](<docs/rounds/round-1.md>)"
                                "\n[c](docs/my%20file.md)\n")
        (root / "docs" / "my file.md").write_text("# x\n", encoding="utf-8")
        errors, _ = docs.check(root)
        self.assertEqual(errors, [])

    def test_duplicate_heading_gets_numbered_anchor(self):
        root = self.readme_plus("\n[x](#dup-1) [y](#dup-2)\n\n## Dup\n\n## Dup\n")
        errors, _ = docs.check(root)
        self.assertEqual(errors, ["README.md: missing anchor -> #dup-2"])

    def test_closing_hashes_and_link_heading_slug(self):
        self.assertEqual(docs.slug("Intro ##"), "intro")
        self.assertEqual(docs.slug("See [the docs](http://x.org/a-b)"), "see-the-docs")

    def test_html_anchor_is_a_valid_target(self):
        root = self.readme_plus('\n<a id="custom"></a>\n[x](#custom)\n')
        errors, _ = docs.check(root)
        self.assertEqual(errors, [])

    def test_link_inside_inline_code_is_ignored(self):
        errors, _ = docs.check(self.readme_plus("\nWrite `[t](path.md)` here.\n"))
        self.assertEqual(errors, [])

    def test_crlf_checkout_still_parses(self):
        crlf = README.replace("\n", "\r\n")
        self.assertIsNotNone(docs.block(crlf, "results"))
        root = self.fixture()
        (root / "README.md").write_bytes(crlf.encode())
        self.assertEqual(docs.check(root)[0], [])
        text, missing = docs.summary(root)
        self.assertEqual(missing, [])

    def test_main_exit_codes(self):
        good, bad = self.fixture(), self.fixture(skip=("round-5.md",))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(docs.main(["check", str(good)]), 0)
            self.assertEqual(docs.main(["check", str(bad)]), 1)
            self.assertEqual(docs.main(["summary", str(good)]), 0)
            self.assertEqual(docs.main([]), 2)


if __name__ == "__main__":
    unittest.main()

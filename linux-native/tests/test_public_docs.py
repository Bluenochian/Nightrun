"""Public docs should describe the software, not the development conversation."""
from pathlib import Path
import re
import unittest


REPOSITORY = Path(__file__).resolve().parents[2]
PUBLIC = (
    "README.md",
    "docs/WINDOWS_GUIDE.md",
    "linux-native/README.md",
    "linux-native/GUIDE.md",
    "linux-native/RELEASE_NOTES.md",
)


class DocumentationTests(unittest.TestCase):
    def test_public_docs_do_not_link_to_removed_release(self):
        for filename in PUBLIC:
            text = (REPOSITORY / filename).read_text(encoding="utf-8")
            with self.subTest(file=filename):
                self.assertNotIn("/releases/tag/v2.3", text)

    def test_public_docs_use_the_author_voice_not_backstage_commentary(self):
        backstage = re.compile(
            r"\bwe\b|\bclaude\b|\bretir(?:ed|ing)\b|"
            r"\b(the assistant|chatgpt helped|ai detector)\b",
            re.IGNORECASE,
        )
        for filename in PUBLIC:
            text = (REPOSITORY / filename).read_text(encoding="utf-8")
            with self.subTest(file=filename):
                self.assertIsNone(backstage.search(text))

    def test_both_guides_are_linked_and_shipped(self):
        homepage = (REPOSITORY / "README.md").read_text(encoding="utf-8")
        self.assertIn("linux-native/GUIDE.md", homepage)
        self.assertIn("docs/WINDOWS_GUIDE.md", homepage)
        builder = (REPOSITORY / "linux-native/build.py").read_text(encoding="utf-8")
        installer = (REPOSITORY / "linux-native/install.sh").read_text(encoding="utf-8")
        self.assertIn('"GUIDE.md"', builder)
        self.assertIn("GUIDE.md", installer)


if __name__ == "__main__":
    unittest.main()

"""Verify the checker catches actual token/control/link regressions."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("package_validator", ROOT / "tools" / "validate.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class PackageRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__', '.agents', '.claude'))

    def tearDown(self):
        self.temp.cleanup()

    def fails(self, name):
        return any(item['check'] == name and not item['passed'] for item in validator.validate(self.root))

    def test_clean_package(self):
        self.assertTrue(all(item['passed'] for item in validator.validate(self.root)))

    def test_changed_path(self):
        p = self.root / 'examples' / 'rtl-web.html'
        p.write_text(p.read_text(encoding='utf-8').replace('C:\\Projects\\demo\\config.json', 'C:\\Projects\\demo\\changed.json'), encoding='utf-8')
        self.assertTrue(self.fails('web-token:path'))

    def test_hidden_control_in_code(self):
        p = self.root / 'examples' / 'rtl-web.html'
        p.write_text(p.read_text(encoding='utf-8').replace('payload =', 'payload\u200f ='), encoding='utf-8')
        self.assertTrue(self.fails('web-token-no-controls:code'))

    def test_broken_reference(self):
        p = self.root / 'skills' / 'persian-output-skill' / 'references' / 'writing.md'
        p.unlink()
        self.assertTrue(self.fails('link:skills\\persian-output-skill\\SKILL.md:references/writing.md') or self.fails('link:skills/persian-output-skill/SKILL.md:references/writing.md'))


if __name__ == '__main__':
    unittest.main()

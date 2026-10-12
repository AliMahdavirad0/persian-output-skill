import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('html_audit', ROOT / 'skills/persian-output-skill/scripts/audit_html.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

BASE = '<html lang="en"><body><div dir="ltr"><p>Hello <code>v2.1</code></p><img src="a.svg" width="100" alt="A"><a href="/docs">Read</a><script>start()</script></div></body></html>'
FA = BASE.replace('lang="en"', 'lang="fa"').replace('<p>Hello', '<p dir="rtl">سلام').replace('alt="A"', 'alt="تصویر"').replace('>Read<', '>بخوانید<')


class HTMLAuditTests(unittest.TestCase):
    def test_text_and_direction_changes_allowed(self):
        self.assertTrue(module.audit(BASE, FA)['passed'])

    def test_asset_or_geometry_change_rejected(self):
        for changed in [FA.replace('a.svg', 'b.svg'), FA.replace('width="100"', 'width="80"')]:
            self.assertFalse(module.audit(BASE, changed)['passed'])

    def test_link_change_rejected(self):
        self.assertFalse(module.audit(BASE, FA.replace('/docs', '/other'))['passed'])

    def test_script_or_code_change_rejected(self):
        for changed in [FA.replace('start()', 'restart()'), FA.replace('v2.1', 'v۲.۱')]:
            self.assertFalse(module.audit(BASE, changed)['passed'])

    def test_removed_picture_rejected(self):
        self.assertFalse(module.audit(BASE, FA.replace('<img src="a.svg" width="100" alt="تصویر">', ''))['passed'])

    def test_markup_change_is_conservatively_flagged(self):
        self.assertFalse(module.audit(BASE, FA.replace('سلام', '<strong>سلام</strong>'))['passed'])

    def test_do_not_translate_region(self):
        a = '<p translate="no">Original quote</p>'
        self.assertFalse(module.audit(a, a.replace('Original', 'New'))['passed'])


if __name__ == '__main__':
    unittest.main()

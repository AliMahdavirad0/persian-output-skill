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

    def test_layout_direction_is_not_a_text_change(self):
        self.assertFalse(module.audit(BASE, FA.replace('<div dir="ltr">', '<div dir="rtl">'))['passed'])

    def test_code_direction_is_preserved(self):
        source = '<pre dir="ltr"><code>value=3.14</code></pre>'
        self.assertFalse(module.audit(source, source.replace('dir="ltr"', 'dir="rtl"'))['passed'])

    def test_nontranslatable_attributes_are_frozen(self):
        source = '<p translate="no" title="Original">Quote</p>'
        self.assertFalse(module.audit(source, source.replace('title="Original"', 'title="Changed"'))['passed'])

    def test_inherited_nontranslatable_attributes(self):
        source = '<div translate="no"><img src="a.svg" alt="Original"></div>'
        self.assertFalse(module.audit(source, source.replace('alt="Original"', 'alt="Changed"'))['passed'])

    def test_explicit_translate_yes_overrides_inheritance(self):
        source = '<div translate="no">Fixed <span translate="yes" title="Hello">Hello</span></div>'
        translated = source.replace('title="Hello"', 'title="سلام"').replace('>Hello<', '>سلام<')
        self.assertTrue(module.audit(source, translated)['passed'])

    def test_direction_of_text_with_inline_media_is_frozen(self):
        source = '<p dir="ltr">Hello <img src="a.svg"></p>'
        translated = source.replace('Hello', 'سلام').replace('dir="ltr"', 'dir="rtl"')
        self.assertFalse(module.audit(source, translated)['passed'])

    def test_invalid_translate_value_inherits(self):
        source = '<div translate="no"><span translate=" no " title="Original">Quote</span></div>'
        self.assertFalse(module.audit(source, source.replace('title="Original"', 'title="Changed"'))['passed'])
        source = '<span translate=" no " title="Original">Hello</span>'
        translated = source.replace('title="Original"', 'title="سلام"').replace('>Hello<', '>سلام<')
        self.assertTrue(module.audit(source, translated)['passed'])


if __name__ == '__main__':
    unittest.main()

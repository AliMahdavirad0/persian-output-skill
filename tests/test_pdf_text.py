import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('pdf_audit', ROOT / 'skills/persian-output-skill/scripts/audit_pdf_text.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PDFTextComparisonTests(unittest.TestCase):
    def test_line_wrapping_whitespace(self):
        self.assertTrue(module.compare_text('مدل‌های NARMAX', 'مدل‌های\n NARMAX'))

    def test_lost_joiner_is_rejected(self):
        self.assertFalse(module.compare_text('مدل‌های', 'مدلهای'))

    def test_presentation_forms_are_not_normalized_away(self):
        self.assertFalse(module.compare_text('شناسایی', 'ﺷﻨﺎﺳﺎﯾﯽ'))

    def test_mixed_citation_order_is_checked(self):
        self.assertFalse(module.compare_text('(Ljung, 1987)', '(1987, Ljung)'))

    def test_combining_mark_is_not_discarded(self):
        self.assertFalse(module.compare_text('حوزهٔ', 'حوزه'))


if __name__ == '__main__':
    unittest.main()

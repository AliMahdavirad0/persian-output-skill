import importlib.util
import json
from pathlib import Path
import unittest

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'evals/performance/real-pdf-searchable.pdf'
EXPECTED = json.loads((ROOT / 'evals/performance/pdf-text-expectations.json').read_text(encoding='utf-8'))
spec = importlib.util.spec_from_file_location('pdf_audit', ROOT / 'skills/persian-output-skill/scripts/audit_pdf_text.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ScientificPDFFixtureTests(unittest.TestCase):
    def test_all_eight_regions_copy_in_mupdf(self):
        result = module.audit(FIXTURE, EXPECTED)
        self.assertTrue(result['passed'], result)

    def test_pdfium_search_including_joiners(self):
        result = module.audit(FIXTURE, EXPECTED, 'pdfium')
        self.assertTrue(all(x['passed'] for x in result['search']), result['search'])
        # Full PDFium mixed-citation copy remains explicitly unverified.

    def test_figure_pixels_and_coordinates(self):
        reference = json.loads((ROOT / 'evals/performance/real-pdf-results.json').read_text(encoding='utf-8'))['images_before'][3][1]
        with pymupdf.open(FIXTURE) as doc:
            self.assertEqual(len(doc), 6)
            figure = doc[3].get_image_info(hashes=True)[1]
            self.assertEqual(figure['digest'].hex(), reference['digest'])
            self.assertEqual(list(figure['bbox']), reference['bbox'])
            self.assertEqual((figure['width'], figure['height']), (reference['width'], reference['height']))

    def test_persian_text_has_no_presentation_forms(self):
        with pymupdf.open(FIXTURE) as doc:
            for region in EXPECTED['regions']:
                text = doc[region['page'] - 1].get_textbox(pymupdf.Rect(region['rect']))
                self.assertFalse(any(0xFB50 <= ord(c) <= 0xFDFF or 0xFE70 <= ord(c) <= 0xFEFF for c in text))


if __name__ == '__main__':
    unittest.main()

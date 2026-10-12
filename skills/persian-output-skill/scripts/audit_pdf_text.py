"""Read-only PDF copy/search checks against explicit expected regions.

Requires PyMuPDF; PDFium mode also requires pypdfium2. A passing renderer
does not establish compatibility with other readers. No Unicode normalization
or removal of joiners/marks is performed. Only whitespace from line wrapping
is ignored in region comparisons; inspect actual clipboard behavior separately.
"""
import argparse
import json
from pathlib import Path
import re


def compare_text(expected, actual):
    return re.sub(r'\s+', '', expected) == re.sub(r'\s+', '', actual)


def audit(path, expectations, engine='mupdf'):
    if engine == 'mupdf':
        import pymupdf as pdf
        doc = pdf.open(path)
    else:
        import pypdfium2 as pdf
        doc = pdf.PdfDocument(path)
    result = {'engine': engine, 'regions': [], 'search': []}
    try:
        for region in expectations['regions']:
            page = doc[region['page'] - 1]
            rect = region['rect']
            if engine == 'mupdf':
                actual = page.get_textbox(pdf.Rect(rect))
            else:
                tp = page.get_textpage()
                height = page.get_height()
                actual = tp.get_text_bounded(rect[0], height - rect[3], rect[2], height - rect[1])
                tp.close()
            result['regions'].append({'id': region['id'], 'passed': compare_text(region['text'], actual), 'actual': actual})
        for token in expectations['search']:
            found = False
            for index in range(len(doc)):
                page = doc[index]
                if engine == 'mupdf':
                    found = found or bool(page.search_for(token))
                else:
                    tp = page.get_textpage()
                    searcher = tp.search(token)
                    found = found or searcher.get_next() is not None
                    searcher.close()
                    tp.close()
            result['search'].append({'text': token, 'passed': found})
        result['passed'] = all(x['passed'] for x in result['regions'] + result['search'])
        result['limit'] = 'Region text is checked modulo whitespace only; this is not a native clipboard test or a guarantee for other readers.'
        return result
    finally:
        doc.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('expected', type=Path)
    parser.add_argument('--engine', choices=['mupdf', 'pdfium'], default='mupdf')
    args = parser.parse_args()
    try:
        result = audit(args.pdf, json.loads(args.expected.read_text(encoding='utf-8')), args.engine)
    except (ImportError, OSError, ValueError) as error:
        parser.exit(2, str(error) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['passed'] else 1)

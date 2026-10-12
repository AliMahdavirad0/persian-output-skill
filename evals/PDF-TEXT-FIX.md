# PDF Unicode repair — v0.2.2

The original eight-region scientific article test failed Persian Unicode search. The [repaired PDF](performance/real-pdf-searchable.pdf) preserves the reviewed Vazirmatn Light appearance as vector outlines in translated regions, with one invisible selectable Unicode text layer in the same regions. Original pages, images, code, math, numeric table content and links remain native. No page or figure is rasterized. See [article/font attribution](performance/NOTICE.md).

The repair emits glyphs in logical text order with bidi coordinates and `ToUnicode` mappings, including dedicated glyph cells for ZWNJ and combining hamza. The earlier broken visible text layer is absent, so extracted text is not duplicated. [Measured results](performance/pdf-text-layer-results.json) and [exact expectations](performance/pdf-text-expectations.json) are included.

Verified on 2026-10-12:

- **MuPDF 1.28.2:** all eight region copy/extraction comparisons pass modulo whitespace from PDF line wrapping. The extraction includes extra breaks, sometimes inside words; comparison removes whitespace, so this is character fidelity rather than a pristine clipboard round trip. No other characters are normalized or discarded: joiners, combining marks, technical tokens, punctuation and English citations match the source translation. Seven search tokens pass, including `مدل‌سازی`, `شبیه‌سازی` and `مدل‌های`.
- **PDFium 156.0.8076.0 / pypdfium2 5.14.0:** the same seven search tokens pass. Three of eight complete region-copy comparisons pass; mixed citations, parentheses and reading order still differ in this engine. This is recorded as a remaining compatibility limitation, not counted as passing.
- All six final pages were rendered and visually inspected. Figure 1's pixels and exact rectangle, other images versus the previous version, URI links, the complete code page and both reference pages match. Font appearance and physical right alignment are preserved.
- Native clipboard behavior in Acrobat, Chrome or the Codex preview was not exercised. A tested extraction engine is not proof for every PDF reader. The article remains a partial translation of eight selected regions.

The logical Unicode/presentation-form failure is repaired for the tested MuPDF copy path, and Persian search is repaired in both tested engines. **Full copy compatibility with every PDF reader is not claimed.**

## Reproduce

Install the optional dependencies in an isolated environment:

```text
python -m pip install PyMuPDF==1.28.2 python-bidi==0.6.11 pypdfium2==5.14.0
python -X utf8 examples/rebuild_pdf_text_fixture.py --source source.pdf --font Vazirmatn-Light.ttf --output rebuilt.pdf
python -X utf8 skills/persian-output-skill/scripts/audit_pdf_text.py rebuilt.pdf evals/performance/pdf-text-expectations.json
python -X utf8 skills/persian-output-skill/scripts/audit_pdf_text.py rebuilt.pdf evals/performance/pdf-text-expectations.json --engine pdfium
```

The second audit intentionally exits nonzero for the recorded PDFium copy differences; its search subchecks pass. This must not be suppressed as a universal pass.

Provide the local [original paper PDF](https://joss.theoj.org/papers/10.21105/joss.02384.pdf) and [Vazirmatn-Light.ttf v33.003](https://github.com/rastikerdar/vazirmatn/blob/v33.003/fonts/ttf/Vazirmatn-Light.ttf). The rebuild example checks the source hash and has explicit regions for this paper only; it is not a general article converter. Render and review any regenerated output.

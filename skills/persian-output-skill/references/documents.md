# Word and PDF

## Word

Set paragraph base direction to RTL as well as the desired alignment. Apply it to headings, body paragraphs, list paragraphs, headers/footers, and Persian paragraphs inside cells. Set table direction so the first logical column appears on the intended side. Keep purely technical paragraphs LTR and left-aligned.

For OOXML-based authoring, these properties are distinct:

- `w:pPr/w:bidi` controls the paragraph's bidi layout.
- `w:pPr/w:jc` controls alignment.
- `w:tblPr/w:bidiVisual` controls table visual direction.
- `w:rPr/w:rtl` is run formatting; use it on Persian runs, not blindly on all runs.
- `w:rFonts/@w:cs`, `w:szCs`, and `w:lang/@w:bidi` support complex-script font, size, and language settings.

Split Persian prose and technical tokens into separate logical runs when needed. An LTR technical run should explicitly avoid inherited RTL run formatting. Do not assume `python-docx` right alignment alone sets RTL. Keep hyperlink targets unchanged and set their display runs appropriately. Preserve an existing document's unrelated styles, fields, and layout.

Example helper, with `python-docx` already available:

```python
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_paragraph_direction(paragraph, rtl=True):
    props = paragraph._p.get_or_add_pPr()
    node = props.find(qn("w:bidi"))
    if node is None:
        node = OxmlElement("w:bidi")
        props.append(node)
    node.set(qn("w:val"), "1" if rtl else "0")
    alignment = props.find(qn("w:jc"))
    if alignment is None:
        alignment = OxmlElement("w:jc")
        props.append(alignment)
    alignment.set(qn("w:val"), "start")
```

Use logical `w:jc="start"` so alignment follows the paragraph direction; check how the target renderer handles it. Numeric dates contain no strong LTR letters, so separate runs with `w:rtl="0"` alone may still render date groups in reverse order. If the target renderer does that, place the unchanged token in its own LTR paragraph or LTR table-cell paragraph; do not reverse the token or add hidden characters. For titles, avoid direct body-size overrides and keep the style\'s `w:szCs` consistent with `w:sz`.

This helper is only a paragraph-direction building block, not a complete document renderer. Check generated OOXML and exact token text, then render every page through Word/LibreOffice or another capable renderer. Inspect glyph connection, numbers, punctuation, table order, page breaks, and clipping. Without a renderer, say **structurally checked; visual layout unverified**.

## PDF

Choose a pipeline that supports Persian glyph shaping and bidi: a capable browser print engine, Word/LibreOffice export, or a tested complex-text typesetting stack. A generic draw-string API with an Arabic font alone is insufficient. Do not reverse the whole paragraph, rasterize all text to hide errors, or run a bidi transformation twice.

Font availability, font embedding permission, shaping, layout, and extraction are separate concerns. If a library requires pre-shaped visual glyph strings, apply that only at its rendering boundary; preserve logical source text and report any search/copy limitation. Keep code and URL strings untransformed.

Render the exported PDF to page images and inspect every page. Separately extract/copy important tokens and verify links. A visually correct PDF may still have faulty text extraction; do not claim searchable Persian unless tested. If tools or font support are missing, deliver usable source with the exact limitation rather than claim the PDF is verified.

OOXML references: [paragraph bidi](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.bidirectional), [table direction](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.bidivisual).

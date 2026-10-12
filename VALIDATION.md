# Validation evidence

## Version 0.2.0 follow-up

The 0.2.0 extension is based on upstream commit `099a27d`. The Word builder, Word regression tests, committed before/after artifacts and alignment/date fixes are preserved. All 15 repository regression tests pass, including the four upstream Word tests and seven new static HTML audit tests. The package checker passes with the translation data, references, authored article fixture and evaluation files included.

Twenty authored translation examples, 30 contextual glossary seeds and 12 evaluation prompts are packaged. The first two prompts were tested with and without the skill; both configurations preserved the declared protected content. No naturalness uplift is claimed. The third with-skill test originally timed out; its source-only retry completed, with the limitation recorded in [the pilot report](evals/BENCHMARK.md).

The paired article demo was visually inspected on desktop and 390px mobile. Its image asset, exact image rectangle, source structure, link/code content and lack of page overflow were checked; raw values are in [geometry evidence](examples/layout-preservation/geometry-evidence.json). This is one static authored example, not proof of arbitrary site/Word/PDF layout-preserving translation.

Word visual evidence from the upstream Linux run remains valid as recorded below; no fresh Windows Word/LibreOffice render was performed for this extension. Claude Code still requires authentication for actual invocation testing. Specialized guidance now includes Word/PDF article translation and its source/OCR/rendering prerequisites; no universal converter is bundled.

## Initial package evidence

This file records performed checks, not guarantees for all models or renderers.

Checked on 2026-10-12 on Windows. Evidence separates format compatibility from agent/runtime support.

| Check | Result | Evidence / limit |
| --- | --- | --- |
| Package checker | PASS | 45 final checks: required metadata, relative links, no hidden bidi controls, exact fixture tokens, HTML language/direction, MIT license |
| Checker regression tests | PASS | Four tests: clean package, changed path, hidden bidi control in code, and missing reference |
| Creator validator | PASS | Bundled `quick_validate.py`, UTF-8 mode, PyYAML parser |
| YAML metadata | PASS | Parsed frontmatter and `agents/openai.yaml`; automatic invocation enabled |
| Project installation | PASS | Complete folder copied to isolated `.agents/skills` and `.claude/skills`; file hashes matched |
| Codex invocation | PASS | Actual `$persian-output-skill` invocation discovered the project skill and loaded writing/direction references |
| Codex preservation | PASS | Authored Persian corrected; Arabic quotation, version, date, Windows path, URL and JSON snippet unchanged; no added bidi controls |
| Claude Code invocation | NOT RUN | Installed CLI 2.1.159 reports not logged in; no claim of runtime behavior |
| Web visual review | PASS | Desktop and 390px mobile screenshots inspected; joined glyphs, RTL paragraphs/list/table, LTR code; no page overflow |
| Web technical text | PASS | Browser DOM text and link target match exact source tokens; no hidden controls in tokens |
| Word structure | PASS | Generated fixture has paragraph `w:bidi`, table `w:bidiVisual`, split RTL/LTR runs, exact technical text and hyperlink target |
| Word visual review | BLOCKED | Packaged renderer attempted; `soffice.exe` unavailable. Generated Word fixture is not presented as visually verified |
| PDF visual review | PASS | One-page QA fixture rendered through Poppler and inspected after table padding correction |
| PDF technical extraction | PASS | Exact version, date, decimal, path, code and URL extracted; link annotation target checked |
| Persian PDF search/copy | NOT CLAIMED | QA pipeline pre-shapes Persian at the rendering boundary; technical tokens stay logical, but searchable Persian was not established |
| Behavioral scenarios | PARTIAL | One actual Codex prose/preservation smoke test; remaining scenarios are supplied for further evaluation, not counted as passing |

The Word builder is included for reproduction; its output still needs visual review in a capable renderer. PDF visual testing used ReportLab 4.4.9, arabic-reshaper 3.0.1, python-bidi 0.6.11, local Tahoma/Consolas fonts and Poppler. Fonts are not redistributed. The PDF fixture was a QA artifact rather than a universal PDF export engine.

An initial Windows shell read displayed corrupted Persian examples due to encoding. The skill now explicitly requires UTF-8 reads on such environments; the successful model output preserved the required content. Package parsing was rerun with UTF-8.

## Reproduce

```text
python -X utf8 tools/validate.py
python -X utf8 -m unittest discover -s tests -p "test_*.py"
python -X utf8 examples/build_docx.py --output sample.docx
```

For agent testing, install the complete folder in a fresh project and run [the scenarios](tests/scenarios.md). Review every rendered page for actual Word/PDF tasks; no structural validator replaces that review.

## Word fixture follow-up on 2026-10-12

The original Windows Word visual check above was blocked. A later Linux run used python-docx 1.2.0 and the packaged LibreOffice renderer, then inspected the complete one-page before/after outputs. This exposed physical alignment being interpreted incorrectly in RTL paragraphs and a reversed inline numeric date. The builder now uses logical `w:jc="start"`, style-sized titles with matching complex-script size, and native LTR cell paragraphs for dates and technical values. The date is visibly `2026-10-12`; Persian paragraphs, bullets, and table labels align on the right. The decorative title border was removed.

The screenshots and DOCX files are linked from both READMEs. Four Word regression tests cover title-size inheritance, paragraph direction/alignment, native LTR date cells, and protected technical tokens/hyperlinks. Technical tokens were also extracted from the rendered PDF and compared with the source; PDF date-group positions were checked in increasing left-to-right order. This is a LibreOffice fixture check, not Microsoft Word runtime testing, a general bidi guarantee, or an agent behavior benchmark. Persian PDF extraction remains outside the claims above.

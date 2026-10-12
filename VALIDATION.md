# Validation evidence

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

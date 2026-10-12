# Acceptance checks

Choose checks appropriate to the requested artifact. Review writing without changing protected content, then review direction in the actual destination.

| Scenario | Observable expectation |
| --- | --- |
| Persian paragraph | Natural wording, joined glyphs, intended base direction |
| English term and parentheses | Term and parentheses stay together; logical source unchanged |
| Version / port / decimal | Exact ASCII token preserved |
| Date | Original calendar and value preserved |
| List | Markers and indentation follow reading order |
| Table | Headers match values; intended first column on the right |
| URL / email / Windows path | Exact copied text; no added bidi controls inside it |
| Code block | LTR presentation; executable text unchanged |
| Unicode workaround | Minimal, scoped controls; paired isolates; no override controls |
| Word / PDF | All pages inspected; no clipping, tofu glyphs, disconnected letters, or overlapping text |

Check technical tokens at the source level and by extraction/copy where available. Check appearance visually; structural checks alone cannot prove it. Include a narrow-width web view and at least one multiline mixed-direction paragraph.

## Reporting

Use accurate evidence labels: **source preserved**, **structure checked**, **rendered and visually inspected**, **agent invocation tested**. Mark unavailable checks explicitly. Running a YAML validator does not prove writing behavior or skill discovery in either agent.

Do not expand a small text-edit task into generating every format. This checklist is for the requested output, not a mandate to create extra deliverables.

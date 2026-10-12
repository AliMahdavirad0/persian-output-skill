---
name: persian-output-skill
description: Write or edit Persian prose and fix Persian mixed-direction output in chat, HTML, Word, and PDF. Use when Persian writing quality or RTL presentation is part of the requested deliverable. Do not activate merely because a technical task contains a Persian word, filename, or identifier.
---

# Persian Output | خروجی فارسی

Deliver natural Persian with correct direction for the destination. Follow the user's language, tone, spelling convention, numeral preference, and output format. This skill supplements the current task; it does not translate unrelated content or authorize publishing, installing tools, or changing settings.

## Choose the route

Read only the reference needed for the current output:

- Prose composition or editing: [Persian writing](references/writing.md).
- Chat, Markdown, plain text, or invisible Unicode marks: [Text direction](references/text-direction.md).
- HTML, CSS, or a web interface: [Web RTL](references/web.md).
- Word or PDF: [Documents](references/documents.md).
- Final review or a mixed-format task: [Acceptance checks](references/quality.md).

For a writing-and-formatting task, combine the writing reference with the destination reference. Instructions are tool-independent; use the authoring tools already available. Never require a named plugin.

All package files are UTF-8. On Windows, read references with an explicit UTF-8 encoding (for example `Get-Content -Encoding utf8`); run Python helpers with `python -X utf8` when the environment defaults to a legacy encoding. If Persian examples appear as question marks or replacement glyphs in tool output, correct decoding before relying on that text.

## Shared invariants

1. Preserve meaning, facts, uncertainty, names, units, calendar, and commitments. Do not invent source material to make prose sound finished.
2. Match the audience. Default to clear natural Persian in conversation and restrained professional Persian in documents. Preserve intentional colloquial wording.
3. In newly authored Persian prose, use Persian ی/ک, appropriate نیم‌فاصله (U+200C), and Persian punctuation. Do not run global replacements over the whole artifact.
4. Keep quotes, code, URLs, emails, paths, commands, identifiers, checksums, and structured data exact unless the user specifically asks to edit them. Direction belongs to the surrounding presentation.
5. Keep technical numbers machine-readable. Do not silently convert dates between calendars, replace numeric decimal separators, or convert currency units. Respect requested digit style in human prose.
6. Use native direction metadata when available. Right alignment alone does not establish RTL. Do not prepend invisible marks everywhere or use RLO/LRO to force visual order.
7. Check both displayed output and copied technical tokens. A screenshot proves appearance only; source checks prove preservation only. Report what was actually verified.

## Completion

Deliver the requested output without narrating every correction. If the destination renderer or font support is missing, preserve usable source and state the concrete unverified part. Never label Word/PDF visually correct without viewing rendered pages. When the user asks about a Unicode mark, identify its code point and scope instead of inserting unexplained controls.

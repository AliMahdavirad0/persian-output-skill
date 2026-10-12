# Plain text, Markdown, and Unicode

Unicode strings stay in logical reading order. Do not reverse Persian characters manually. ZWNJ changes joining; RLM changes bidi context. They solve different problems.

## Destination first

Use the renderer's direction setting if available. Ordinary Persian-leading paragraphs often display correctly without any mark. Markdown alignment and bidi handling differ across hosts; a skill cannot guarantee how every chat client lays out a paragraph.

When a plain-text paragraph is visibly misdirected and native metadata is unavailable, a single leading RLM (U+200F, RIGHT-TO-LEFT MARK) may establish a strong RTL character. Add it only to the affected prose paragraph, outside a list marker or code fence, and verify the destination. It does not set right alignment or isolate every English fragment. Do not insert it into link targets, filenames, code, CSV/JSON values, or commands.

For an embedded opposite-direction phrase in plain text, prefer paired isolates when the renderer supports them: LRI U+2066 for known LTR text; RLI U+2067 for RTL text; FSI U+2068 when direction is unknown; terminate each with PDI U+2069. Keep controls outside the token, disclose them when copy fidelity matters, and avoid them altogether in machine-readable output. Prefer HTML markup in HTML.

Do not use RLO U+202E or LRO U+202D. Avoid legacy RLE U+202B/LRE U+202A embedding as a routine workaround. Balanced isolates still require destination testing.

## Copyable technical content

- Use code spans for short tokens and separate code blocks for commands. They improve readability, but some Markdown clients still need a native LTR block setting.
- Put a long path or command on its own line rather than surrounding it with punctuation and invisible marks.
- Keep a Markdown URL destination byte-for-byte intact. A descriptive Persian link label may be edited independently.
- Use simple lists or separate lines if a Markdown table makes mixed text harder to read.

## Inspect invisible characters

Represent marks visibly in documentation: `\u200f`, `\u2066`, `\u2069`. For actual use, explain the code point if asked. To inspect a suspicious string without changing it:

```python
import unicodedata
for i, ch in enumerate(text):
    if unicodedata.category(ch) == "Cf":
        print(i, f"U+{ord(ch):04X}", unicodedata.name(ch, "UNKNOWN"))
```

Report unexpected controls; do not silently strip every format character, because legitimate ZWNJ and intended isolates may exist.

Source: [Unicode bidi FAQ](https://unicode.org/faq/bidi.html), [UAX #9](https://www.unicode.org/reports/tr9/).

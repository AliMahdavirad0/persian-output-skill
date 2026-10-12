# نگارش فارسی

## Voice and meaning

Use familiar words, concrete verbs, and sentences that follow the reader's train of thought. Shorten unnecessary ceremonial language, but preserve the author's register. A chat may say «می‌تونی»; a formal letter may say «می‌توانید». Neither is a universal replacement for the other. Keep established domain terminology and explain unfamiliar terms only when useful.

Do not turn a tentative claim into a certainty, an estimate into an exact number, or a suggestion into a commitment. In source-grounded writing, request missing material when essential facts cannot be derived.

## Orthography

- Use ی U+06CC and ک U+06A9 in newly authored Persian prose; preserve Arabic quotations and protected tokens.
- Use ZWNJ U+200C at meaningful word boundaries: «می‌شود»، «نمی‌توان»، «کتاب‌ها». It is not a space, a direction mark, or a universal joining repair. Do not insert it into names, every compound, or code by pattern alone.
- Prefer «،»، «؛»، «؟» and «گیومه» in Persian prose. Use punctuation appropriate to English passages within it.
- No space before sentence punctuation; normally one space after it. Keep punctuation adjacent to the relevant phrase, not inside a URL.
- Do not remove intentional diacritics, normalize verbatim quotes, or change proper-name spellings without authorization.

## Numbers and dates

Follow an explicit user convention. Otherwise preserve source digits when editing; Persian digits are reasonable in newly authored human prose, ASCII digits in executable or structured material. Keep version strings, ports, API fields, and formulas exact. Preserve the source calendar and unit: 2026-10-12 must not become a guessed Solar Hijri date. Currency labels must make تومان versus ریال explicit when that distinction matters.

## Examples

| Input | Edited prose | Protected content |
| --- | --- | --- |
| اين گزارش ميتواند كامل تر باشد. | این گزارش می‌تواند کامل‌تر باشد. | None |
| فايل config.json را تغيير بده. | فایل `config.json` را تغییر بده. | `config.json` |
| نسخه v2.1.0 در پورت 8080 اجرا ميشود. | نسخهٔ `v2.1.0` روی پورت `8080` اجرا می‌شود. | Version and port |

These examples demonstrate editing decisions; they are not a global replacement algorithm.

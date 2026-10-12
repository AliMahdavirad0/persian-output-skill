# Before and after

## Prose

Before: `اين فايل ها ميتوانند به روز شوند، آيا ادامه ميدهيد?`

After: این فایل‌ها می‌توانند به‌روز شوند؛ آیا ادامه می‌دهید؟

This edits authored prose. It does not authorize editing a quote containing the same characters.

## Mixed technical content

Before: نسخه v2.1.0 در مسیر C:\Projects\demo\config.json است.

After: نسخهٔ `v2.1.0` در مسیر `C:\Projects\demo\config.json` است.

The token characters are unchanged. In HTML, wrap them in `bdi dir="ltr"`; in plain Markdown, check the host renderer.

## Dates and quantities

Input: آزمون در `2026-10-12` انجام شد؛ مقدار `3.14` در خروجی JSON ثبت شد.

Expected: keep both technical tokens and the calendar unchanged. Do not convert to Persian digits inside JSON.

## A direction defect

Input: a plain-text Persian paragraph begins with an English version and the host gives it LTR layout.

First fix: use native RTL metadata if available, or put the technical token on a separate line. If unavailable and a leading strong RTL mark resolves the observed issue, prefix only the affected prose with `\u200f` (notation here; not a literal instruction to print the six characters).

Do not prefix every paragraph, code fence, or link with invisible marks.

## Protected code

This stays exact:

```python
payload = {"version": "v2.1.0", "amount": 3.14, "path": r"C:\Projects\demo\config.json"}
```

## Negative activation

Request: “Fix the failing test in `گزارش.py`.”

Expected: perform the coding task. A Persian filename alone is not a reason to invoke this writing/RTL skill.

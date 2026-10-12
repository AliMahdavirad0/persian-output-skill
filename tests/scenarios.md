# Behavioral evaluation scenarios

Run in a fresh session with the installed skill. Evaluate observable outputs, not specific wording. These scenarios are not an automated model benchmark.

| ID | Request / setup | Pass criteria |
| --- | --- | --- |
| P01 | Edit «اين فايل ها ميتوانند تغيير كنند.» | Natural Persian ی/ک and meaningful ZWNJ; same meaning |
| P02 | Keep a conversational message casual | No forced formal letter wording |
| P03 | Edit a paragraph containing a verbatim Arabic quote | Quote unchanged |
| B01 | Persian-leading mixed paragraph with `v2.1.0 (beta)` | Version intact, punctuation readable |
| B02 | Persian paragraph with `2026-10-12` and `3.14` | No calendar/unit conversion; technical digits intact |
| B03 | Plain text is already displayed correctly | No blanket invisible-mark insertion |
| B04 | English-leading paragraph visibly misdirected | Native direction preferred; minimal workaround if needed, destination checked |
| B05 | User explicitly requests a leading Unicode mark | Identify code point; scope to prose, keep machine tokens intact |
| W01 | Build Persian HTML with unknown-direction user name | `lang`/`dir`, isolated unknown text, escaped text binding |
| W02 | Long Windows path, URL, code at 390px width | No page overflow; copied tokens exact; code LTR |
| D01 | Create a Persian Word table with code | RTL paragraphs/table; separate LTR code; render before visual claim |
| D02 | PDF generation tool lacks Persian shaping | Choose capable pipeline or report concrete limitation |
| D03 | Renderer unavailable | Preserve source; no claim of visually verified output |
| N01 | Fix failing code in a Persian-named file | No unsolicited prose normalization or RTL work |
| N02 | Return valid JSON containing Persian text | No hidden direction controls or Persianized numeric syntax |

For each run record agent/version, request, loaded references, output, token-preservation check, destination screenshot where relevant, and pass/fail with reason. Do not count reading this table as passing a test.

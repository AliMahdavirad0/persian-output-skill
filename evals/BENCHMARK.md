# Initial translation pilot

Results are in [pilot-results.json](pilot-results.json); prompts are in [evals.json](evals.json).

On 2026-10-12, Codex CLI 0.162.0-alpha.17.2 ran translation (E01) and informal editing (E02) once with and once without the skill, in fresh projects with the same user-configured defaults. All four completed and preserved the declared protected version/date/URL tokens. Percentages in ordinary translated prose may use Persian digits; these are checked for meaning, not byte identity. The E02 outputs were identical. E01 outputs both retained uncertainty, upper bound and lack of a universal guarantee on author inspection. There is no demonstrated naturalness advantage from these two pairs.

For HTML (E03), the no-skill run completed. The initial with-skill run timed out at 150 seconds; a source-only retry completed after the harness explicitly stated that the referenced image and renderer were unavailable. Both completed HTML outputs passed the conservative static audit for structure, image attributes, stylesheet/layout attributes, links and protected code. The retry is not a strictly matched baseline pair and does not establish rendered image geometry.

Separately, the authored [English](../examples/layout-preservation/original.html) and [Persian](../examples/layout-preservation/translated.html) article fixtures were visually inspected at desktop and 390px mobile widths. [Geometry evidence](../examples/layout-preservation/geometry-evidence.json) records identical image rectangles and assets, unchanged code, and no page overflow. These fixtures are not model-generated benchmark outputs.

Remaining nine cases were not run. There was no blinded human comparison, statistical significance test, Microsoft Word runtime test, or general website/PDF guarantee. The pilot reports observable behavior and cost, not a quality score or proof of universal improvement.

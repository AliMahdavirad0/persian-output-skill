# Translation and editing evaluation

The 12 authored cases in [evals.json](evals.json) cover meaning, tone, preserved tokens, in-place article structure, and unavailable renderer/OCR behavior. The first three are the pilot set. They are prompts and expected behavior, not a declaration that all cases passed.

Run each case in a fresh project/session with the installed skill and again without it, keeping model/settings identical. Record the exact output, agent/version, elapsed time, token usage if available, and mechanical checks. For subjective naturalness, compare anonymized outputs with a Persian reader. Check fidelity against the source separately; smoother text can still be wrong.

Do not infer better translation from a YAML checker or a single example. Publish raw counts and limitations; do not claim statistical significance from this small pilot. The suite uses authored synthetic sources to avoid republishing private or restricted articles.

"""Dependency-free package/fixture checks; not an agent behavior benchmark."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "persian-output-skill"
BIDI = set(chr(n) for n in [0x061C, 0x200E, 0x200F, *range(0x202A, 0x202F), *range(0x2066, 0x206A)])
TOKENS = {
    "path": r"C:\Projects\demo\config.json",
    "url": "https://example.com/docs?q=rtl&v=2",
    "code": 'payload = {"version": "v2.1.0", "amount": 3.14, "path": r"C:\\Projects\\demo\\config.json"}',
}


class FixtureParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tokens = {}
        self.active = None
        self.html = {}
        self.href = None
        self.pre_ltr = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.html = attrs
        if tag == "pre":
            self.pre_ltr = attrs.get("dir") == "ltr"
        if "data-token" in attrs:
            self.active = attrs["data-token"]
            self.tokens[self.active] = ""
            if self.active == "url":
                self.href = attrs.get("href")

    def handle_data(self, data):
        if self.active:
            self.tokens[self.active] += data

    def handle_endtag(self, tag):
        if ((tag == "bdi" and self.active == "path") or
                (tag == "a" and self.active == "url") or
                (tag == "code" and self.active == "code")):
            self.active = None


def validate(root=ROOT):
    skill = root / "skills" / "persian-output-skill"
    checks = []

    def check(name, condition):
        checks.append({"check": name, "passed": bool(condition)})

    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    check("frontmatter-delimiters", match is not None)
    front = match.group(1) if match else ""
    check("skill-name", "name: persian-output-skill" in front)
    check("description", bool(re.search(r"^description: .{40,1024}$", front, re.M)))
    check("no-scaffold", not re.search(r"\b(?:TODO|TBD|FIXME)\b", text))
    metadata = (skill / "agents" / "openai.yaml").read_text(encoding="utf-8")
    check("ui-invocation", "$persian-output-skill" in metadata)
    check("implicit-selection", "allow_implicit_invocation: true" in metadata)
    for file in sorted(root.rglob("*.md")):
        if any(part in {".agents", ".claude", ".git"} for part in file.parts):
            continue
        content = file.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if "://" not in target and not target.startswith("#"):
                check(f"link:{file.relative_to(root)}:{target}", (file.parent / target.split("#")[0]).is_file())
        check(f"no-hidden-bidi:{file.relative_to(root)}", not (set(content) & BIDI))
    html = (root / "examples" / "rtl-web.html").read_text(encoding="utf-8")
    parser = FixtureParser()
    parser.feed(html)
    check("web-root-rtl", parser.html.get("dir") == "rtl" and parser.html.get("lang") == "fa")
    check("web-code-ltr", parser.pre_ltr)
    check("web-link-target", parser.href == TOKENS["url"])
    for name, expected in TOKENS.items():
        actual = parser.tokens.get(name)
        check(f"web-token:{name}", actual == expected)
        check(f"web-token-no-controls:{name}", actual is not None and not any(unicodedata.category(ch) == "Cf" for ch in actual))
    check("web-no-hidden-bidi", not (set(html) & BIDI))
    check("license", "MIT License" in (root / "LICENSE").read_text(encoding="utf-8"))
    return checks


if __name__ == "__main__":
    results = validate()
    failures = [item for item in results if not item["passed"]]
    print(json.dumps({"passed": len(results) - len(failures), "failed": len(failures), "failures": failures}, ensure_ascii=False, indent=2))
    sys.exit(bool(failures))

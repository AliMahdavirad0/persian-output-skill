"""Read-only conservative static HTML preservation check; not a visual renderer."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import sys

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
TRANSLATABLE_ATTRS = {'lang', 'dir', 'alt', 'title', 'aria-label', 'placeholder'}
PROTECTED = {'script', 'style', 'code', 'pre', 'math'}


class Snapshot(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.structure = []
        self.protected = []
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        stable = tuple(sorted((k, v) for k, v in attrs.items() if k not in TRANSLATABLE_ATTRS))
        self.structure.append(('start', tag, stable))
        if tag not in VOID:
            protect = tag in PROTECTED or attrs.get('translate') == 'no'
            self.stack.append({'tag': tag, 'protected': protect, 'text': ''})

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        self.structure.append(('end', tag))
        if not self.stack or self.stack[-1]['tag'] != tag:
            self.errors.append(f'Unbalanced closing tag: {tag}')
            return
        frame = self.stack.pop()
        if frame['protected']:
            self.protected.append((frame['tag'], frame['text']))

    def handle_data(self, data):
        for frame in self.stack:
            if frame['protected']:
                frame['text'] += data

    def finish(self):
        self.close()
        if self.stack:
            self.errors.append('Unclosed tags: ' + ', '.join(frame['tag'] for frame in self.stack))


def audit(original, translated):
    snapshots = []
    for text in [original, translated]:
        snap = Snapshot()
        snap.feed(text)
        snap.finish()
        snapshots.append(snap)
    before, after = snapshots
    checks = {
        'explicit_html_balance': not before.errors and not after.errors,
        'structure_and_stable_attributes': before.structure == after.structure,
        'protected_code_scripts_styles_math': before.protected == after.protected,
    }
    return {'passed': all(checks.values()), 'checks': checks,
            'parse_notes': before.errors + after.errors,
            'limit': 'Static source check only. Render both pages to compare image geometry and text fit; review translation separately.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original', type=Path)
    parser.add_argument('translated', type=Path)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        result = audit(args.original.read_text(encoding='utf-8'), args.translated.read_text(encoding='utf-8'))
    except (OSError, UnicodeError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for name, passed in result['checks'].items():
            print(f'{name}: {"PASS" if passed else "FAIL"}')
        print(result['limit'])
    sys.exit(0 if result['passed'] else 1)

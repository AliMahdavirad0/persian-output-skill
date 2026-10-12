"""Read-only conservative static HTML preservation check; not a visual renderer."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import sys

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
TRANSLATABLE_ATTRS = {'lang', 'dir', 'alt', 'title', 'aria-label', 'placeholder'}
PROTECTED = {'script', 'style', 'code', 'pre', 'math'}
TEXT_DIRECTION = {'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'a', 'bdi', 'bdo', 'b', 'i', 'em', 'strong', 'u', 's', 'small', 'mark', 'sub', 'sup', 'cite', 'q', 'blockquote', 'li', 'dt', 'dd', 'th', 'td', 'figcaption', 'label', 'legend', 'button', 'option', 'textarea', 'title'}
MEDIA = {'img', 'picture', 'video', 'audio', 'canvas', 'svg', 'iframe', 'object', 'embed'}


class Snapshot(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.structure = []
        self.protected = []
        self.stack = []
        self.errors = []
        self.direction_candidates = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        inherited_no = self.stack[-1]['notranslate'] if self.stack else False
        translate = attrs.get('translate')
        value = translate.lower() if translate is not None else None
        notranslate = True if value == 'no' else False if value in {'', 'yes'} else inherited_no
        code_scope = tag in PROTECTED or (self.stack[-1]['code_scope'] if self.stack else False)
        allowed = set() if notranslate or code_scope else TRANSLATABLE_ATTRS
        stable = tuple(sorted((k, v) for k, v in attrs.items() if k not in allowed))
        candidate = {'index': len(self.structure), 'tag': tag,
                     'direction': (attrs.get('dir') or '').strip().lower(),
                     'freeze': tag not in TEXT_DIRECTION or code_scope or notranslate,
                     'contains_media': tag in MEDIA}
        self.direction_candidates.append(candidate)
        if tag in MEDIA:
            for frame in self.stack:
                frame['candidate']['contains_media'] = True
        self.structure.append(('start', tag, stable))
        if tag not in VOID:
            self.stack.append({'tag': tag, 'protected': code_scope or notranslate,
                               'code_scope': code_scope, 'notranslate': notranslate,
                               'candidate': candidate, 'text': ''})

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
        current_no = self.stack[-1]['notranslate'] if self.stack else False
        for frame in self.stack:
            if frame['code_scope'] or (frame['notranslate'] and current_no):
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
    def layout_directions(snap):
        return [(c['index'], c['tag'], c['direction']) for c in snap.direction_candidates
                if c['freeze'] or c['contains_media']]
    checks = {
        'explicit_html_balance': not before.errors and not after.errors,
        'structure_and_stable_attributes': before.structure == after.structure,
        'protected_code_scripts_styles_math': before.protected == after.protected,
        'layout_media_and_code_directions': layout_directions(before) == layout_directions(after),
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

#!/usr/bin/env python3
"""Check an Arabic page source against its English original.

Usage: python3 scripts/check-ar.py <key> [<key> ...]   (key e.g. password-generator, blog/index)
       python3 scripts/check-ar.py --all
Exit code 1 if any hard error. Leftover-English findings are warnings to review.
"""
import glob, json, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = re.compile(r'^<!--meta\n([\s\S]*?)\n-->\n<!--head-->\n([\s\S]*?)<!--body-->\n([\s\S]*)$')
SCRIPT = re.compile(r'<script(?![^>]*ld\+json)[^>]*>(.*?)</script>', re.S)
LDJSON = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
TAG = re.compile(r'<([a-zA-Z][a-zA-Z0-9]*)\b')


def load(lang, key):
    path = os.path.join(ROOT, 'src/site', lang, key + '.html')
    m = SRC.match(open(path, encoding='utf-8').read())
    if not m:
        raise ValueError(f'{path}: malformed (needs <!--meta ... -->, <!--head-->, <!--body--> sections)')
    return json.loads(m.group(1)), m.group(2), m.group(3)


def markup_only(s):
    s = SCRIPT.sub('<script></script>', s)
    s = LDJSON.sub('<script></script>', s)
    return re.sub(r'<style[^>]*>.*?</style>', '<style></style>', s, flags=re.S)


def tags(s):
    return [t.lower() for t in TAG.findall(markup_only(s)) if t.lower() != 'bdi']


def attr_set(s, attr):
    vals = set()
    for v in re.findall(rf'\b{attr}="([^"]*)"', markup_only(s)):
        vals.update(v.split() if attr == 'class' else [v])
    return vals - {'flip-rtl'}


def visible_text_segments(body):
    s = SCRIPT.sub(' ', body)
    s = re.sub(r'<style[^>]*>.*?</style>', ' ', s, flags=re.S)
    s = re.sub(r'<(pre|code|kbd|samp)\b[^>]*>.*?</\1>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]*\bdir="ltr"[^>]*>.*?</[a-z0-9]+>', ' ', s, flags=re.S)
    return [t.strip() for t in re.split(r'<[^>]+>', s) if t.strip()]


def js_strings(body):
    out = []
    for js in SCRIPT.findall(body):
        out += re.findall(r"""(?:textContent|innerText|innerHTML|label|title|toast\w*)\s*[=:(]\s*(['"`])((?:(?!\1).)*)\1""", js)
    return [s for _, s in out]


def english_runs(text):
    # 4+ consecutive Latin words that look like prose
    return re.findall(r"\b[A-Za-z][a-z']+(?:[ ,][A-Za-z][a-z']+){3,}", text)


def check(key):
    errors, warns = [], []
    try:
        em, eh, eb = load('en', key)
        am, ah, ab = load('ar', key)
    except FileNotFoundError as e:
        return [f'missing file: {e.filename}'], []
    except (ValueError, json.JSONDecodeError) as e:
        return [str(e)], []

    if set(em) != set(am):
        errors.append(f'meta keys differ: {set(em) ^ set(am)}')
    for k in ('title', 'description', 'ogTitle', 'ogDescription'):
        if k in am and not re.search(r'[؀-ۿ]', am[k]):
            errors.append(f'meta.{k} not translated')
    for k in ('robots', 'ogType', 'sitemap'):
        if em.get(k) != am.get(k):
            errors.append(f'meta.{k} changed')

    for label, e, a in (('head', eh, ah), ('body', eb, ab)):
        te, ta = tags(e), tags(a)
        if label == 'head':
            ta = [t for t in ta if t != 'style'] ; te = [t for t in te if t != 'style']
        if te != ta:
            i = next((i for i, (x, y) in enumerate(zip(te, ta)) if x != y), min(len(te), len(ta)))
            errors.append(f'{label} tag sequence differs at #{i}: en={te[i:i+4]} ar={ta[i:i+4]} (en {len(te)} tags, ar {len(ta)})')
        for attr in ('id', 'class', 'href', 'onclick', 'for', 'name', 'type'):
            d = attr_set(e, attr) ^ attr_set(a, attr)
            if d:
                errors.append(f'{label} {attr} values differ: {sorted(d)[:8]}')

    en_styles = re.findall(r'<style[^>]*>(.*?)</style>', eh, re.S)
    ar_styles = re.findall(r'<style[^>]*>(.*?)</style>', ah, re.S)
    if ar_styles[:len(en_styles)] != en_styles:
        errors.append('original <style> blocks were modified (append RTL overrides in a new <style> instead)')
    for extra in ar_styles[len(en_styles):]:
        for rule in re.findall(r'([^{}]+)\{', extra):
            if not rule.strip().startswith(('html[dir=rtl]', '@media')) and 'html[dir=rtl]' not in rule:
                errors.append(f'RTL override not scoped to html[dir=rtl]: {rule.strip()[:60]}')

    for i, js in enumerate(SCRIPT.findall(ab)):
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t:
            t.write(js)
        r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
        os.unlink(t.name)
        if r.returncode:
            errors.append(f'script #{i} syntax error: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "?"}')
    en_js, ar_js = SCRIPT.findall(eb), SCRIPT.findall(ab)
    if len(en_js) != len(ar_js):
        errors.append(f'script count differs: en {len(en_js)} ar {len(ar_js)}')

    for blk in LDJSON.findall(ah + ab):
        try:
            d = json.loads(blk)
            if '"inLanguage": "ar"' not in json.dumps(d, ensure_ascii=False):
                warns.append('JSON-LD has no "inLanguage": "ar"')
        except json.JSONDecodeError as e:
            errors.append(f'JSON-LD invalid: {e}')

    for seg in visible_text_segments(ab):
        for run in english_runs(seg):
            warns.append(f'English text? "{run[:80]}"')
    for s in js_strings(ab):
        for run in english_runs(s):
            warns.append(f'English JS string? "{run[:80]}"')
    for attr in ('aria-label', 'title', 'alt', 'placeholder'):
        for v in re.findall(rf'\b{attr}="([^"]*)"', markup_only(ab)):
            if english_runs(v) or (re.fullmatch(r'[A-Za-z ]{3,}', v) and v.lower() not in ('zecure',)):
                warns.append(f'{attr} untranslated? "{v}"')
    return errors, sorted(set(warns))


def main(argv):
    if argv == ['--all']:
        keys = sorted(os.path.relpath(p, os.path.join(ROOT, 'src/site/ar'))[:-5]
                      for p in glob.glob(os.path.join(ROOT, 'src/site/ar/**/*.html'), recursive=True))
    else:
        keys = argv
    failed = 0
    for key in keys:
        errors, warns = check(key)
        status = 'FAIL' if errors else 'ok'
        failed += bool(errors)
        print(f'[{status}] {key}  ({len(errors)} errors, {len(warns)} warnings)')
        for e in errors:
            print('   ERROR', e)
        for w in warns[:40]:
            print('   warn ', w)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

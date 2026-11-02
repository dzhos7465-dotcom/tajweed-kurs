# tk.py (часть инструментов скилла, нужная для контрольной): корпус, сверка, текст v18
import json, re, os, subprocess, unicodedata as u
CORPUS = '/tmp/quran-json/data/quranpedia/qpc-hafs.json'
V18_URL = 'https://raw.githubusercontent.com/thetruetruth/quran-data-kfgqpc/main/hafs/data/hafsData_v18.json'
FONT_URL = 'https://raw.githubusercontent.com/thetruetruth/quran-data-kfgqpc/main/hafs/font/hafs.18.woff2'
_C = None
def corpus():
    global _C
    if _C is None: _C = json.load(open(CORPUS))
    return _C

_MAP = {'ـ': '', 'ࣰ': 'ٗ', 'ࣱ': 'ٞ', 'ࣲ': 'ٖ', '۟': 'ْ', 'آ': 'آ'}
def key(w):
    for a, b in _MAP.items(): w = w.replace(a, b)
    out = []
    for ch in w:
        if u.combining(ch) or ch in 'ٰۡۥۦْٓٔ':
            if out: out[-1][1].append('ْ' if ch == 'ۡ' else ch)
        else: out.append([ch, []])
    return tuple((b, tuple(sorted(m))) for b, m in out)
def _nosuk(k): return tuple((b, tuple(m for m in ms if m != 'ْ')) for b, ms in k)

def check_words(text):
    full, light = set(), set()
    for vs in corpus().values():
        for v in vs:
            for w in v['text'].split(): k = key(w); full.add(k); light.add(_nosuk(k))
    bad, suk = [], []
    for w in sorted(set(re.findall(r'[ء-ۿࣰ-ࣲ]+', text))):
        if re.fullmatch(r'[٠-٩]+', w) or key(w) in full: continue
        (suk if _nosuk(key(w)) in light else bad).append(w)
    if 'آ' in text: bad.insert(0, 'ВНИМАНИЕ: готовая U+0622')
    return bad, suk

_V = None
def aya18(s, a):
    global _V
    p = '/tmp/hafsData_v18.json'
    if not os.path.exists(p): subprocess.run(['curl', '-sSL', '-o', p, V18_URL], check=True)
    if _V is None: _V = {(int(v['sora']), int(v['aya_no'])): v['aya_text'] for v in json.load(open(p))}
    return re.sub(r'[\s\xa0]*[٠-٩]+$', '', _V[(s, a)])

def font_b64():
    import base64
    p = '/tmp/hafs.18.woff2'
    if not os.path.exists(p): subprocess.run(['curl', '-sSL', '-o', p, FONT_URL], check=True)
    return base64.b64encode(open(p, 'rb').read()).decode()

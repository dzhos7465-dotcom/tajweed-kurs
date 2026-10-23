# madd.py — разметка всех маддов в аяте (QPC Hafs) при условии: остановка только в конце аята
import json, re, unicodedata as u
C = json.load(open('/tmp/quran-json/data/quranpedia/qpc-hafs.json'))
def aya(s, a): return next(v['text'] for v in C[str(s)] if v['verse'] == a)
def nayat(s): return len(C[str(s)])

FATHA, DAMMA, KASRA = 'َ', 'ُ', 'ِ'
SUK, SHADDA, MADDA, DAGGER = 'ۡ', 'ّ', 'ٓ', 'ٰ'
HMZ_MARK = 'ٕٔ'
SILENT = '۟'
TANF = 'ًࣰٗ'
SW, SY = 'ۥ', 'ۦ'
HAMZAS = 'ءأإؤئ'
WAQF = set('ۖۗۘۙۚۛۜ')

def letters(w):
    out = []
    for ch in w:
        if ch in WAQF: continue
        if u.combining(ch) or ch in 'ٰٕۡٓٔ۟':
            if out: out[-1][1].append(ch)
        else: out.append([ch, []])
    # tatweel без знаков — выкинуть; немые буквы (۟) — выкинуть
    return [l for l in out if not (l[0] == 'ـ' and not l[1]) and SILENT not in l[1] and '\u0652' not in l[1] and '\u06e0' not in l[1]]

def is_hamza(l): return l[0] in HAMZAS or any(m in HMZ_MARK for m in l[1])
def has(l, ms): return any(m in ms for m in l[1])
def perm_suk(l): return has(l, SUK + SHADDA)

def madds(word):
    """позиции маддов в слове: (индекс буквы-носителя, буква мадда, хамза_перед)"""
    L = letters(word); res = []
    for i, (b, ms) in enumerate(L):
        prev = L[i-1] if i else None
        if DAGGER in ms: res.append((i, 'ا', is_hamza(L[i])))
        if b in 'اى' and DAGGER not in ms and not has(L[i], FATHA+DAMMA+KASRA+SUK+SHADDA) and prev and has(prev, FATHA) and b != 'ٱ':
            res.append((i, 'ا', is_hamza(prev)))
        if b == 'و' and not has(L[i], FATHA+DAMMA+KASRA+SUK+SHADDA+TANF) and prev and has(prev, DAMMA):
            res.append((i, 'و', is_hamza(prev)))
        if b in 'يى' and DAGGER not in ms and not has(L[i], FATHA+DAMMA+KASRA+SUK+SHADDA+TANF) and prev and has(prev, KASRA):
            res.append((i, 'ي', is_hamza(prev)))
        if b == 'أ' and MADDA in ms: res.append((i, 'ا', True))
        if b in (SW, SY): res.append((i, 'sila', False))
    return L, res

def starts_hamza(w):
    L = letters(w); return bool(L) and is_hamza(L[0])

def classify(s, a, skip_first=False):
    ws = [w for w in aya(s, a).split() if any(c.isalpha() for c in w if not u.combining(c))]
    out = []
    for wi, w in enumerate(ws):
        L, ms = madds(w); last = wi == len(ws) - 1
        nxt = ws[wi+1] if not last else None
        for (i, kind, hb) in ms:
            after = L[i+1:]
            # где стоит «буква мадда»: для ٰ — на той же букве; для обычной — это сама буква i
            if kind == 'sila':
                if last: t = None
                elif starts_hamza(nxt): t = 'сыля кубра'
                else: t = 'сыля сугра'
            elif hb and L[i][0] == 'أ': t = 'бадаль'
            elif after and is_hamza(after[0]):
                t = 'мунфасиль' if (i <= 1 and L[0][0] in 'يه' and has(L[0], FATHA)) or (i <= 2 and L[0][0] == 'و' and L[1][0] in 'يه') else 'муттасиль'
            elif after and perm_suk(after[0]): t = 'лязим'
            elif not after:
                if last: t = 'табиъий'
                elif nxt.startswith('ٱ'): t = None   # выпадает
                elif starts_hamza(nxt): t = 'мунфасиль'
                else: t = 'табиъий'
            elif last and len(after) == 1: t = 'арид' + (' (бадаль)' if hb else '')
            else: t = 'бадаль' if hb else 'табиъий'
            if t: out.append((wi+1, w, kind, t))
        if last:
            if len(L) >= 2 and L[-1][0] == 'ا' and has(L[-2], TANF): out.append((wi+1, w, 'ا', 'ивад'))
            elif has(L[-1], TANF) and L[-1][0] != 'ة': out.append((wi+1, w, 'ا', 'ивад'))
            if len(L) >= 3 and L[-2][0] in 'وي' and SUK in L[-2][1] and has(L[-3], FATHA):
                out.append((wi+1, w, L[-2][0], 'лин'))
    return out

def show(s, a1, a2, kinds=None):
    for a in range(a1, a2+1):
        r = classify(s, a)
        r = [x for x in r if not kinds or x[3].split()[0] in kinds]
        print(f'{s}:{a}', ' | '.join(f'{w}({k}:{t})' for _, w, k, t in r))

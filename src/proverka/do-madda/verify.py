# verify.py — независимая проверка всех ответов: каждый ответ вычисляется заново по тексту аята
# (остановка только в конце аята) и сравнивается с data.py. В конце должно быть «ВСЁ ВЕРНО».
import os, sys, unicodedata as u
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'engine'))
import data, tk
from common import toks, sk

FATHA, DAMMA, KASRA, SHADDA, SUK = 'َ', 'ُ', 'ِ', 'ّ', 'ۡ'
TAN_F, TAN_D, TAN_K = set('ًٗ'), set('ٌٞ'), set('ٍٖ')
TAN = TAN_F | TAN_D | TAN_K
IQ = {'\u06e2', '\u06ed'}   # малый мим — танвин с иклябом
def tanv(m): return bool(m & TAN) or (bool(m & IQ) and bool(m & {FATHA, DAMMA, KASRA}))
HEAVY = set('خصضغطقظ')

def letters(w):
    """[(буква, {знаки})] — буквы слова с огласовками; татвиль и малые буквы не считаются буквами"""
    out = []
    for c in w:
        if (u.combining(c) or c in 'ٰۡۥۦۭۢـۜ') and out: out[-1][1].add(c)
        elif not (u.combining(c) or c == 'ـ'): out.append([c, set()])
    return out

def vowel(m):
    if m & ({FATHA} | TAN_F): return 'a'
    if m & ({DAMMA} | TAN_D): return 'u'
    if m & ({KASRA} | TAN_K): return 'i'
    return ''

def first(w):
    L = letters(w); return L[0][0] if L else ''

def nun_places(s, a):
    """все нуны с сукуном и танвины аята: {номер_слова: правило}; на последнем слове аята — 'stop'"""
    ws = toks(s, a); res = {}
    for i, w in enumerate(ws):
        L = letters(w)
        for j, (c, m) in enumerate(L):
            last = j == len(L) - 1
            nx = None
            if c == 'ن' and not (m & ({FATHA, DAMMA, KASRA, SHADDA} | TAN)):
                nx = L[j + 1][0] if not last else (first(ws[i + 1]) if i + 1 < len(ws) else 'STOP')
            elif tanv(m) and (last or all(x[0] in 'اى' for x in L[j + 1:])):
                nx = first(ws[i + 1]) if i + 1 < len(ws) else 'STOP'
            if nx is None or nx in 'ٱ': continue
            if nx == 'STOP': res[i] = 'stop'
            elif nx in 'ءأإؤئهعحغخا': res[i] = 'Изхар'
            elif nx in 'ينمو': res[i] = 'Идгам с гунной'
            elif nx in 'لر': res[i] = 'Идгам без гунны'
            elif nx == 'ب': res[i] = 'Икляб'
            else: res[i] = 'Ихфа'
    return res

def mim_places(s, a):
    ws = toks(s, a); res = {}
    for i, w in enumerate(ws[:-1]):
        L = letters(w)
        if L and L[-1][0] == 'م' and not (L[-1][1] & {FATHA, DAMMA, KASRA, SHADDA}):
            nx = first(ws[i + 1]); res[i] = 'Ихфа' if nx == 'ب' else 'Идгам' if nx == 'م' else 'Изхар'
    return res

def ghunna(w):
    L = letters(w); return any(c in 'من' and SHADDA in m and j > 0 for j, (c, m) in enumerate(L))

def ra_kind(ws, i):
    L = letters(ws[i]); last_word = i == len(ws) - 1
    for j, (c, m) in enumerate(L):
        if c != 'ر': continue
        v = vowel(m)
        if last_word and j == len(L) - 1: v = ''          # остановка: ра с сукуном
        if v in ('a', 'u'): return 'Твёрдая'
        if v == 'i': return 'Мягкая'
        k = j - 1
        while k >= 0 and not vowel(L[k][1]): k -= 1
        return 'Мягкая' if k >= 0 and vowel(L[k][1]) == 'i' else 'Твёрдая'
    return None

def qal_kind(ws, i):
    L = letters(ws[i]); last_word = i == len(ws) - 1
    for j, (c, m) in enumerate(L):
        if c not in 'قطبجد': continue
        if last_word and j == len(L) - 1: return 'Большая'
        if SUK in m and j < len(L) - 1: return 'Малая'
        if SUK in m and not last_word: return 'Малая'
    return None

def stop_kind(w):
    L = letters(w); c, m = L[-1]
    if c == 'ة': return 'Читаем «х»'
    if c in 'اى' and len(L) > 1 and (L[-2][1] & TAN_F or (FATHA in L[-2][1] and L[-2][1] & IQ)): return 'Читаем алиф'
    if m & (TAN_D | TAN_K) or (m & IQ and m & {DAMMA, KASRA}): return 'Сукун, танвин уходит'
    if c == 'ه' and m & {'ۥ', 'ۦ'}: return 'Малая буква не читается'
    return '?'

def lam_kind(ws, i):
    w = ws[i]
    if not w.startswith('ٱ'):                     # приставка в том же слове: بِٱللَّهِ, لِّلَّهِ
        return 'Мягко' if vowel(letters(w)[0][1]) == 'i' else 'Твёрдо'
    if i == 0: return 'Твёрдо'
    return 'Мягко' if vowel(letters(ws[i - 1])[-1][1]) == 'i' else 'Твёрдо'

ok = True; text = ''
def rep(good, msg):
    global ok; ok &= good; print(('   OK  ' if good else '   !!! ') + msg)

for mode in 'kt':
    print('=====', 'контрольная' if mode == 'k' else 'тренажёр')
    for n, T in enumerate(data.tasks(mode), 1):
        print('%2d %s' % (n, T['title'])); key = T['key']
        if T['kind'] == 'pickWord':
            for it in T['items']:
                w = toks(it['s'], it['a'])[it['wi']]; text += ' ' + w
                rep(bool(set(w) & HEAVY) == it['ok'] and (it['ok'] or ('ر' not in w and 'لل' not in sk(w))), '%s ok=%s' % (w, it['ok']))
        elif T['kind'] == 'label':
            for it in T['items']:
                ws = toks(it['s'], it['a']); w = ws[it['wi']]; text += ' ' + ' '.join(ws)
                if key == 'lam': exp = lam_kind(ws, it['wi'])
                elif key == 'stop': exp = stop_kind(w) if it['wi'] == len(ws) - 1 else 'не конец аята'
                else: exp = nun_places(it['s'], it['a']).get(it['wi'])
                rep(exp == it['ans'], '%d:%d %s → %s (вычислено: %s)' % (it['s'], it['a'], w, it['ans'], exp))
        else:
            tg = {(p['s'], p['a'], p['wi']): p['ans'] for p in T['targets']}
            neu = {(p['s'], p['a'], p['wi']) for p in T.get('neutral', [])}
            want_neu = set()
            for s, a in T['ayat']:
                ws = toks(s, a); text += ' ' + ' '.join(ws)
                for i, w in enumerate(ws):
                    if key == 'gh': exp = 'ok' if ghunna(w) else None
                    elif key == 'mim': exp = mim_places(s, a).get(i)
                    elif key == 'ra': exp = ra_kind(ws, i)
                    elif key == 'qal': exp = qal_kind(ws, i)
                    else:
                        r = nun_places(s, a).get(i)
                        if r == 'stop': want_neu.add((s, a, i))
                        rule = {'izh': 'Изхар', 'iql': 'Икляб', 'ikh': 'Ихфа'}.get(key)
                        if key == 'idg': exp = {'Идгам с гунной': 'С гунной', 'Идгам без гунны': 'Без гунны'}.get(r)
                        else: exp = 'ok' if r == rule else None
                    got = tg.get((s, a, i))
                    if exp or got: rep(exp == got, '%d:%d %s → %s (вычислено: %s)' % (s, a, w, got, exp))
            if key in ('izh', 'ikh'):
                want_neu = {k for k in want_neu}
                rep(neu == want_neu, 'нейтральные концы аятов: %d (вычислено %d)' % (len(neu), len(want_neu)))
        if T['kind'] == 'label': pts = len(T['items'])
        elif T['kind'] == 'pickWord': pts = sum(1 for it in T['items'] if it['ok'])
        else: pts = len(T['targets'])
        print('   задание %d: %d мест' % (n, pts))
    print('ИТОГО мест:', sum(len(T['items']) if T['kind'] == 'label' else sum(1 for it in T['items'] if it['ok']) if T['kind'] == 'pickWord' else len(T['targets']) for T in data.tasks(mode)))
bad, suk = tk.check_words(text); print('нет в корпусе:', bad, '| сукун:', suk)
print('ВСЁ ВЕРНО' if ok and not bad else 'ЕСТЬ ОШИБКИ')

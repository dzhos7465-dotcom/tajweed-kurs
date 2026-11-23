# verify.py — независимая проверка ответов пробного экзамена / экзамена: каждый ответ вычисляется заново
# по тексту аята (детекторы do-madda/verify.py и madd/madd.py), в отрывках сур — что других нужных мест нет.
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
for p in ('../engine', '../madd', '.'): sys.path.insert(0, os.path.join(H, p))
src = open(os.path.join(H, '../do-madda/verify.py')).read()
exec(src[:src.find('ok = True')].replace('import data, tk', 'import tk'))
import madd, data
from common import toks
bad = []
def chk(cond, msg):
    if not cond: bad.append(msg)
def M(s, a, i):   # виды мадда в слове i (с 0)
    return [t for wi, w, k, t in madd.classify(s, a) if wi - 1 == i]
CAP = {'табиъий':'Табиъий','ивад':'Ивад','бадаль':'Бадаль','сыля сугра':'Сыля сугра','сыля кубра':'Сыля кубра','муттасиль':'Муттасиль',
       'мунфасиль':'Мунфасиль','арид':'Арид','лин':'Лин','лязим':'Лязим'}
def mkind(it):
    """вид мадда в выделенном месте: мадд, начинающийся внутри выделения"""
    ws = toks(it['s'], it['a']); w = ws[it['wi']]
    out = [(k, t) for wi, ww, k, t in madd.classify(it['s'], it['a']) if wi - 1 == it['wi']]
    return out
T = data.tasks('k')
for t in T:
    key = t['key']
    for it in t.get('items', []):
        s, a = it['s'], it['a']; ws = toks(s, a); i = it.get('wi'); w = ws[i] if i is not None else ws[-1]
        where = '%s %d:%d %s' % (key, s, a, w)
        if key == 'hv': chk(bool(set(sk(w)) & HEAVY) == it['ok'], where)
        elif key == 'lam': chk(lam_kind(ws, i) == {'Твёрдо':'Твёрдо','Мягко':'Мягко'}[it['ans']], where + ' ' + str(lam_kind(ws, i)))
        elif key == 'stop': chk(i == len(ws) - 1 and stop_kind(w) == it['ans'], where + ' ' + str(stop_kind(w)))
        elif key == 'nun': chk(nun_places(s, a).get(i) == it['ans'], where + ' ' + str(nun_places(s, a).get(i)))
        elif key in ('kl', 'cnt', 'mm', 'ar', 'all', 'sl'):
            ks = [CAP[x] for _, x in mkind(it)]
            if key == 'kl': chk(any(({'Табиъий','Ивад','Бадаль','Сыля сугра'} & {k}) and it['ans']=='Короткий' or ({'Муттасиль','Мунфасиль','Сыля кубра','Арид','Лин','Лязим'} & {k}) and it['ans']=='Длинный' for k in ks), where + str(ks))
            elif key == 'cnt': chk(any({'Табиъий':'2','Ивад':'2','Бадаль':'2','Сыля сугра':'2','Муттасиль':'4 или 5','Мунфасиль':'4 или 5','Сыля кубра':'4 или 5','Арид':'2, 4 или 6','Лин':'2, 4 или 6','Лязим':'6'}[k] == it['ans'] for k in ks), where + str(ks))
            elif key == 'sl': chk((it['ans'] in ks) or (it['ans'] == 'Сыли нет' and not ({'Сыля сугра','Сыля кубра'} & set(ks))), where + str(ks))
            else: chk(it['ans'] in ks, where + ' ' + str(ks))
        elif key == 'iw': chk(('ивад' in [t2 for *_, t2 in madd.classify(s, a)][-1:]) == it['ok'], where)
        elif key == 'bd': chk(('бадаль' in M(s, a, i)) == it['ok'], where + str(M(s, a, i)))
        elif key == 'lz': chk(('лязим' in M(s, a, i)) == it['ok'], where + str(M(s, a, i)))
    if t['kind'] == 'tap':
        exp = {}
        for s, a in t['ayat']:
            ws = toks(s, a)
            for i, w in enumerate(ws):
                r = None
                if key == 'gh': r = 'ok' if ghunna(w) else None
                elif key == 'mim': r = mim_places(s, a).get(i)
                elif key in ('izh', 'iql', 'ikh'):
                    v = nun_places(s, a).get(i); r = v if v == {'izh':'Изхар','iql':'Икляб','ikh':'Ихфа'}[key] else None
                elif key == 'idg':
                    v = nun_places(s, a).get(i); r = {'Идгам с гунной':'С гунной','Идгам без гунны':'Без гунны'}.get(v)
                elif key == 'ra': r = ra_kind(ws, i)
                elif key == 'qal': r = qal_kind(ws, i)
                elif key == 'find':
                    k = [CAP[x] for x in M(s, a, i) if x in ('муттасиль', 'мунфасиль', 'сыля кубра')]; r = k[0] if k else None
                elif key == 'lin': r = 'Лин' if 'лин' in M(s, a, i) and i == len(ws) - 1 else None
                if r: exp[(s, a, i)] = r
        got = {(p['s'], p['a'], p['wi']): p['ans'] for p in t['targets']}
        if t.get('opts') is None: got = {k: (exp.get(k) or 'ok') if exp.get(k) else v for k, v in got.items()}
        if got != exp: bad.append('%s: в задании %s, по тексту %s' % (key, sorted(got.items()), sorted(exp.items())))
print('ПРОВЕРЕНО заданий:', len(T)); print('\n'.join(bad) if bad else 'ВСЁ ВЕРНО')

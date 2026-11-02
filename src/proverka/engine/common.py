# common.py — общий код проверочных работ: текст аятов, места в аятах, сборка HTML из data.py
# Работа (папка рядом с engine/) пишет только data.py (задания) и verify.py (проверку ответов),
# а build.py вызывает build_work(...) отсюда.
import json, os, sys, unicodedata as u
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tk

AR = '٠١٢٣٤٥٦٧٨٩'
AU = 'https://everyayah.com/data/Husary_Muallim_128kbps/%03d%03d.mp3'
WBW = 'https://audio.qurancdn.com/wbw/%03d_%03d_%03d.mp3'
SITE = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'proverka'))   # папка сайта proverka/

def an(n): return ''.join(AR[int(c)] for c in str(n))
def toks(s, a): return tk.aya18(s, a).split(' ')

def sk(w):
    """скелет слова: только буквы, для поиска"""
    w = w.replace('\u0622', '\u0627\u0653')
    return ''.join(c for c in w if not u.combining(c) and c not in 'ـۥۦ' and c.isalpha()).replace('ٱ', 'ا').replace('ى', 'ي')

def segs(w):
    """буквы слова вместе с их знаками"""
    out = []
    for ch in w:
        if (u.combining(ch) or ch in 'ٰۡٓٔ') and out: out[-1] += ch
        else: out.append(ch)
    return out

def find_word(s, a, word, occ=0):
    t = toks(s, a); hits = [i for i, x in enumerate(t) if sk(x) == sk(word)]
    assert len(hits) > occ, 'нет слова %s в %d:%d' % (word, s, a)
    return hits[occ]

def hl_range(w, part, pocc=0):
    """диапазон букв слова w, которые образуют part (по скелету)"""
    sg = segs(w); base = [sk(x) for x in sg]
    target = sk(part); found = []
    for i in range(len(sg)):
        acc = ''
        for j in range(i, len(sg)):
            acc += base[j]
            if acc == target and base[i] and base[j]:
                k = j + 1
                while k < len(sg) and sg[k][0] in 'ۥۦ': k += 1
                found.append((i, k)); break
            if len(acc) >= len(target): break
    assert len(found) > pocc, 'нет части %s в %s' % (part, w)
    return found[pocc]

def P(s, a, word, ans, hl=None, occ=0, pocc=0, why=None, ctx=None, alt=None):
    """Место в аяте. hl — какие буквы выделить; ctx — (from,to) номера слов для показа отрывка."""
    wi = find_word(s, a, word, occ); w = toks(s, a)[wi]
    d = dict(s=s, a=a, wi=wi, ans=ans)
    if hl: d['hl'] = hl_range(w, hl, pocc)
    if why: d['why'] = why
    if ctx: d['ctx'] = ctx
    if alt: d['alt'] = alt
    return d

def C(s, a, word, ok, why=None, occ=0):
    """Карточка-слово для выбора."""
    wi = find_word(s, a, word, occ)
    d = dict(s=s, a=a, wi=wi, ok=ok)
    if why: d['why'] = why
    return d

def A(s, a, ok, why=None):
    """Карточка-аят для выбора (последнее слово подчёркнуто)."""
    d = dict(s=s, a=a, wi=len(toks(s, a)) - 1, ok=ok)
    if why: d['why'] = why
    return d

# ---------- сборка ----------
NONLEFT = set('اأإآٱدذرزوؤةىءۥۦ')
def _joins(t):
    base = [c for c in t if not (u.combining(c) or c in 'ٰۡٓٔ')]
    return bool(base) and base[-1] not in NONLEFT

def parts(w, hl):
    if not hl: return w
    sg = segs(w); a, b, c = ''.join(sg[:hl[0]]), ''.join(sg[hl[0]:hl[1]]), ''.join(sg[hl[1]:])
    Z = '‍'   # ZWJ: Safari/iPhone иначе рвёт связь букв на границе цветного куска
    if a and b and _joins(a): a += Z; b = Z + b
    if b and c and _joins(b): b += Z; c = Z + c
    return [a, b, c]

def last_h(w):
    sg = segs(w); i = max(k for k, x in enumerate(sg) if x[0] == 'ه'); j = i + 1
    while j < len(sg) and sg[j][0] in 'ۥۦ': j += 1
    return (i, j)

def _task(T):
    t = dict(key=T['key'], kind=T['kind'], title=T['title'], instr=T['instr'], opts=T.get('opts'))
    if T.get('extra'): t['extra'] = T['extra']
    if T.get('gen'): t['gen'] = T['gen']             # объяснения ответов только для этого задания          # текст «лишняя отметка» в заданиях-«нажми в суре»
    if T['kind'] == 'label':
        t['items'] = []
        for it in T['items']:
            tw = toks(it['s'], it['a']); w = tw[it['wi']]; hl = it.get('hl')
            if T.get('hl_h'): hl = last_h(w)
            d = dict(ans=it['ans'], au=AU % (it['s'], it['a']))
            if 'ctx' in it:
                f, to = it['ctx']; d['words'] = tw[f-1:to]; d['ti'] = it['wi'] - (f-1); d['num'] = None
            else: d['words'] = tw; d['ti'] = it['wi']; d['num'] = an(it['a'])
            d['tw'] = parts(w, hl)
            if 'why' in it: d['why'] = it['why']
            if 'alt' in it: d['alt'] = it['alt'][0]; d['altwhy'] = it['alt'][1]
            t['items'].append(d)
    elif T['kind'] in ('pickAya', 'pickWord'):
        t['items'] = []
        for it in T['items']:
            tw = toks(it['s'], it['a']); w = tw[it['wi']]
            d = dict(ok=it['ok'], tw=w, why=it.get('why', ''))
            if T['kind'] == 'pickAya': d.update(words=tw, ti=it['wi'], num=an(it['a']), au=AU % (it['s'], it['a']))
            else: d['au'] = WBW % (it['s'], it['a'], it['wi'] + 1)
            t['items'].append(d)
    else:
        K = lambda p: '%d:%d:%d' % (p['s'], p['a'], p['wi'])
        t['targets'] = {K(p): p['ans'] for p in T['targets']}
        t['alt'] = {K(p): list(p['alt']) for p in T['targets'] if 'alt' in p}
        if T.get('neutral'): t['neutral'] = {K(p): 1 for p in T['neutral']}   # не засчитывается и не штрафуется
        t['blocks'] = []; t['order'] = []; t['wtext'] = {}
        for s, a in T['ayat']:
            ws = []
            for wi, w in enumerate(toks(s, a)):
                k = '%d:%d:%d' % (s, a, wi); ws.append(dict(t=w, k=k)); t['order'].append(k); t['wtext'][k] = w
            t['blocks'].append(dict(num=an(a), n=a, au=AU % (s, a), words=ws))
        if T.get('sura'): t['sura'] = T['sura']
        if T.get('basmala'): t['basmala'] = tk.aya18(1, 1)
    return t

def build_work(tasks, files, **opt):
    """tasks(mode) → список заданий; files — [(mode, имя файла в proverka/, заголовок, короткий заголовок)].
    opt (необязательно): key — ключ хранения ответов контрольной, hero — арабское слово на старте,
    sub — подзаголовок, group — спрашивать номер группы, gen — объяснения ответов {ответ: текст}."""
    tpl = open(os.path.join(HERE, 'template.html')).read() \
        .replace('__FONT__', tk.font_b64()).replace('__SURAFRAME__', open(os.path.join(HERE, 'suraframe.css')).read())
    for mode, fn, title, short in files:
        D = dict(mode=mode, title=title, short=short, tasks=[_task(T) for T in tasks(mode)])
        D.update({k: v for k, v in opt.items() if v is not None})
        js = json.dumps(D, ensure_ascii=False).replace('</', '<\\/')
        path = os.path.join(SITE, fn)
        open(path, 'w').write(tpl.replace('__TITLE__', title).replace('__DATA__', js))
        print('proverka/' + fn, len(open(path).read()) // 1024, 'KB')

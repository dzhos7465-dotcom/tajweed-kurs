import data, madd, tk
from data import toks, sk
LONG={'муттасиль','мунфасиль','сыля кубра','арид','лин','лязим','арид (бадаль)'}
MAPC={'2':{'табиъий','ивад','бадаль','сыля сугра'},'4 или 5':{'муттасиль','мунфасиль','сыля кубра'},'2, 4 или 6':{'арид','лин'},'6':{'лязим'}}
def types(s,a,wi):
    w=toks(s,a)[wi]
    return [t for _,ww,k,t in madd.classify(s,a) if sk(ww)==sk(w)], w
def exp(ans):
    a=ans.lower()
    if ans=='Длинный': return LONG
    if ans=='Короткий': return {'табиъий','ивад','бадаль','сыля сугра'}
    if ans in MAPC: return MAPC[ans]
    if ans=='Сыли нет': return None
    return {a}
ok=True; alltext=''
for mode in 'kt':
    print('=====',mode)
    for n,T in enumerate(data.tasks(mode),1):
        pts=0
        for it in T.get('items',[]):
            alltext+=' '+tk.aya18(it['s'],it['a'])
            ty,w=types(it['s'],it['a'],it['wi'])
            if 'ans' in it:
                pts+=1
                if T['key'] in ('harf','muh'): flag='(вручную)'
                else:
                    e=exp(it['ans'])
                    if e is None: good=not any('сыля' in t for t in ty)
                    else: good=bool(e & set(ty))
                    flag='OK' if good else '!!!'; ok&=good
                hl=''
                if 'hl' in it: sg=data.segs(w); hl=''.join(sg[it['hl'][0]:it['hl'][1]])
                print('%2d %d:%d %-18s [%s] %-12s %s %s'%(n,it['s'],it['a'],w,hl,it['ans'],ty,flag))
            else:
                if it['ok']: pts+=1
                if T['key']=='iw': good=('ивад' in ty and toks(it['s'],it['a'])[-1]==w)==it['ok']
                elif T['key']=='bd': good=(any('бадаль' in t for t in ty))==it['ok']
                elif T['key']=='lz': good=('лязим' in ty)==it['ok']
                ok&=good; print('%2d %d:%d %-18s ok=%s %s %s'%(n,it['s'],it['a'],w,it['ok'],ty,'OK' if good else '!!!'))
        if T['kind']=='tap':
            want={'find':{'муттасиль','мунфасиль','сыля кубра'},'lin':{'лин'}}[T['key']]
            tg={(p['s'],p['a'],p['wi']):p['ans'] for p in T['targets']}
            for s,a in T['ayat']:
                alltext+=' '+tk.aya18(s,a)
                for wi,w in enumerate(toks(s,a)):
                    ty=[t for t in types(s,a,wi)[0] if t in want]
                    if ty or (s,a,wi) in tg:
                        good=(s,a,wi) in tg and tg[(s,a,wi)].lower() in ty
                        ok&=good; print('%2d %d:%d %-18s %s → %s %s'%(n,s,a,w,ty,tg.get((s,a,wi)),'OK' if good else '!!!'))
            pts=len(tg)
        print('   задание %d: %d б.'%(n,pts))
bad,suk=tk.check_words(alltext); print('нет в корпусе:',bad,'| сукун:',suk); print('ВСЁ ВЕРНО' if ok else 'ЕСТЬ ОШИБКИ')

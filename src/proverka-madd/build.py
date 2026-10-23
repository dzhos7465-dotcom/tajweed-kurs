import json, sys, data, tk
from data import toks, segs
AR='٠١٢٣٤٥٦٧٨٩'
def an(n): return ''.join(AR[int(c)] for c in str(n))
AU='https://everyayah.com/data/Husary_Muallim_128kbps/%03d%03d.mp3'
WBW='https://audio.qurancdn.com/wbw/%03d_%03d_%03d.mp3'
def parts(w,hl):
    if not hl: return w
    sg=segs(w); return [''.join(sg[:hl[0]]),''.join(sg[hl[0]:hl[1]]),''.join(sg[hl[1]:])]
def last_h(w):
    sg=segs(w); i=max(k for k,x in enumerate(sg) if x[0]=='ه'); j=i+1
    while j<len(sg) and sg[j][0] in 'ۥۦ': j+=1
    return (i,j)
def build(mode):
    out=[]
    for T in data.tasks(mode):
        t=dict(key=T['key'],kind=T['kind'],title=T['title'],instr=T['instr'],opts=T.get('opts'))
        if T['kind']=='label':
            t['items']=[]
            for it in T['items']:
                tw=toks(it['s'],it['a']); w=tw[it['wi']]; hl=it.get('hl')
                if T['key']=='sl': hl=last_h(w)
                d=dict(ans=it['ans'],au=AU%(it['s'],it['a']))
                if 'ctx' in it:
                    f,to=it['ctx']; d['words']=tw[f-1:to]; d['ti']=it['wi']-(f-1); d['num']=None
                else: d['words']=tw; d['ti']=it['wi']; d['num']=an(it['a'])
                d['tw']=parts(w,hl)
                if 'why' in it: d['why']=it['why']
                t['items'].append(d)
        elif T['kind'] in ('pickAya','pickWord'):
            t['items']=[]
            for it in T['items']:
                tw=toks(it['s'],it['a']); w=tw[it['wi']]
                d=dict(ok=it['ok'],tw=w,why=it.get('why',''))
                if T['kind']=='pickAya': d.update(words=tw,ti=it['wi'],num=an(it['a']),au=AU%(it['s'],it['a']))
                else: d['au']=WBW%(it['s'],it['a'],it['wi']+1)
                t['items'].append(d)
        else:
            tg={'%d:%d:%d'%(p['s'],p['a'],p['wi']):p['ans'] for p in T['targets']}
            t['targets']=tg; t['blocks']=[]; t['order']=[]; t['wtext']={}
            for s,a in T['ayat']:
                ws=[]
                for wi,w in enumerate(toks(s,a)):
                    k='%d:%d:%d'%(s,a,wi); ws.append(dict(t=w,k=k)); t['order'].append(k); t['wtext'][k]=w
                t['blocks'].append(dict(num=an(a),n=a,au=AU%(s,a),words=ws))
            if T.get('sura'): t['sura']=T['sura']
            if T.get('basmala'): t['basmala']=tk.aya18(1,1)
        out.append(t)
    return out
tpl=open('template.html').read().replace('__FONT__',tk.font_b64()).replace('__SURAFRAME__',open('suraframe.css').read())
for mode,fn,title,short in [('k','kontrolnaya_madd.html','Контрольная по правилам мадда','Мадд · Контрольная'),('t','trenazher_madd.html','Тренажёр: правила мадда','Мадд · Тренажёр')]:
    D=dict(mode=mode,title=title,short=short,tasks=build(mode))
    js=json.dumps(D,ensure_ascii=False).replace('</','<\\/')
    open('out/'+fn,'w').write(tpl.replace('__TITLE__',title).replace('__DATA__',js))
    print(fn, len(open('out/'+fn).read())//1024,'KB')

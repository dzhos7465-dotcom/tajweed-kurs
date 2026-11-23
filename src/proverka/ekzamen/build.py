# Экзамен (23.11.2026): задания — ekzamen/data.py (виды как в пробном экзамене, места новые)
# → proverka/ekzamen.html. Свой key: попытки не смешиваются с пробным экзаменом.
import os, sys, re
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'engine')); sys.path.insert(0, H)
import data
from common import build_work
build_work(data.tasks, [('k', 'ekzamen.html', 'Экзамен по таджвиду', 'Экзамен')],
   key='ekzamen-2-v1', hero='ٱخۡتِبَارٌ', sub='заданий по всем пройденным темам',
   group=True, gen=data.GEN, parts=data.PARTS, **{'pass': 70})

# Надписи шаблона «контрольная» → «экзамен» (только в этом файле)
p = os.path.join(H, '..', '..', '..', 'proverka', 'ekzamen.html'); s = open(p, encoding='utf-8').read()
for a, b in [('Итог контрольной', 'Итог экзамена'), ('Контрольная сдана', 'Экзамен сдан'), ('Завершить контрольную?', 'Завершить экзамен?'),
             ('Контрольная сдана от ', 'Экзамен сдан от ')]:
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)

# Превью ссылки в WhatsApp / Telegram: общая обложка курса + название экзамена
U = 'https://dzhos7465-dotcom.github.io/tajweed-kurs/'
og = ('<meta property="og:type" content="website">\n<meta property="og:title" content="Экзамен по таджвиду">\n'
      '<meta property="og:description" content="Курс таджвида: 30 заданий по всем пройденным темам">\n'
      '<meta property="og:url" content="%sproverka/ekzamen.html">\n<meta property="og:image" content="%spreview-ekzamen-2.jpg">\n'
      '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:type" content="image/jpeg">\n'
      '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="%spreview-ekzamen-2.jpg">\n') % (U, U, U)
s = open(p, encoding='utf-8').read()
s = re.sub(r'<meta (property|name)="(og|twitter):[^>]*>\n', '', s); s = s.replace('<title>', og + '<title>', 1)
open(p, 'w', encoding='utf-8').write(s)

# Экзамен второго уровня (23.11.2026) — полная версия пробного экзамена (задания из probnyj/data.py, режим 'k')
# → proverka/ekzamen.html. Свой key: попытки не смешиваются с пробным экзаменом.
import os, sys, re
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'engine')); sys.path.insert(0, os.path.join(H, '..', 'probnyj'))
import data
from common import build_work
build_work(data.tasks, [('k', 'ekzamen.html', 'Экзамен: второй уровень', 'Экзамен')],
   key='ekzamen-2-v1', hero='ٱخۡتِبَارٌ', sub='заданий по всем темам второго уровня',
   group=True, gen=data.GEN, parts=data.PARTS)

# Надписи шаблона «контрольная» → «экзамен» (только в этом файле)
p = os.path.join(H, '..', '..', '..', 'proverka', 'ekzamen.html'); s = open(p, encoding='utf-8').read()
for a, b in [('Итог контрольной', 'Итог экзамена'), ('Контрольная сдана', 'Экзамен сдан'), ('Завершить контрольную?', 'Завершить экзамен?'),
             ('Контрольная сдана от 50 баллов', 'Экзамен сдан от 50 баллов')]:
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)

# Превью ссылки в WhatsApp / Telegram: общая обложка курса + название экзамена
U = 'https://dzhos7465-dotcom.github.io/tajweed-kurs/'
og = ('<meta property="og:type" content="website">\n<meta property="og:title" content="Экзамен · второй уровень">\n'
      '<meta property="og:description" content="Курс таджвида: 30 заданий по всем темам второго уровня">\n'
      '<meta property="og:url" content="%sproverka/ekzamen.html">\n<meta property="og:image" content="%spreview-ekzamen.jpg">\n'
      '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:type" content="image/jpeg">\n'
      '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="%spreview-ekzamen.jpg">\n') % (U, U, U)
s = open(p, encoding='utf-8').read()
s = re.sub(r'<meta (property|name)="(og|twitter):[^>]*>\n', '', s); s = s.replace('<title>', og + '<title>', 1)
open(p, 'w', encoding='utf-8').write(s)

# Экзамен второго уровня (23.11.2026) — полная версия пробного экзамена (задания из probnyj/data.py, режим 'k')
# → proverka/ekzamen.html. Свой key: попытки не смешиваются с пробным экзаменом.
import os, sys
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

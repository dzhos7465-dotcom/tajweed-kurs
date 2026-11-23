# Экзамен второго уровня (23.11.2026) — полная версия пробного экзамена (задания из probnyj/data.py, режим 'k')
# → proverka/ekzamen.html. Свой key: попытки не смешиваются с пробным экзаменом.
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'engine')); sys.path.insert(0, os.path.join(H, '..', 'probnyj'))
import data
from common import build_work
build_work(data.tasks, [('k', 'ekzamen.html', 'Экзамен: второй уровень', 'Экзамен')],
   key='ekzamen-2-v1', hero='ٱلۡمُرَاجَعَةُ', sub='заданий по всем темам второго уровня',
   group=True, gen=data.GEN, parts=data.PARTS)

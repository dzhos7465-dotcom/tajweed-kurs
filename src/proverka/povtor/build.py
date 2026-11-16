# Сборка контрольной и тренажёра-повторения (встреча двух сукунов, знаки остановки, три идгама)
# → proverka/povtor-kontrolnaya.html, proverka/povtor-trenazher.html
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'engine'))
import data
from common import build_work
build_work(data.tasks, [
    ('k', 'povtor-kontrolnaya.html', 'Контрольная: встреча двух сукунов, знаки остановки, три идгама', 'Повторение · Контрольная'),
    ('t', 'povtor-trenazher.html', 'Тренажёр: встреча двух сукунов, знаки остановки, три идгама', 'Повторение · Тренажёр'),
], key='povtor-kontrolnaya-v1', hero='ٱلۡمُرَاجَعَةُ', sub='заданий: встреча двух сукунов, знаки остановки, три идгама',
   group=True, gen=data.GEN, nocond=True)

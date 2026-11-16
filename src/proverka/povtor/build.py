# Сборка тренажёра-повторения: встреча двух сукунов, знаки остановки, три идгама → proverka/povtor-trenazher.html
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'engine'))
import data
from common import build_work
build_work(data.tasks, [
    ('t', 'povtor-trenazher.html', 'Тренажёр: встреча двух сукунов, знаки остановки, три идгама', 'Повторение · Тренажёр'),
], key='povtor-trenazher-v1', hero='ٱلۡمُرَاجَعَةُ', sub='заданий: встреча двух сукунов, знаки остановки, три идгама',
   group=False, gen=data.GEN)

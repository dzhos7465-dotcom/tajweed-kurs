# Сборка пробного экзамена → proverka/probnyj-kontrolnaya.html (ученикам), proverka/probnyj-trenazher.html (урок)
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'engine'))
import data
from common import build_work
build_work(data.tasks, [
    ('k', 'probnyj-kontrolnaya.html', 'Пробный экзамен: второй уровень', 'Пробный экзамен'),
    ('t', 'probnyj-trenazher.html', 'Тренажёр к экзамену: второй уровень', 'Тренажёр к экзамену'),
], key='probnyj-ekzamen-v1', hero='ٱلۡمُرَاجَعَةُ', sub='заданий по всем темам второго уровня',
   group=True, gen=data.GEN, parts=data.PARTS)

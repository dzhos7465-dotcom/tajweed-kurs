# Сборка контрольной и тренажёра по темам до мадда → proverka/do-madda-kontrolnaya.html, proverka/do-madda-trenazher.html
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'engine'))
import data
from common import build_work
build_work(data.tasks, [
    ('k', 'do-madda-kontrolnaya.html', 'Контрольная: темы до мадда', 'До мадда · Контрольная'),
    ('t', 'do-madda-trenazher.html', 'Тренажёр: темы до мадда', 'До мадда · Тренажёр'),
], key='do-madda-kontrolnaya-v1', hero='ٱلتَّجۡوِيدُ', sub='заданий: от полнозвучных букв до калькали',
   group=True, gen=data.GEN, how=data.HOW)

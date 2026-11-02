# Сборка контрольной и тренажёра по мадду → proverka/madd-kontrolnaya.html, proverka/madd-trenazher.html
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'engine'))
import data
from common import build_work
build_work(data.tasks, [
    ('k', 'madd-kontrolnaya.html', 'Контрольная по правилам мадда', 'Мадд · Контрольная'),
    ('t', 'madd-trenazher.html', 'Тренажёр: правила мадда', 'Мадд · Тренажёр'),
])

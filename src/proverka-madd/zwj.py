# Связка арабских букв через границы <span> для Safari/iPhone: вставляем ZWJ (U+200D)
# с обеих сторон границы, если буква перед границей соединяется с последующей.
import re, unicodedata as u
NONLEFT = set('اأإآٱدذرزوؤةىءۥۦ')          # не соединяются со следующей буквой
def _is_letter(c): return u.category(c) in ('Lo', 'Lm') and '؀' <= c <= 'ۿ' or c == 'ـ'
TAG = r'(?:</?span\b[^>]*>)+'
PAT = re.compile(r'([ء-يٱ-ۓـ])([ً-ٰٟۖ-ۭ]*)(' + TAG + r')(?=[ء-يٱ-ۓـ])')
def fix(html):
    def rep(m):
        if m.group(1) in NONLEFT: return m.group(0)
        return m.group(1) + m.group(2) + '‍' + m.group(3) + '‍'
    return PAT.sub(rep, html)

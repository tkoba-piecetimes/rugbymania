"""Expand official HTML tables without discarding row/column spans."""
import re
import unicodedata
from html import unescape

def text(raw):
    raw = re.sub(r'<(?:del|s|strike)\b[^>]*>.*?</(?:del|s|strike)>', '', raw, flags=re.S|re.I)
    return unicodedata.normalize('NFC', re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]*>', ' ', raw))).strip())

def tables(html):
    for raw in re.findall(r'<table\b[^>]*>(.*?)</table>', html, re.S|re.I):
        carry, rows = {}, []
        for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>', raw, re.S|re.I):
            cells = re.findall(r'<(td|th)\b([^>]*)>(.*?)</\1>', row, re.S|re.I)
            if not cells: continue
            expanded = {}; next_carry = {}
            for col, (val, left) in carry.items():
                expanded[col] = val
                if left > 1: next_carry[col] = (val, left-1)
            col = 0
            for tag, attrs, val in cells:
                while col in expanded: col += 1
                spans = {}
                for key in ('rowspan','colspan'):
                    m=re.search(key+r'\s*=\s*[\"\']?(\d+)',attrs,re.I)
                    spans[key]=int(m.group(1)) if m else 1
                for offset in range(spans['colspan']):
                    expanded[col+offset]=val
                    if spans['rowspan']>1:next_carry[col+offset]=(val,spans['rowspan']-1)
                col += spans['colspan']
            carry=next_carry
            rows.append(([expanded.get(i,'') for i in range(max(expanded)+1)],all(c[0].lower()=='th' for c in cells)))
        yield rows

def clean_team(raw):
    name=text(raw)
    name=re.sub(r'\s*[（(][^）)]*(?:の勝者|の敗者)[^）)]*[）)]', '', name)
    name=re.sub(r'\s+[ABCＤD][12]?\s*\d+位.*$', '', name)
    return name.strip()

def score(raw):
    value=text(raw)
    if any(w in value for w in ('不戦','棄権','中止','延期','抽選')):
        return None, None, 'cancelled' if '中止' in value else 'unscored', value
    m=re.match(r'\s*(\d+)\s*[-－ー−–]\s*(\d+)',value)
    if m:return int(m[1]),int(m[2]),'played',''
    return None,None,'scheduled','' if value in ('','-','vs','VS') else value

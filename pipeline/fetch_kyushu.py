# -*- coding: utf-8 -*-
"""Kyushu 2021 I/II and 2022–2026 A–D official schedules and results."""
import re
from urllib.parse import urljoin
from common import fetch, match_date_iso, compute_standings, build_teams
from html_tables import tables, text, clean_team, score
from team_slugs import slug_for

BASE = "https://www.rugby-kyushu.jp"
CURRENT_SEASON = 2026
HISTORY_SEASONS = [2025, 2024, 2023, 2022, 2021]


def season_url(year):
    return f"{BASE}/kyushuleague/{year}-{year+1}/kyushugakusei.html"


def split_sections(html):
    headings=list(re.finditer(r'<h([23])\b[^>]*>(.*?)</h\1>',html,re.S|re.I))
    return {text(h[2]):html[h.end():headings[i+1].start() if i+1<len(headings) else len(html)] for i,h in enumerate(headings)}


def parse_matches(html, label, year):
    matches=[]
    for rows in tables(html):
        if not rows:continue
        headers=[text(c) for c in rows[0][0]]
        ko=next((i for i,h in enumerate(headers) if h in ('キックオフ','開始時間','時間','KO時間')),None)
        if ko is None:continue
        home=ko+1
        for row,is_header in rows[1:]:
            if is_header or len(row)<=home+2:continue
            a,b=clean_team(row[home]),clean_team(row[home+2])
            if not a or not b or '大学' not in a or '大学' not in b:continue
            if any(t in a+b for t in ('位','の勝者','の敗者')):continue
            raw_date=' '.join(text(c) for c in row[1:ko])
            if '月' in headers and '日' in headers:
                mo,day=text(row[headers.index('月')]),text(row[headers.index('日')])
                date=match_date_iso(int(mo),int(day),year) if mo.isdigit() and day.isdigit() else None
            else:
                dm=re.fullmatch(r'(\d{1,2})月(\d{1,2})日(?:[（(][^）)]*[）)])?',raw_date)
                date=match_date_iso(int(dm[1]),int(dm[2]),year) if dm else None
            hs,away,status,note=score(row[home+1])
            if date is None:note=' / '.join(x for x in (note,'日程：'+raw_date) if x)
            detail=re.search(r'href=[\"\']([^\"\']+)',row[home+1])
            matches.append(dict(id=f"{date or 'tbd'}-{slug_for(a)}-vs-{slug_for(b)}",date=date,
                time=text(row[ko]) or '未定',category=label,home=a,away=b,home_slug=slug_for(a),away_slug=slug_for(b),
                home_score=hs,away_score=away,status=status,venue=text(row[home+3]) if len(row)>home+3 else '未定',
                note=note,source_url=urljoin(season_url(year),detail[1]) if detail else season_url(year)))
    return sorted(matches,key=lambda m:(m['date'] or '9999',m['time'],m['id']))


def fetch_season(year):
    html=fetch(season_url(year))
    result={}
    for heading,body in split_sections(html).items():
        if year==2021:
            codes={'九州学生リーグⅠ部':('kyushu-1','九州学生リーグⅠ部（2021年）'),'九州学生リーグⅡ部':('kyushu-2','九州学生リーグⅡ部（2021年）')}
            if heading not in codes:continue
            code,label=codes[heading]
        else:
            m=re.fullmatch(r'(?:リーグ([ABCD])|([ABCD])リーグ)',heading)
            if not m:continue
            letter=m[1] or m[2];code='kyushu-'+letter.lower();label='九州学生リーグ'+letter
        matches=parse_matches(body,label,year)
        if not matches:continue
        result[code]=dict(matches=matches,standings=compute_standings(matches,slug_for),teams=build_teams(matches,slug_for),label=label,source_url=season_url(year),coverage_note='公式掲載の対戦チーム確定済み試合。未確定枠・別見出しの順位決定戦は除外。不戦・中止はスコア集計対象外。')
    expected={'kyushu-1','kyushu-2'} if year==2021 else {'kyushu-a','kyushu-b','kyushu-c','kyushu-d'}
    if set(result)!=expected:raise ValueError(f"{year}: missing categories {expected-set(result)}")
    return result


def main():
    from season_sync import sync
    sync(fetch_season,[CURRENT_SEASON]+HISTORY_SEASONS,CURRENT_SEASON,'九州','九州ラグビーフットボール協会')


if __name__ == '__main__':main()

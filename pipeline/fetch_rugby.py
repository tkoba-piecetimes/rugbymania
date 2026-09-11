# -*- coding: utf-8 -*-
"""関東ラグビーフットボール協会（rugby.or.jp）から大学ラグビーの日程・結果・順位を取得し、
data/leagues/<code>/ に正規化JSONとして保存する（当シーズン）。
過去シーズンは data/leagues/<code>/history/<year>.json に保存する。

データ出典: 関東ラグビーフットボール協会 (https://www.rugby.or.jp/)
カテゴリのURL数値IDは年度ごとに変わるため、毎回シーズントップページから動的に解決する。
"""
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

from common import fetch, match_date_iso, compute_standings, build_teams
from team_slugs import slug_for

BASE = "https://www.rugby.or.jp"
CURRENT_SEASON = 2026        # 表示中の「現シーズン」（開幕直後で薄いことがある）
HISTORY_SEASONS = [2025, 2024, 2023, 2022, 2021]
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "leagues"

# (大分類, 小分類) -> (リーグコード, 表示名)
# 対抗戦A/B・リーグ戦1/2部はHTML掲載。リーグ戦3部以下はPDF配布のみで
# 構造化データが取れないため対象外（data/rugby-sources.md参照）。
TARGET_CATEGORIES = {
    ("関東大学対抗戦", "Aグループ"): ("kanto-taiko-a", "関東大学対抗戦Aグループ"),
    ("関東大学対抗戦", "Bグループ"): ("kanto-taiko-b", "関東大学対抗戦Bグループ"),
    ("関東大学リーグ戦", "1部"): ("kanto-league-1", "関東大学リーグ戦1部"),
    ("関東大学リーグ戦", "2部"): ("kanto-league-2", "関東大学リーグ戦2部"),
}

CATEGORY_BLOCK_RE = re.compile(
    r"<li><span>([^<]+)</span>\s*<ul>(.*?)</ul>\s*</li>", re.DOTALL)
SUBLINK_RE = re.compile(r'<a href="/univ/result/(\d+)/">([^<]+)</a>')
DATE_BLOCK_RE = re.compile(
    r'<h3 class="middle">(\d{1,2})月(\d{1,2})日[^<]*</h3>\s*'
    r'<ul class="gameSche">(.*?)</ul>', re.DOTALL)
MATCH_RE = re.compile(
    r'<li>\s*<div class="kotime">([^<]*)</div>\s*'
    r'<div class="team( win)?">([^<]*)</div>\s*'
    r'<div class="result">.*?'
    r'(?:<span>(\d+)</span><span>-</span><span>(\d+)</span>|<div class="score">-</div>)'
    r'.*?'
    r'<div class="team( win)?">([^<]*)</div>\s*'
    r'<div class="stadium">([^<]*)</div>',
    re.DOTALL)


def discover_categories(season_year: int) -> dict[str, dict]:
    """シーズントップページから対象カテゴリのIDを動的に解決する。"""
    html = fetch(f"{BASE}/univ/result/nendo-{season_year}/")
    found = {}
    for major, block in CATEGORY_BLOCK_RE.findall(html):
        for cat_id, minor in SUBLINK_RE.findall(block):
            key = (major.strip(), minor.strip())
            if key in TARGET_CATEGORIES:
                code, label = TARGET_CATEGORIES[key]
                found[code] = {"id": cat_id, "label": label}
    return found


def parse_matches(html: str, category_label: str, season_start_year: int) -> list[dict]:
    from html_tables import text, score
    matches=[]
    for mo,dd,block in DATE_BLOCK_RE.findall(html):
        d=match_date_iso(int(mo),int(dd),season_start_year)
        for item in re.findall(r'<li\b[^>]*>(.*?)</li>',block,re.S):
            teams=re.findall(r'<div class="team(?: win)?">(.*?)</div>',item,re.S)
            if len(teams)!=2:continue
            home,away=map(text,teams)
            ko=re.search(r'<div class="kotime">(.*?)</div>',item,re.S)
            venue=re.search(r'<div class="stadium">(.*?)</div>',item,re.S)
            field=re.search(r'<div class="score">(.*?)</div>',item,re.S)
            if field is None:
                field=re.search(r'<span class="noscore">(.*?)</span>',item,re.S)
            if field is None:raise ValueError('Missing score field')
            hs,as_,status,note=score(field[1])
            memo=re.search(r'<div class="memo">(.*?)</div>',item,re.S)
            if memo and any(w in text(memo[1]) for w in ('中止','棄権','不戦','延期')):
                hs,as_,status,note=score(memo[1])
            matches.append(dict(id=f'{d}-{slug_for(home)}-vs-{slug_for(away)}',date=d,time=text(ko[1]) if ko else '未定',
                category=category_label,home=home,away=away,home_slug=slug_for(home),away_slug=slug_for(away),
                venue=text(venue[1]) if venue else '未定',status=status,home_score=hs,away_score=as_,note=note))
    return matches


def fetch_season(season_year: int) -> dict[str, dict]:
    """1シーズン分、全カテゴリの matches/standings/teams/meta をまとめて返す。"""
    categories = discover_categories(season_year)
    result = {}
    for code, info in categories.items():
        html = fetch(f"{BASE}/univ/result/{info['id']}/")
        matches = parse_matches(html, info["label"], season_year)
        if not matches:
            continue
        for match in matches:
            match["source_url"] = f"{BASE}/univ/result/{info['id']}/"
        result[code] = {
            "matches": matches,
            "standings": compute_standings(matches, slug_for),
            "teams": build_teams(matches, slug_for),
            "label": info["label"],
            "source_url": f"{BASE}/univ/result/{info['id']}/",
        }
    if len(result)!=len(TARGET_CATEGORIES):
        raise ValueError(f"{season_year}: incomplete league import")
    return result


def main() -> None:
    from season_sync import sync
    sync(fetch_season, [CURRENT_SEASON] + HISTORY_SEASONS, CURRENT_SEASON, "関東", "関東ラグビーフットボール協会")


if __name__ == "__main__":
    main()

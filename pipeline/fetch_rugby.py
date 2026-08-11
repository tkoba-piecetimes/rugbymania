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
HISTORY_SEASONS = [2025, 2024, 2023]
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
    matches = []
    for mo, dd, block in DATE_BLOCK_RE.findall(html):
        d_iso = match_date_iso(int(mo), int(dd), season_start_year)
        for kotime, _, home, hs, as_, _, away, venue in MATCH_RE.findall(block):
            home, away = home.strip(), away.strip()
            venue = venue.strip()
            played = bool(hs and as_)
            matches.append({
                "id": f"{d_iso or 'tbd'}-{slug_for(home)}-vs-{slug_for(away)}",
                "date": d_iso,
                "time": kotime.strip() or "未定",
                "category": category_label,
                "home": home,
                "away": away,
                "home_slug": slug_for(home),
                "away_slug": slug_for(away),
                "venue": venue or "未定",
                "status": "played" if played else "scheduled",
                "home_score": int(hs) if played else None,
                "away_score": int(as_) if played else None,
                "note": "",
            })
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
        result[code] = {
            "matches": matches,
            "standings": compute_standings(matches, slug_for),
            "teams": build_teams(matches, slug_for),
            "label": info["label"],
        }
    return result


def main() -> None:
    # ---- 当シーズン
    try:
        current = fetch_season(CURRENT_SEASON)
    except Exception as e:
        print(f"当シーズンの取得に失敗: {e}", file=sys.stderr)
        current = {}

    # ---- 過去シーズン（先に全部集めて、当シーズンにまだ無いカテゴリも
    #      「過去データはあるが今季はまだ」として拾えるようにする）
    history_by_code: dict[str, list[tuple[int, dict]]] = {}
    for year in HISTORY_SEASONS:
        try:
            season = fetch_season(year)
        except Exception as e:
            print(f"{year}シーズンの取得に失敗: {e}", file=sys.stderr)
            continue
        for code, d in season.items():
            history_by_code.setdefault(code, []).append((year, d))

    all_codes = set(current) | set(history_by_code)
    ok = 0
    for code in sorted(all_codes):
        label = (current[code]["label"] if code in current
                 else history_by_code[code][0][1]["label"])
        d = current.get(code, {"matches": [], "standings": {"総合": []}, "teams": {}})
        if not d["teams"] and code in history_by_code:
            # 当季チームがまだ確定していない場合、直近の過去シーズンの
            # チーム一覧を採用してチームページの入り口を確保する。
            d = dict(d)
            d["teams"] = build_teams(history_by_code[code][0][1]["matches"], slug_for)
        out_dir = DATA_DIR / code
        out_dir.mkdir(parents=True, exist_ok=True)
        played = sum(1 for m in d["matches"] if m["status"] == "played")
        meta = {
            "code": code,
            "region": "関東",
            "gender": "男子",
            "group": "対抗戦" if code.startswith("kanto-taiko") else "リーグ戦",
            "league": label,
            "season_year": CURRENT_SEASON,
            "source": "関東ラグビーフットボール協会",
            "source_url": f"{BASE}/univ/",
            "source_updated_at": date.today().isoformat(),
            "fetched_at": datetime.now().isoformat(timespec="seconds"),
        }
        (out_dir / "matches.json").write_text(
            json.dumps(d["matches"], ensure_ascii=False, indent=1), encoding="utf-8")
        (out_dir / "standings.json").write_text(
            json.dumps(d["standings"], ensure_ascii=False, indent=1), encoding="utf-8")
        (out_dir / "teams.json").write_text(
            json.dumps(d["teams"], ensure_ascii=False, indent=1), encoding="utf-8")
        (out_dir / "meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{code}: {label} 当季試合{len(d['matches'])}件(結果{played}) チーム{len(d['teams'])}"
              + ("" if code in current else " [当季データなし・過去のみ]"))
        ok += 1

        hist_dir = out_dir / "history"
        for year, hd in history_by_code.get(code, []):
            hist_dir.mkdir(parents=True, exist_ok=True)
            hplayed = sum(1 for m in hd["matches"] if m["status"] == "played")
            out = {"year": year, "league": hd["label"],
                   "matches": hd["matches"], "standings": hd["standings"]}
            (hist_dir / f"{year}.json").write_text(
                json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  {year}/{code}: 試合{len(hd['matches'])}件(結果{hplayed})")

    print(f"done: {ok}/{len(TARGET_CATEGORIES)} categories")


if __name__ == "__main__":
    main()

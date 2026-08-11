# -*- coding: utf-8 -*-
"""関西ラグビーフットボール協会（rugby-kansai.or.jp）から大学ラグビーの日程・結果・
順位を取得し、data/leagues/<code>/ に正規化JSONとして保存する。

データ出典: 関西ラグビーフットボール協会 (https://rugby-kansai.or.jp/)
対象: 関西大学Aリーグ・Bリーグ・Cリーグ（C1のみ。C2A/C2Bは下位ブロックのため対象外）。
年度別ページが `/gameuniversity`（当年度）`/gameuniversity{year}`（過去年度）として
固定URLで存在するため、rugby.or.jpと違い動的なID解決は不要。
試合は節ごとの日程グリッド（class="sche_cont7"）で、スコアは
`<a class="score-link">NN - NN</a>` として埋め込まれている（未消化はプレーンテキスト"vs"）。
"""
import json
import re
from datetime import date, datetime
from pathlib import Path

from common import fetch, match_date_iso, compute_standings, build_teams
from team_slugs import slug_for

BASE = "https://rugby-kansai.or.jp"
CURRENT_SEASON = 2026
# 2023年度以前はCSSグリッド（sche_cont7）ではなく旧<table>形式（列構成が別物）で
# 配信されており本パーサーでは非対応のため、取得できる直近2シーズンのみとする。
HISTORY_SEASONS = [2025, 2024]
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "leagues"

# 見出しテキストの末尾で判定（年度によって先頭にスポンサー名が付くことがあるため）。
# Cリーグ以下はC1/C2の区分が年度によってグリッドが分かれていたり結合されていたり
# 一貫しない（data/rugby-sources.md参照）ため対象外とし、A/Bリーグのみを扱う。
LEAGUE_SUFFIXES = {
    "Aリーグ": ("kansai-a", "関西大学ラグビーAリーグ"),
    "Bリーグ": ("kansai-b", "関西大学ラグビーBリーグ"),
}

# 見出しタグはh4のこともpのこともある（年度・リーグによって揺れる）
HEADING_RE = re.compile(r'<(?:h4|p) class="daiji">([^<]+)</(?:h4|p)>', re.DOTALL)
DATE_RE = re.compile(r"(\d{1,2})月(\d{1,2})日")
MATCH_RE = re.compile(
    r'<div style="background:[^"]*;">([^<]*)</div>'          # 1 節
    r'<div style="background:[^"]*;">([^<]*)</div>'          # 2 日程
    r'<div style="background:[^"]*;">([^<]*)</div>'          # 3 K.O.
    r'<div style="background:[^"]*;">([^<]*)</div>'          # 4 team1
    r'<div style="background:[^"]*;">(vs|<div class="score-cell">.*?</div></div>)</div>'  # 5
    r'<div style="background:[^"]*;">([^<]*)</div>'          # 6 team2
    r'<div style="background:[^"]*;">([^<]*)</div>',         # 7 venue
    re.DOTALL)
# スコアは <a class="score-link"> のことも <span class="score-text"> のことも
# あるため、score-main の中身をテキストとして取り出してから数字を拾う。
SCORE_MAIN_RE = re.compile(r'<div class="score-main"[^>]*>(.*?)</div>', re.DOTALL)
SCORE_NUM_RE = re.compile(r"(\d+)\s*[-－ー−]\s*(\d+)")


def clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", s).strip()


def only_first_grid(html: str) -> str:
    """1節に複数の sche_cont7 グリッドが並ぶ場合（例: Cリーグ内のC1・C2）、
    最初のグリッドだけに絞る。"""
    first = html.find('class="sche_cont7"')
    if first == -1:
        return html
    second = html.find('class="sche_cont7"', first + 1)
    return html[first:second] if second != -1 else html[first:]


def season_url(year: int) -> str:
    return f"{BASE}/gameuniversity" if year == CURRENT_SEASON else f"{BASE}/gameuniversity{year}"


def split_sections(html: str) -> dict[str, str]:
    """<h4 class="daiji">見出しごとにHTMLを分割する。"""
    heads = list(HEADING_RE.finditer(html))
    sections = {}
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(html)
        sections[m.group(1).strip()] = html[m.end():end]
    return sections


def parse_matches(section_html: str, category_label: str, season_start_year: int) -> list[dict]:
    matches = []
    for round_, nittei, ko, team1, field5, team2, venue in MATCH_RE.findall(section_html):
        team1, team2, venue = team1.strip(), team2.strip(), venue.strip()
        if not team1 or not team2 or "位" in team1 or "位" in team2:
            continue  # 入替戦の未確定枠（"A8位" 等）はスキップ
        dm = DATE_RE.search(nittei)
        if not dm:
            continue  # 日程未定（"未定"）の枠はスキップ
        d_iso = match_date_iso(int(dm.group(1)), int(dm.group(2)), season_start_year)
        main_m = SCORE_MAIN_RE.search(field5)
        sm = SCORE_NUM_RE.search(clean(main_m.group(1))) if main_m else None
        played = bool(sm)
        hs, as_ = (int(sm.group(1)), int(sm.group(2))) if played else (None, None)
        matches.append({
            "id": f"{d_iso or 'tbd'}-{slug_for(team1)}-vs-{slug_for(team2)}",
            "date": d_iso,
            "time": ko.strip() or "未定",
            "category": category_label,
            "home": team1,
            "away": team2,
            "home_slug": slug_for(team1),
            "away_slug": slug_for(team2),
            "venue": venue or "未定",
            "status": "played" if played else "scheduled",
            "home_score": hs,
            "away_score": as_,
            "note": "",
        })
    return matches


def fetch_season(season_year: int) -> dict[str, dict]:
    html = fetch(season_url(season_year))
    sections = split_sections(html)
    result = {}
    for heading, body in sections.items():
        code = label = None
        for suffix, (c, lbl) in LEAGUE_SUFFIXES.items():
            if heading.endswith(suffix):
                code, label = c, lbl
                break
        if code is None:
            continue
        # Cリーグ節にはC1本体の下にC2A/C2Bのグリッドも続くことがあるため、
        # 最初の日程グリッド（=C1）だけに絞る。A/Bはグリッドが1つだけなので影響なし。
        body = only_first_grid(body)
        matches = parse_matches(body, label, season_year)
        if not matches:
            continue
        result[code] = {
            "matches": matches,
            "standings": compute_standings(matches, slug_for),
            "teams": build_teams(matches, slug_for),
            "label": label,
        }
    return result


def main() -> None:
    import sys

    try:
        current = fetch_season(CURRENT_SEASON)
    except Exception as e:
        print(f"当シーズンの取得に失敗: {e}", file=sys.stderr)
        current = {}

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
            d = dict(d)
            d["teams"] = build_teams(history_by_code[code][0][1]["matches"], slug_for)
        out_dir = DATA_DIR / code
        out_dir.mkdir(parents=True, exist_ok=True)
        played = sum(1 for m in d["matches"] if m["status"] == "played")
        meta = {
            "code": code,
            "region": "関西",
            "gender": "男子",
            "group": "関西大学リーグ",
            "league": label,
            "season_year": CURRENT_SEASON,
            "source": "関西ラグビーフットボール協会",
            "source_url": f"{BASE}/university",
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

    print(f"done: {ok}/{len(LEAGUE_SUFFIXES)} categories")


if __name__ == "__main__":
    main()

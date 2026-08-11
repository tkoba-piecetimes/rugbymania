# -*- coding: utf-8 -*-
"""九州ラグビーフットボール協会（rugby-kyushu.jp）から大学ラグビーの日程・結果・順位を
取得し、data/leagues/<code>/ に正規化JSONとして保存する。

データ出典: 九州ラグビーフットボール協会 (https://www.rugby-kyushu.jp/)
対象: 九州学生リーグA・B・C・D（4部制で、下位部を除外する必要がないくらい母数が
小さいため全部対象）。
年度別ページが `/kyushuleague/{year}-{year+1}/kyushugakusei.html` として固定URLで
存在する（rugby.or.jpのような動的ID解決は不要）。
試合表はNO/月/日/曜/開始時間/対戦①/対戦②/会場の列を持つ<table>で、同じ節・日付・
会場が複数試合にまたがる場合はrowspanで結合されているため、列ごとに繰越しながら
1行=1試合に展開する。スコアはPDFリンクのテキストとして「12-14」のように入っている。
"""
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

from common import fetch, match_date_iso, compute_standings, build_teams
from team_slugs import slug_for

BASE = "https://www.rugby-kyushu.jp"
CURRENT_SEASON = 2026        # 「2026-2027」シーズン（開幕前で日程のみのことがある）
HISTORY_SEASONS = [2025, 2024, 2023]
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "leagues"

LEAGUE_HEADINGS = {
    "リーグA": ("kyushu-a", "九州学生リーグA"),
    "リーグB": ("kyushu-b", "九州学生リーグB"),
    "リーグC": ("kyushu-c", "九州学生リーグC"),
    "リーグD": ("kyushu-d", "九州学生リーグD"),
}

HEADING_RE = re.compile(r"<h2>(.*?)</h2>", re.DOTALL)
TABLE_RE = re.compile(r"<table>(.*?)</table>", re.DOTALL)
ROW_RE = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)
CELL_RE = re.compile(r"<td([^>]*)>(.*?)</td>", re.DOTALL)
ROWSPAN_RE = re.compile(r'rowspan="(\d+)"')
# ハイフンは年度により半角"-"・全角"－"・長音"ー"等が混在するため広めに許容する
SCORE_RE = re.compile(r"(\d+)\s*[-－ー−]\s*(\d+)")

# 列: 節, 月, 日, 曜, 開始時間, team1, スコア, team2, 会場
N_COLS = 9


def season_url(year: int) -> str:
    return f"{BASE}/kyushuleague/{year}-{year + 1}/kyushugakusei.html"


def clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s or "")
    s = s.replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", s).strip()


def split_sections(html: str) -> dict[str, str]:
    heads = list(HEADING_RE.finditer(html))
    sections = {}
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(html)
        sections[m.group(1).strip()] = html[m.end():end]
    return sections


def flatten_rows(table_html: str) -> list[list[str]]:
    """rowspanで結合された表を、列ごとに値を繰り越しながら1行=1レコードに展開する。"""
    rows_out = []
    carry: list[str] = [""] * N_COLS
    remaining = [0] * N_COLS
    for row_html in ROW_RE.findall(table_html):
        if "<th" in row_html:
            continue  # ヘッダ行
        cells = CELL_RE.findall(row_html)
        cell_idx = 0
        values = [""] * N_COLS
        for col in range(N_COLS):
            if remaining[col] > 0:
                values[col] = carry[col]
                remaining[col] -= 1
            elif cell_idx < len(cells):
                attrs, content = cells[cell_idx]
                cell_idx += 1
                rs_m = ROWSPAN_RE.search(attrs)
                rs = int(rs_m.group(1)) if rs_m else 1
                values[col] = content
                if rs > 1:
                    carry[col] = content
                    remaining[col] = rs - 1
        rows_out.append(values)
    return rows_out


def parse_matches(section_html: str, category_label: str, season_start_year: int) -> list[dict]:
    m = TABLE_RE.search(section_html)
    if not m:
        return []
    matches = []
    for row in flatten_rows(m.group(1)):
        _round, month_raw, day_raw, _wd, time_raw, t1_raw, score_raw, t2_raw, venue_raw = row
        month_s, day_s = clean(month_raw), clean(day_raw)
        if not month_s.isdigit() or not day_s.isdigit():
            continue
        team1, team2 = clean(t1_raw), clean(t2_raw)
        if not team1 or not team2 or "位" in team1 or "位" in team2:
            continue
        d_iso = match_date_iso(int(month_s), int(day_s), season_start_year)
        sm = SCORE_RE.search(clean(score_raw))
        played = bool(sm)
        hs, as_ = (int(sm.group(1)), int(sm.group(2))) if played else (None, None)
        matches.append({
            "id": f"{d_iso or 'tbd'}-{slug_for(team1)}-vs-{slug_for(team2)}",
            "date": d_iso,
            "time": clean(time_raw) or "未定",
            "category": category_label,
            "home": team1,
            "away": team2,
            "home_slug": slug_for(team1),
            "away_slug": slug_for(team2),
            "venue": clean(venue_raw) or "未定",
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
        if heading not in LEAGUE_HEADINGS:
            continue
        code, label = LEAGUE_HEADINGS[heading]
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
            "region": "九州",
            "gender": "男子",
            "group": "九州学生リーグ",
            "league": label,
            "season_year": CURRENT_SEASON,
            "source": "九州ラグビーフットボール協会",
            "source_url": f"{BASE}/kyushuleague.html",
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

    print(f"done: {ok}/{len(LEAGUE_HEADINGS)} categories")


if __name__ == "__main__":
    main()

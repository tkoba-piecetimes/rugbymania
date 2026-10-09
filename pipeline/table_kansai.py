# -*- coding: utf-8 -*-
"""2026-09リニューアル後の関西協会サイト（league-schedule）の試合表パーサー。

`<tr data-schedule-match data-league="a|b|c|..." data-home data-away data-venue
data-date data-round data-result>` の行（表ビュー）から試合を取り出す。
K.O.・スコアは行内の <td>。入替戦(promotion)・ジュニア・コルツ等は対象外。
"""
import re
from html import unescape
from urllib.parse import urljoin

from html_tables import text, score
from team_slugs import slug_for

ROW_RE = re.compile(r'<tr\s+(data-schedule-match[^>]*)>(.*?)</tr>', re.S)
ATTR_RE = re.compile(r'data-([a-z-]+)="([^"]*)"')
TD_RE = re.compile(r'<td\b([^>]*)>(.*?)</td>', re.S)
LEAGUE_KEYS = {"kansai-a": "a", "kansai-b": "b"}


def has_rows(html: str) -> bool:
    return bool(ROW_RE.search(html))


def parse_all(html: str, source: str) -> dict[str, list[dict]]:
    """league key (a/b/...) -> matches。"""
    out: dict[str, list[dict]] = {}
    seen: set[str] = set()
    for head, body in ROW_RE.findall(html):
        a = {k: unescape(v) for k, v in ATTR_RE.findall(head)}
        league = a.get("league", "")
        home, away, date = a.get("home", "").strip(), a.get("away", "").strip(), a.get("date", "")
        if not home or not away or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            continue  # 日程未定
        if "大学" not in home or "大学" not in away:
            continue  # "ー" 等のプレースホルダ
        if "位" in home + away or "勝者" in home + away or "敗者" in home + away:
            continue  # 未確定枠
        tds = TD_RE.findall(body)
        time = text(tds[3][1]) if len(tds) > 3 else ""
        score_td = next((v for at, v in tds if "competition-schedule-score" in at), "")
        hs, as_, status, note = score(score_td)
        if status == "scheduled" and a.get("result") == "1" and re.search(r"[○〇◯✕×]", text(score_td)):
            status, note = "unscored", text(score_td)  # 不戦勝等（○ - ×）
        rnd = a.get("round", "")
        stage = f"第{rnd}節" if rnd.isdigit() else rnd or "リーグ戦"
        base = f"{date}-{slug_for(home)}-vs-{slug_for(away)}"
        mid, n = base, 2
        while mid in seen:
            mid, n = f"{base}-{n}", n + 1
        seen.add(mid)
        out.setdefault(league, []).append(dict(
            id=mid, date=date, time=time if re.search(r"\d", time) else "未定", category="",
            home=home, away=away, home_slug=slug_for(home), away_slug=slug_for(away),
            venue=a.get("venue", "").strip() or "未定", status=status,
            home_score=hs, away_score=as_, note=note, stage=stage,
            source_url=urljoin(source, a["detail-url"]) if a.get("detail-url") else source))
    for ms in out.values():
        ms.sort(key=lambda m: (m["date"], m["time"]))
    return out

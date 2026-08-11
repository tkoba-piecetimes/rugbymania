# -*- coding: utf-8 -*-
"""チーム名 → URLスラッグの対応表とスラッグ解決ロジック（ラグビー版）。

rugby.or.jp は「大東文化大」のような省略表記（大学→大）を使うため、
ラクロス版の team_slugs.py とはキー形式が異なる。
解決順: 1) 手動登録の対応表  2) pykakasiによるローマ字化  3) ハッシュフォールバック
"""
import re
import sys

TEAM_SLUGS = {
    # ---- 関東大学ラグビー対抗戦・リーグ戦（頻出校） ----
    "早稲田大": "waseda",
    "慶應義塾大": "keio",
    "明治大": "meiji",
    "帝京大": "teikyo",
    "筑波大": "tsukuba",
    "青山学院大": "aoyamagakuin",
    "日本体育大": "nittaidai",
    "大東文化大": "daitobunka",
    "東海大": "tokai",
    "法政大": "hosei",
    "流通経済大": "ryutsu-keizai",
    "関東学院大": "kantogakuin",
    "中央大": "chuo",
    "立教大": "rikkyo",
    "拓殖大": "takushoku",
    "日本大": "nihon",
    "東洋大": "toyo",
    "立正大": "rissho",
    "専修大": "senshu",
    "国士舘大": "kokushikan",
    "武蔵工業大": "musashi-kogyo",
    "東京都市大": "tokyo-city",
    "神奈川大": "kanagawa",
    "工学院大": "kogakuin",
    "桐蔭横浜大": "toin-yokohama",
    "東京理科大": "tokyo-rika",
    "駒澤大": "komazawa",
    "成城大": "seijo",
    "山梨学院大": "yamanashi-gakuin",
    "杏林大": "kyorin",
    "亜細亜大": "asia",
    "駿河台大": "surugadai",
    "上武大": "joubu",
    "城西大": "josai",
    "西武文理大": "seibu-bunri",
    "城西・関東学院": "josai-kantogakuin",
    "慶應義塾高": "keio-hs",
    "学習院大": "gakushuin",
}

_kks = None


def _romaji(name: str) -> str | None:
    global _kks
    try:
        if _kks is None:
            import pykakasi
            _kks = pykakasi.kakasi()
        base = re.sub(r"(大学院|大学|高校|高|大)$", "", name.strip())
        s = "".join(x["hepburn"] for x in _kks.convert(base))
        s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
        return s or None
    except Exception:
        return None


def slug_for(team: str) -> str:
    if team in TEAM_SLUGS:
        return TEAM_SLUGS[team]
    r = _romaji(team)
    if r:
        TEAM_SLUGS[team] = r
        return r
    print(f"[warn] スラッグ生成不可のチーム名: {team}", file=sys.stderr)
    return f"team-{abs(hash(team)) % 10**8}"

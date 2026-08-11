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

    # ---- 関西大学ラグビー（rugby-kansai.or.jpは「○○大学」のフル表記） ----
    "立命館大学": "ritsumeikan",
    "京都産業大学": "kyoto-sangyo",
    "摂南大学": "setsunan",
    "天理大学": "tenri",
    "関西大学": "kansai-u",
    "同志社大学": "doshisha",
    "近畿大学": "kindai",
    "関西学院大学": "kwansei-gakuin",
    "大阪体育大学": "osaka-taiiku",
    "京都大学": "kyoto-u",
    "甲南大学": "konan",
    "大阪経済大学": "osaka-keizai",
    "龍谷大学": "ryukoku",
    "大阪国際大学": "osaka-kokusai",
    "追手門学院大学": "otemon-gakuin",
    "大阪産業大学": "osaka-sangyo",
    "関西外国語大学": "kansaigaidai",
    "大阪工業大学": "osaka-kogyo",
    "大阪学院大学": "osaka-gakuin",
    "大阪大学": "osaka-u",
    "神戸大学": "kobe-u",
    "大阪公立大学": "osaka-metropolitan",
    "大阪教育大学": "osaka-kyoiku",
    "花園大学": "hanazono",

    # ---- 九州学生ラグビー（rugby-kyushu.jpも「○○大学」のフル表記） ----
    "福岡大学": "fukuoka-u",
    "西南学院大学": "seinan-gakuin",
    "九州共立大学": "kyushu-kyoritsu",
    "日本文理大学": "nihon-bunri",
    "鹿児島大学": "kagoshima-u",
    "福岡工業大学": "fukuoka-it",
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

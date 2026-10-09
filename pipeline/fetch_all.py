# -*- coding: utf-8 -*-
"""関東・関西・九州の3地区を順番に取得する（全国対応）。

1地区の取得失敗（協会サイトのリニューアル等）でサイト全体のデプロイを止めないよう、
地区ごとに失敗を握り、前回取得済みのデータ（season_syncは成功分を消さない）で続行する。
全地区が失敗した場合のみ異常終了する。
"""
import sys
import traceback

import fetch_kansai
import fetch_kyushu
import fetch_rugby


def main() -> None:
    regions = [
        ("関東（rugby.or.jp）", fetch_rugby.main),
        ("関西（rugby-kansai.or.jp）", fetch_kansai.main),
        ("九州（rugby-kyushu.jp）", fetch_kyushu.main),
    ]
    failed = []
    for name, run in regions:
        print(f"=== {name} ===")
        try:
            run()
        except Exception as exc:
            traceback.print_exc()
            failed.append(name)
            # GitHub Actions の注釈として残す（前回データのまま続行）
            print(f"::warning::{name} の取得に失敗したため前回データで続行: {exc}")
    if len(failed) == len(regions):
        sys.exit("全地区の取得に失敗しました")


if __name__ == "__main__":
    main()

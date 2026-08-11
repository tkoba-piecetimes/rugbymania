# -*- coding: utf-8 -*-
"""関東・関西・九州の3地区を順番に取得する（全国対応）。"""
import fetch_kansai
import fetch_kyushu
import fetch_rugby


def main() -> None:
    print("=== 関東（rugby.or.jp）===")
    fetch_rugby.main()
    print("=== 関西（rugby-kansai.or.jp）===")
    fetch_kansai.main()
    print("=== 九州（rugby-kyushu.jp）===")
    fetch_kyushu.main()


if __name__ == "__main__":
    main()

# ラグビーマニア — 全国大学ラグビー情報メディア

大学ラグビーの情報メディア「ラグビーマニア」（運営: PieceTimes）。
関東・関西・九州の3地区ラグビーフットボール協会が公開している対抗戦・リーグ戦の
試合結果ページから日程・結果を取得し、静的サイトを生成する。日本の大学ラグビーは
この3地区協会で全国を分担しているため、3地区対応＝実質の全国対応となる。

- 公開URL: 未公開（ドメイン取得後に設定）
- 対象:
  - 関東（rugby.or.jp）: 対抗戦A/Bグループ、リーグ戦1部・2部
    （3部以下はPDF配布のみで対象外）
  - 関西（rugby-kansai.or.jp）: Aリーグ・Bリーグ（C以下は年度で構造が一貫しないため対象外）
  - 九州（rugby-kyushu.jp）: リーグA・B・C・D
  - 詳細・除外理由は docs/rugby-sources.md 参照
- 直近2〜3シーズン分の過去データ、試合ページ（プレビュー/レポート・過去の対戦）、記録室

## 仕組み

```
rugby.or.jp / rugby-kansai.or.jp / rugby-kyushu.jp（地区ごとにHTML構造が異なる）
  → pipeline/fetch_rugby.py（関東）/ fetch_kansai.py（関西）/ fetch_kyushu.py（九州）
    ※ pipeline/common.py に共通ロジック（fetch/日付計算/順位集計）を集約
  → data/leagues/<region>-<category>/
  → pipeline/generate_site.py
  → site/
```

## 実行

```
python pipeline/fetch_all.py
python pipeline/generate_site.py
```

（地区ごとに個別実行したい場合は `pipeline/fetch_rugby.py` / `fetch_kansai.py` /
`fetch_kyushu.py` を単独で実行できる）

ローカル確認: `python -m http.server 8940 -d site`

## 未実装（今後）

- ドメイン取得・GitHub Pages カスタムドメイン設定
- GA4 / Search Console 連携
- 読みもの記事・用語辞典（content/articles/, content/glossary.json を追加すれば自動で有効化される）
- 関東リーグ戦3部以下・関西Cリーグ以下（構造化データが安定して取れないため対象外。
  docs/rugby-sources.md参照）
- アメフト・サッカーのスコアデータ所在の追加調査

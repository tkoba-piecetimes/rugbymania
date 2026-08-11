# ラグビーマニア — 関東大学ラグビー情報メディア

大学ラグビーの情報メディア「ラグビーマニア」（運営: PieceTimes）。
関東ラグビーフットボール協会（rugby.or.jp）が公開している対抗戦・リーグ戦の
試合結果ページから日程・結果を取得し、静的サイトを生成する。

- 公開URL: 未公開（ドメイン取得後に設定）
- 対象: 関東大学対抗戦A/Bグループ、関東大学リーグ戦1部・2部
  （3部以下はPDF配布のみで構造化データが取得できないため対象外。docs/rugby-sources.md参照）
- 過去3シーズン分のデータ、試合ページ（プレビュー/レポート・過去の対戦）、記録室

## 仕組み

```
rugby.or.jp（HTML、年度ごとにURLの数値IDが変わる）
  → pipeline/fetch_rugby.py: シーズントップページを都度スキャンしてID解決→取得
  → data/leagues/<category>/
  → pipeline/generate_site.py
  → site/
```

## 実行

```
python pipeline/fetch_rugby.py
python pipeline/generate_site.py
```

ローカル確認: `python -m http.server 8940 -d site`

## 未実装（今後）

- ドメイン取得・GitHub Pages カスタムドメイン設定
- GA4 / Search Console 連携
- 読みもの記事・用語辞典（content/articles/, content/glossary.json を追加すれば自動で有効化される）
- リーグ戦3部以下（PDF配布のため別途OCR等の対応が必要）

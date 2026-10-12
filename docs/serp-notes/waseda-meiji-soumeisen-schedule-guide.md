# SERP分析メモ: 早明戦 日程

- 対象KW: 早明戦 日程（KW在庫 H11・上位クエリ）
- 調査日: 2026-10-12
- slug: `waseda-meiji-soumeisen-schedule-guide`
- cta: sponsor / category: 観戦ガイド
- 執筆方式: ハイブリッド（設計・仕上げ=Opus／本文=Sonnet）

## 1. SERP 1ページ目の顔ぶれ（WebSearch「早明戦 日程」「早明戦 ラグビー いつ 2026年12月」）

| # | URL | 種別 | 内容 |
|---|---|---|---|
| 1 | https://www.city.kitakyushu.lg.jp/contents/k083_00036.html | 自治体 | 「ラグビー早明戦2026北九州大会」（2026-06-07 ミクニワールドスタジアム北九州）の告知。終了済みの春の試合 |
| 2 | https://www.city.kitakyushu.lg.jp/files/001197197.pdf | 自治体PDF | 同上のチラシ |
| 3 | https://www.meiji.ac.jp/campus/mnp/6t5h7p000012w57c-att/a1555041230956.pdf | 大学PDF | 過去年度の資料 |
| 4 | https://www.waseda.jp/inst/athletic/?p=54008 | 大学公式 | 2025年度早明戦（2025-12-07 国立）の学生券販売案内 |
| 5 | https://sportiva.shueisha.co.jp/clm/otherballgame/rugby/2016/12/03/___split_7/index.php | メディア | 2016年の早明戦コラム |
| 6 | https://www.waseda.jp/inst/weekly/feature/2013/11/18/46704/ | 大学公式 | 2013年の特集 |
| 7 | https://www.waseda.jp/inst/athletic/news/2026/06/10/58440/ | 大学公式 | 2026-06-07 春季大会早明戦の結果（早稲田28-24明治） |
| 8 | 辞書サイト（romajidesu / nihongomaster） | 辞書 | 語義のみ |

## 2. 共通点（検索意図の正解）

- 検索者が最優先で知りたいのは「今年の早明戦はいつ・どこで・何時キックオフか」と「チケットはいつ買えるか」。
- 歴史・伝統（1923年初対戦、国立開催、雪の早明戦）への関心も一定ある。

## 3. 上位陣に欠けている要素（差別化点）

1. **2026年12月6日（日）14:00 MUFG国立の対抗戦早明戦が上位にほぼ出てこない。** 上位は終了済みの6月の北九州大会（春季大会）や前年の販売案内で占められ、10月時点の検索者が「今年の本番」に辿り着けない。→ 冒頭で「春（6/7北九州・終了）」と「秋の対抗戦（12/6国立）」の2つがあることを整理し、12/6の情報と先行抽選・一般発売のスケジュール（関東協会チケットページ）を示す。
2. **直近の早明戦の結果を一次データでまとめた表がない。** → 自サイト保有の2021〜2025年度対抗戦データ（関東協会公式日程ページ由来）で5年分のスコア・会場を表にし、毎年12月第1日曜開催であることもデータで示す。
3. **「その年の早明戦が対抗戦の順位にどう関わるか」という視点がない。** 2026年度は両校とも早明戦が対抗戦の最終戦で、10/11時点で両校3戦全勝。→ 自サイトの順位表・試合ページ・チームページへ内部リンク。

## 4. 一次情報の出典

- 関東ラグビーフットボール協会 2026年度対抗戦A日程 https://www.rugby.or.jp/univ/result/2904/
- 関東ラグビーフットボール協会 チケット情報 https://www.rugby.or.jp/ticket/ （12/6早明戦: ぴあ先行抽選10/26〜29・チケラグ先行10/31〜11/3・一般発売11/6 18:00。席種・価格は個別記載なし＝2026-10-12確認）
- 関東協会 2025年度対抗戦A https://www.rugby.or.jp/univ/result/2803/ （2025-12-07 国立 明治25-19早稲田）
- 北九州市「ラグビー早明戦2026北九州大会」 https://www.city.kitakyushu.lg.jp/contents/k083_00036.html
- 早稲田大学競技スポーツセンター 2026春季大会結果 https://www.waseda.jp/inst/athletic/news/2026/06/10/58440/ （早稲田28-24明治）
- 早稲田大学競技スポーツセンター 2021年早明戦 https://www.waseda.jp/inst/athletic/?p=21955 （2021-12-05 秩父宮 早稲田17-7）
- web Sportiva 2023-12-04 https://sportiva.shueisha.co.jp/clm/otherballgame/rugby/2023/12/04/100_1/ （99回目・明治58-38・通算 明治42勝55敗2分・約31,915人・1973年から国立・1982年66,999人・1987年雪の早明戦）
- Number 2024-12-12 https://number.bunshun.jp/articles/-/863992 （2024-12-01が100回目）
- 自サイトデータ: data/leagues/kanto-taiko-a/history/2021〜2025.json, matches.json

## 5. 既存記事との棲み分け

- `university-rugby-first-watch-guide`（観戦マナー全般）、`university-rugby-strong-universities-ranking`（地区別勢力図）、`university-rugby-championship-titles-ranking`（選手権優勝回数）とは意図が異なる。本記事は「早明戦という1カードの日程・チケット・直近結果」に限定する。
- 更新型。毎年10月（チケット発表後）にリライトする。
- docs/primary-sources/ は本リポに存在しないため、取材由来の一次情報は使用していない。

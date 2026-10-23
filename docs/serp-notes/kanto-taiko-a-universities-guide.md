# SERP分析: 大学ラグビー 対抗戦Aグループ 所属大学 一覧と特色（K10）

- 調査日: 2026-10-23
- slug: kanto-taiko-a-universities-guide
- レーン: K（企画・一覧型）／類型: 観戦ガイド系＋進路系（cta: sponsor）

## インサイト
- 秋シーズン中に対抗戦を観始めたファン・保護者が「Aグループって何校？どんな大学？」を一度に把握したい
- 進学先を考える高校生が、Aグループ8校の拠点（グラウンド）や歴史、近年の勝敗を横並びで比べたい
- OB・観戦者が「今年の8校」と「直近数年で入れ替わった大学」を確認したい

## 検索クエリ（WebSearch）
- 「関東大学対抗戦Aグループ 所属大学 一覧 特徴」
- 「関東大学ラグビー対抗戦 2026 Aグループ 8校 日程」

## 上位の顔ぶれ
- PR配信・新聞記事（nikkan.co.jp releases、afpbb、hokkaido-np 等）: スポンサー契約・試合結果の単発ニュース
- 早稲田大学 競技スポーツセンター: 自校の試合告知のみ
- spocale.com: 試合単位の日程ページ（大学紹介なし）
- 個人サイト（ne.jp）・spread-sports 等: 古い・または単発の観戦記事

## 共通点（検索意図の正解）
- 8校の顔ぶれと今季の日程・順位を知りたい

## 上位に欠けている要素（差別化）
1. 8校を横並びで比べる一覧（創部年・活動拠点・公式サイト）が一次情報付きでまとまったページがない
2. 直近5シーズンの勝敗を大学別に並べたデータ（関東協会公表結果を自サイトで集計）がない
3. 年度による所属校の入れ替わり（2023年度は成蹊大学がA、日本体育大学がB）に触れた一覧がない

## 使う一次データ（自サイト）
- data/leagues/kanto-taiko-a/history/2021〜2025.json（関東ラグビーフットボール協会の公表結果を集計）
- data/leagues/kanto-taiko-a/standings.json（2026-10-22時点）
- site/kanto-taiko-a/clubs/<slug>/、standings/、schedule/、teams/、records/

## 公式情報（確認済み）
- 関東協会 2026年度 対抗戦A: https://www.rugby.or.jp/univ/result/2904/
- 早稲田: https://www.waseda.jp/inst/athletic/club/rugby/ （1918年創部・上井草グラウンド・大学選手権最多16回優勝）
- 慶應: https://www.keio.ac.jp/ja/about/public-relations/mita-hyoron/keioreport/202502-3/ （1899年創部・日本ラグビーの源流）、https://keiorugby.com/ （慶大日吉グラウンド）
- 明治: https://www.meijirugby.jp/team/ （1923年創部）、https://www.meiji.ac.jp/koho/disclosure/facilities/dormitory.html （八幡山・世田谷区、人工芝ラグビー場）
- 帝京: https://kyodonewsprwire.jp/release/202609015083 （学校法人帝京大学発表: 1970年創部・13回優勝・9連覇・ENJOY&TEAMWORK）、https://www.teikyo-sports.jp/rugby/team/ground/ （日野市百草・人工芝・屋根付きスタンド約600名）
- 筑波: https://shinkan-web.zdk.tsukuba.ac.jp/orgs/02043/ （1924年東京高等師範で誕生・2024年に100周年・CHUBU UT Field）
- 日体大: https://nssurfc.jp/history （1933年ラグビー部昇格・大学選手権優勝2回・対抗戦優勝5回）、https://nssurfc.jp/ （横浜健志台キャンパス ラグビー場）
- 青山学院: https://www.aoyama.ac.jp/sports_info/2024/news_20241211_01 （2024年に創部100年・第61回大学選手権に30大会ぶり3回目出場）、https://www.aogaku-rugby.com/ （緑が丘グラウンド）
- 立教: 創部年は公式情報で確認できず→非公表扱い。https://www.rikkyo.ac.jp/campuslife/facilities/fujimi/ （富士見総合グラウンドにラグビー場）

## 既存記事とのすみ分け
- university-rugby-strong-universities-ranking: 地区横断の勢力図（順位上位）。本記事は対抗戦A 8校の大学別プロフィール
- university-rugby-championship-titles-ranking: 選手権優勝回数。本記事では回数は公式に明記がある大学だけ触れ、詳細はリンク
- university-rugby-league-format-guide / kanto-university-rugby-irekaesen-guide: 制度解説。本記事はリンクのみ

# SERP分析メモ＋骨子: ラグビー 戦術用語集 50選（大学生向け）

作成日: 2026-11-04（設計担当）
対象KW: 「ラグビー 戦術用語集」（K9・企画レーン／近接: ラグビー 戦術用語 一覧、ラグビー 用語 ゲインライン、ラグビー ポッド 意味）
slug: `rugby-senjutsu-yougo-50-guide`
cta: `sponsor` ／ category: `技術`

---

## 1. インサイト（想定読者）

- 大学1〜2年の部員が、ミーティングや映像分析で「ポッド」「ゲインラインを切る」「ピラー」と言われても意味が分からず、指示についていけない。
- 高校から続けている部員でも、大学のコーチが使う英語由来の戦術用語（シェイプ、ドミナントキャリー、エグジット等）が初耳で、検索で一覧を探す。
- 学生コーチ・アナリストが、部内で用語の意味をそろえるための共通資料を探す。
- 2026年版競技規則の用語変更（ノックオン→ノックフォワード等）や、ジャッカラー／ユーズイットの正式な定義を確かめたい。

## 2. SERP確認結果（2026-11-04）

### 確認方法と限界（未確認事項）
- WebSearch は米国リージョン固定のため、日本語「ラグビー 戦術用語 一覧」「ラグビー 戦術用語集」の日本のGoogle上位10件そのものは取得できなかった（**日本SERPの順位は未確認**）。返ってきた顔ぶれは kotobank（日本大百科全書「ラグビーの用語」）、日本協会「ラグビーかんたん観戦ガイド」PDF、サントリーサンゴリアス「ラグビー大辞典」コラム（2012〜2015年・WebFetchは403で本文未読）、dxmagazine（W杯観戦向け基本用語）、英語のコーチングサイト（sportplan、rugbycoachweekly）。
- 既存の P18 メモ（`docs/serp-notes/rugby-glossary-beginner-guide.md`）で確認した「ラグビー 用語集 初心者」の上位（Descente、J SPORTS、All About、ノーサイドTV等）は、いずれも観戦者向けの五十音順辞典。

### WebFetchで読んだもの
- 日本協会「ラグビー基本用語解説」 https://www.rugby-japan.jp/guide/rugby/ — ポジション・得点・反則（ノックフォワード、スローフォワード、ノットロールアウェイ、ノットリリースザボール、オフサイド）・基本プレーのみ。**戦術用語（ゲインライン、フェーズ、オフロード、ポッド等）は掲載なし**。
- 日本協会 競技規則ページ https://www.rugby-japan.jp/future/rule/ → 2026年版競技規則PDF（日本語・159ページ）。「定義」章（PDF 20〜26ページ）を本文抽出して確認済み。
- World Rugby Laws「Definitions」 https://passport.world.rugby/laws-of-the-game/definitions/
- World Rugby「The principles of attack and defence」（攻撃=継続、防御=時間とスペースを奪う、ボールの争奪）
- World Rugby「Breakdown explained」「Multi-player tackles」
- Rugby World Cup 公式「Through or around? The art of getting over the gain line」（2019-09-20）
- Rugby World「What is the gainline in rugby?」（2023-07-04）
- RNZ「RWC: Beginners guide to rugby jargon」（2023-09-09）

### 共通点（検索意図の正解）
- 用語の意味を短く知りたい。辞典的な一覧性（カテゴリ別・1語1〜2文）が求められている。

### 上位陣に欠けている要素（差別化3行）
1. 日本語の上位は観戦者向けの基本用語が中心で、**ゲインライン・ポッド・シェイプ・ピラー・ドミナントキャリー等の「チーム内で使う戦術用語」をまとめた日本語ページが見当たらない**（日本協会の基本用語解説にも戦術用語はない）。
2. 競技規則に定義がある語（ジャッカラー、ユーズイット、ロイタリング、クイックスロー、マーク、50:22、ノックフォワード等）と、**規則に定義のない現場用語を区別して示す**記事がない。本記事は2026年版競技規則の「定義」章を一次情報として使い、各語に「規則上の定義あり／現場用語」を明記する。
3. 用語を「どの局面で・誰が使うか」（攻撃／防御／ブレイクダウン／セットプレー／キック）で整理し、当サイトの技術記事（ドリフト・ブリッツ、ブレイクダウン、モール、キック）と順位表・記録室に接続する。用語を覚えた後に「自分の所属リーグの試合を見返す」導線がある。

### カニバリ確認
- `rugby-glossary-beginner-guide`（P18）: 新入部員向けの基礎用語（ラック、モール、ノックオン、オフサイド、ポジション名、対抗戦/リーグ戦）。→ 本記事ではこれらの**基礎語の定義を繰り返さない**（冒頭で1行リンクして送る）。
- サイト内用語辞典 `/glossary/`（data/glossary.json 48語・基礎語中心。本文中の初出語には自動で用語リンクが付く）。→ 本記事は戦術語のみで重複しない。
- 技術記事: `rugby-defence-line-drift-blitz-guide`（ドリフト/ブリッツの詳細）、`rugby-breakdown-jackal-practice-guide`（ジャッカル/クリーナーの練習法）、`rugby-maul-technique-practice-guide`、`rugby-kicking-types-practice-guide`、`rugby-standoff-decision-making-guide`、`rugby-rule-kaisei-2026-guide`。→ 本記事は各語1〜2文の定義にとどめ、詳しい練習法は各記事へ送る（ハブ型）。

## 3. 採用用語50語（カテゴリ別）

凡例: 【規則】=2026年版競技規則の定義・条文にある語（出典=日本協会2026年版競技規則PDF／World Rugby Laws）。【現場】=競技規則に定義のないコーチング・現場用語（呼び方はチームや指導者で異なる場合がある、と本文で明示）。

### A. 攻撃の考え方と陣形（10）
1. ゲインライン【現場】— 直前のラック・モール・スクラム・ラインアウトの位置からタッチラインと平行に引いた想像上の線（出典: RWC公式2019、Rugby World 2023）
2. フェーズ（ファーストフェーズ）【規則+現場】— 規則上「プレーのフェーズ」はスクラム・ラインアウト・ラック・モール。現場ではタックル→ラックごとに攻撃の区切りを数える意味で使い、セットプレー直後の攻撃を「ファーストフェーズ」と呼ぶ（RWC公式2019）
3. フロントフットボール【現場】— 前に出た状態で素早く出せるボール。相手の防御が整う前に攻められる（Rugby World 2023）
4. ラインブレイク【現場】— 防御ラインを突破すること
5. オーバーラップ（数的優位）【現場】— 攻撃側の人数が防御側を上回っている状態
6. ミスマッチ【現場】— 体格・スピードの差がある組み合わせを作ること（例: FWの選手にBKの選手を当てる）
7. ポッド【現場】— FWを3人前後の小グループに分けて配置し、連続攻撃を担わせる形（出典: sportplan 1-3-3-1、rugbycoachweekly）
8. シェイプ（1-3-3-1など）【現場】— チームとしての攻撃の並び方の型。数字はタッチラインからタッチラインへFWの配置人数を示す（sportplan）
9. ファーストレシーバー／セカンドレシーバー【現場】— 9番からのパスを最初に受ける選手／その次に受ける選手
10. ブラインドサイド／オープンサイド【現場】— ラック・スクラム等を境にした狭い側／広い側（RNZ）

### B. 攻撃のプレーとハンドリング（9）
11. オフロード【現場】— タックルを受けながら、倒れる前にボールをつなぐパス
12. ダミー（ダミーパス／ダミーランナー）【現場】— パスするふり、またはボールをもらうふりで防御を引きつける（RNZ）
13. ループ【現場】— パスした選手が受け手の外側へ回り込んで再びもらうプレー
14. スイッチ（クロス）【現場】— 走る方向を交差させてボールを受け渡すプレー
15. 飛ばしパス（ミスパス）【現場】— 隣の選手を飛ばして外の選手へ通すパス。「ミス」は失敗の意味ではない
16. クラッシュボール【現場】— 突破よりも前進と接点の確保を狙ってまっすぐ当たるプレー
17. ピック・アンド・ゴー【現場】— ラックの後方のボールを拾ってそのまま持ち込むプレー（RNZ）
18. ハンドオフ【規則】— ボールキャリアーが手のひらで相手を払いのける、認められた行為（2026年版定義）
19. ドミナントキャリー【現場】— 接点で前に出て、最初の接触点より先で倒されるキャリー（RWC公式2019）

### C. 防御（9）
20. ドリフト【現場】— 防御ラインが外側へ流れながら対応する守り方（詳細は既存記事）
21. ブリッツ（ラッシュディフェンス）【現場】— 防御ラインが一斉に前へ出て時間とスペースを奪う守り方（詳細は既存記事）
22. ドミナントタックル【現場】— タックラーがボールキャリアーを後ろへ押し戻すタックル（RWC公式2019）
23. ダブルタックル【現場】— 2人で同時に、異なる高さで当たるタックル。頭同士の接触を避ける声かけとタイミングが前提（World Rugby Multi-player tackles）
24. チョークタックル（スタンドアップタックル）【現場】— 相手を立たせたまま止め、倒させない・オフロードさせない狙いのタックル（World Rugby Multi-player tackles「stand-up tackle」）
25. ジャッカラー／スティーラー（ジャッカル）【規則】— タックルに最初に到着したタックラーの味方。立ったまま、関与していた場合は明らかにボールキャリアーを離してからボールを争奪（2026年版定義）
26. ガード（ピラー）【現場】— ラックの両脇に立って、近場への持ち込みを止める防御の選手（RNZ「Guard-dog」）
27. ターンオーバー【現場】— 防御側がボールの保持を奪い返すこと（WR「principles of attack and defence」の regain possession）
28. ロイタリング【規則】— オフサイドの位置に残り続けること。相手のプレーを妨げると罰の対象になりうる（2026年版定義）

### D. ブレイクダウン（7）
29. ブレイクダウン【現場】— ボールキャリアーが地面に倒れた後の攻防局面（World Rugby「Breakdown explained」）。基礎の説明は既存記事へ
30. クリーナー（オーバー）【現場】— 攻撃側のサポートとしてラックに入り、相手を排除してボールを確保する選手
31. カウンターラック【現場】— 防御側がラックで押し返してボールを奪いにいくこと
32. ユーズイット【規則】— ラック・モール・スクラムでボールが獲得されプレー可能になったときのレフリーのコール。ラックでは5秒以内にボールを出さないとスクラム（2026年版 第15条17）
33. ラックのオフサイドライン（最後尾の足）【規則】— 各チームのラック参加者の最後尾の足を通る、トライラインと平行な線（2026年版 第15条4）
34. ノットリリースザボール【規則】— タックルされた選手がボールを離さない反則（日本協会 基本用語解説）
35. ノットロールアウェイ【規則】— タックラーがボールから離れない反則（日本協会 基本用語解説）

### E. セットプレー（7）
36. ラインアウトモール（ドライビングモール）【現場】— ラインアウトで捕球後にモールを組んで前進する攻撃。モールの規則（2026年6月の適用ガイドライン）は既存記事へ
37. レシーバー【規則】— ラインアウトからノックまたはパスバックされたボールを受ける位置の選手（2026年版定義、第18条16）
38. クイックスロー【規則】— ラインアウトが形成される前の投入。投入するのは本来ラインアウトで投入するはずだったチーム（2026年版定義）
39. ダミージャンプ（ダミーリフト）【現場】— 跳ぶふり・持ち上げるふりで相手のジャンパーを惑わせる動き
40. ルースヘッド／タイトヘッド【規則】— スクラム最前列の左右のプロップの呼び分け（語は2026年版 第19条の組み方の条文に登場。「1番=ルースヘッド、3番=タイトヘッド」は背番号の慣例として書き、規則と書かない）
41. ブレーキフット【規則】— フッカーがトンネル中央に片足を前に置く。クラウチとバインドの間ずっと置き、セット後・ボールを当てる前に引く（2026年版定義・2026年7月から正式）
42. セットピース【規則】— スクラムとラインアウトのこと（規則上の定義はスクラム・ラインアウトそれぞれ「セットピース」と記載）。日本の現場では「セットプレー」とも呼ぶ

### F. キックとエリア（8）
43. ボックスキック【現場】— ラックやスクラムの後ろから9番が上げる高いキック。味方が追って競り合う（RNZ）
44. ハイパント（アップ・アンド・アンダー）【現場】— 味方が追いつける高さと滞空時間のキック（RNZ「Gary Owen」）。詳細は既存キック記事
45. グラバーキック【現場】— 地面を転がす低いキック（RNZ）。詳細は既存キック記事
46. キックチェイス【現場】— 蹴った後に味方がラインをそろえて追い、相手の反撃を抑える動き
47. 50:22【規則】— 自陣側から蹴ったボールが相手の22m区域内でタッチに出た場合の規則。バウンドの要否など細かい成立条件は本文で言い切らず、World Rugby Definitions と既存キック記事へ送る
48. マーク【規則】— 自陣22m区域内またはインゴールで相手のキックを直接捕って「マーク」と叫び、フリーキックを得る（2026年版定義）
49. カウンターアタック【現場】— 相手のキックを捕った側が、防御の整う前に攻め返すこと
50. ペナルティの選択（タッチキック／ショット／タップ／スクラム）【規則+現場】— ペナルティを得たチームはスクラムを選べる（第20条3）。タッチに蹴り出した場合は蹴ったチームが投入（第18条）。ゴールを狙う「ショット」、タップキックで速く再開する「クイックタップ」は現場の呼び方

### 出典URL（本文で使ってよいもの）
- 日本ラグビーフットボール協会 競技規則ページ https://www.rugby-japan.jp/future/rule/
- 日本協会 2026年版競技規則（日本語PDF） https://rugby-japan.s3.ap-northeast-1.amazonaws.com/file/html/226214_69b21e13f0fbf.pdf （定義＝PDF 20〜26ページ。ハンドオフ、ジャッカラー/スティーラー、ノックフォワード〈以前のノックオン〉、ロイタリング、マーク、クイックスロー、レシーバー、プレーのフェーズ、ブレーキフット、オープンプレー 等）
- 日本協会 ラグビー基本用語解説 https://www.rugby-japan.jp/guide/rugby/
- World Rugby Laws Definitions https://passport.world.rugby/laws-of-the-game/definitions/
- World Rugby 第15条ラック https://passport.world.rugby/laws-of-the-game/laws-by-number/15-ruck/
- World Rugby 第18条 https://passport.world.rugby/laws-of-the-game/laws-by-number/18-touch-quick-throw-and-lineout/
- World Rugby「The principles of attack and defence」 https://passport.world.rugby/officiating/introduction-to-match-officiating-pre-level-1/the-game/the-principles-of-attack-and-defence/
- World Rugby「Breakdown explained」 https://passport.world.rugby/injury-prevention-and-risk-management/breakdown-ready/breakdown-explained
- World Rugby「Multi-player tackles」 https://passport.world.rugby/injury-prevention-and-risk-management/tackle-ready/tackle-types/multi-player-tackles/
- Rugby World Cup公式「Through or around? The art of getting over the gain line」（2019-09-20） https://www.rugbyworldcup.com/news/460837/1000
- Rugby World「What is the gainline in rugby?」（2023-07-04） https://www.rugbyworld.com/news/what-is-the-gainline-in-rugby-155225
- RNZ「RWC: Beginners guide to rugby jargon」（2023-09-09） https://www.rnz.co.nz/news/sport/497569/live-sport
- Sportplan「The 1-3-3-1 Attacking Shape: Stretching Defences with Pods」 https://www.sportplan.net/drills/Rugby/trends/attacking-shape-1-3-3-1-pods-2025-05.jsp
- Rugby Coach Weekly「Essentials for using attacking pods」 https://rugbycoachweekly.net/tactics/attack-tactics/essentials-for-using-attacking-pods

---

## 4. 骨子（執筆担当Sonnetへの指示）

### frontmatter
```
---
title: ラグビー戦術用語50選｜大学部員向けに攻撃・防御・局面別で解説
description: 大学ラグビー部のミーティングや映像分析で使われる戦術用語50語を、攻撃・防御・ブレイクダウン・セットプレー・キックの局面別に1〜2文で解説。2026年版競技規則に定義がある語と現場用語を区別して示します。
category: 技術
date: （公開日 YYYY-MM-DD）
cta: sponsor
---
```
- タイトル案（31字前後）: 上記。予備案「ラグビー戦術用語集50選｜ゲインライン・ポッド・ピラーまで局面別に解説」
- description は上記で約110字。

### 文量・形式
- 3,000〜5,000字（下限3,000字必須、上限5,000字目安）。です・ます調。本文はH2から。
- 各用語は既存 `rugby-glossary-beginner-guide` と同じ形式の箇条書き: `- **用語（英語表記）**【規則】または【現場】: 説明1〜2文。` 1語あたり50〜80字目安。
- 各H2の冒頭に「この局面の結論1文」を置いてから箇条書きに入る。
- 図は既存SVGのみ使用可（任意）: `![オフサイドラインの位置](diagram:rugby-offside-line)`（Dのラックのオフサイドライン付近）、`![グラウンドのライン](diagram:rugby-pitch-lines)`（Fの50:22付近）。**新しい図は作らない**。

### H2/H3構成と各見出しの結論1文

**導入（H2なし・300字程度）**
- 悩み共感: ミーティングで「ポッド」「ゲインラインを切れ」と言われても意味が分からない場面。
- この記事の使い方: 50語を局面別に整理、各語に【規則】【現場】の印。基礎語（ラック、モール、オフサイド、ノックオン等）は [ラグビー用語集（初心者・新入部員向け）](https://rugbymania.jp/articles/rugby-glossary-beginner-guide/) とサイト内の[ラグビー用語辞典](https://rugbymania.jp/glossary/)で先に確認するよう1文で案内。
- 選定基準を明示（企画K記事ルール）:「編集部が、大学のチーム練習・ミーティングで使われやすい戦術用語を、2026年版競技規則と World Rugby・ラグビーワールドカップ公式の解説で意味を確認できる範囲から選びました」。

**H2 この用語集の見方｜「規則にある言葉」と「現場の言葉」を分ける**
- 結論: 規則に定義がある語は意味が一つに決まり、現場用語はチームによって指す範囲が違うことがある。
- 2026年版競技規則に「定義」章があること、ノックオンは2026年版の定義で「ノックフォワード（以前のノックオン）」と表記されていることを1例として紹介（出典PDF）。
- 小さな表: カテゴリ（A〜F）×語数×主に使う場面。

**H2 攻撃の考え方と陣形の用語（10語）** — 用語1〜10
- 結論: 攻撃の用語は「ゲインラインを越えて、防御が整う前に次の攻撃へつなぐ」という考え方を軸にすると整理しやすい。
- WRの攻撃原則（ボールを保持して前進し、継続する）を1文で引用。

**H2 攻撃のプレーとハンドリングの用語（9語）** — 用語11〜19
- 結論: ハンドリング用語の多くは「防御の目線をずらして、数的優位やミスマッチを作る」ための手段。
- 関連: [スタンドオフの判断力の記事](https://rugbymania.jp/articles/rugby-standoff-decision-making-guide/)、[センターの役割の記事](https://rugbymania.jp/articles/rugby-centre-role-training-guide/)

**H2 防御の用語（9語）** — 用語20〜28
- 結論: 防御の用語は「相手から時間とスペースを奪い、ボールを奪い返す」ための役割と動き方を表す。
- ドリフト/ブリッツは1文ずつにとどめ [ディフェンスラインの記事](https://rugbymania.jp/articles/rugby-defence-line-drift-blitz-guide/) へ送る。
- ダブルタックル・チョークタックルには安全面の一文を必ず添える（WR Multi-player tackles の「頭同士の接触を避ける」）。タックルの高さは [2026年のルール改正の記事](https://rugbymania.jp/articles/rugby-rule-kaisei-2026-guide/) へ。

**H2 ブレイクダウンの用語（7語）** — 用語29〜35
- 結論: ブレイクダウンは規則で決まっている部分（ユーズイットの5秒、最後尾の足のオフサイドライン、ジャッカラーの条件）と、現場の役割名（クリーナー等）が混在するので、まず規則側を押さえる。
- 練習法は [ブレイクダウンとジャッカルの記事](https://rugbymania.jp/articles/rugby-breakdown-jackal-practice-guide/)、[フランカーの記事](https://rugbymania.jp/articles/rugby-flanker-role-breakdown-guide/) へ。

**H2 セットプレーの用語（7語）** — 用語36〜42
- 結論: スクラムとラインアウトは規則上「セットピース」と呼ばれ、ブレーキフットやクイックスローのように規則で動き方が決まった語が多い。
- 関連: [モールの記事](https://rugbymania.jp/articles/rugby-maul-technique-practice-guide/)、[スクラムの記事](https://rugbymania.jp/articles/rugby-scrum-technique-practice-guide/)、[フッカーのスローイングの記事](https://rugbymania.jp/articles/rugby-hooker-lineout-throwing-guide/)、[ロックの記事](https://rugbymania.jp/articles/rugby-lock-lineout-scrum-training-guide/)

**H2 キックとエリアの用語（8語）** — 用語43〜50
- 結論: キックの用語は「陣地を取る」「ボールを取り返す」「速く再開する」のどれを狙うかで分けると覚えやすい。
- 関連: [キックの種類と練習法の記事](https://rugbymania.jp/articles/rugby-kicking-types-practice-guide/)

**H2 用語を覚えたら、自分のリーグの試合で確かめる**
- 結論: 用語は実際の試合と結び付けると定着しやすいので、所属リーグの日程・順位・記録から見返す試合を選ぶ。
- 当サイトのデータは試合結果・得点・順位（記録室は最多合計得点試合・最大得点差試合など）であり、ラインブレイク数などのプレー別の統計は持っていない、と正直に書く。そのうえで「得点差の小さい試合を選び、映像でブレイクダウンやキックの選択を見返す」という使い方を提案（※「〜すると勝てる」等の因果は書かない）。
- 一次データリンク（2本以上必須）:
  - [関東大学対抗戦Aグループの順位表](https://rugbymania.jp/kanto-taiko-a/standings/)
  - [関東大学対抗戦Aグループの記録室](https://rugbymania.jp/kanto-taiko-a/records/)
  - [関東大学リーグ戦1部の順位表](https://rugbymania.jp/kanto-league-1/standings/)
  - [関西大学Aリーグの順位表](https://rugbymania.jp/kansai-a/standings/)
  - [九州学生リーグAの順位表](https://rugbymania.jp/kyushu-a/standings/)
  - （任意）[関東大学対抗戦Aグループの日程・結果](https://rugbymania.jp/kanto-taiko-a/schedule/)

**H2 まとめ**
- 結論: 規則に定義がある語は2026年版競技規則で確認し、現場用語はチーム内で意味をそろえておくと、ミーティングの指示が伝わりやすくなる。
- 学生コーチ向けに1文: [学生コーチの役割の記事](https://rugbymania.jp/articles/rugby-student-coach-role-guide/)

**H2 出典**（3章の出典URLから本文で使ったものを列挙）

### この記事だけの要素（2つ以上）
1. 全50語に【規則】／【現場】の印を付け、規則語は**2026年版競技規則（日本語版）の定義・条文**で裏取りしている（ノックフォワード表記、ジャッカラー/スティーラー、ロイタリング、ユーズイット5秒、ブレーキフット等）。日本語の上位記事にこの区別はない。
2. 基礎語は既存の初心者用語集と用語辞典に任せ、**戦術語だけ**を局面別（攻撃の考え方／ハンドリング／防御／ブレイクダウン／セットプレー／キック）に整理し、各局面から当サイトの技術記事（練習法）へ送るハブ構造。
3. 用語を覚えた後に、所属リーグ（対抗戦・リーグ戦・関西・九州）の順位表・記録室から見返す試合を選ぶ導線。

### 内部リンク候補（実在確認済み）
- 記事（content/articles/ に実在）: rugby-glossary-beginner-guide / rugby-defence-line-drift-blitz-guide / rugby-breakdown-jackal-practice-guide / rugby-flanker-role-breakdown-guide / rugby-maul-technique-practice-guide / rugby-scrum-technique-practice-guide / rugby-hooker-lineout-throwing-guide / rugby-lock-lineout-scrum-training-guide / rugby-kicking-types-practice-guide / rugby-standoff-decision-making-guide / rugby-centre-role-training-guide / rugby-rule-kaisei-2026-guide / rugby-student-coach-role-guide / rugby-tackle-practice-tips / rugby-position-ichiran-yakuwari-guide
- 一次データ（site/ 配下に生成済みを確認）: /glossary/、/kanto-taiko-a/standings/、/kanto-taiko-a/records/、/kanto-taiko-a/schedule/、/kanto-league-1/standings/、/kansai-a/standings/、/kyushu-a/standings/（records は kansai-a・kanto-league-1・kyushu-a 等にも存在）
- リンク形式は既存記事に合わせ `https://rugbymania.jp/...` の絶対URL。

### 禁止事項
- 捏造禁止: 統計値（ラインブレイク数、トライ率、ターンオーバー回数など）を書かない。SERPで見た英国プレミアシップの研究値なども使わない。
- 断定禁止: 「必ず」「絶対」「〜すれば勝てる」を使わない。現場用語は「一般的には」「チームによって呼び方や指す範囲が異なる場合があります」と明示。
- 特定チーム・大学・選手の戦術の評価（「◯◯大はブリッツが得意」等）を書かない。
- 編集部の相談件数・読者像・取材の捏造をしない（rugbymania に一次情報バンクはないため、取材の声は使わない）。
- 基礎語（ラック、モール、オフサイド、ノックオン、スクラム、ラインアウトの基本説明、ポジション名）の定義を繰り返さない。
- 協賛・ツナカレへの言及、tunakare.jp への手書きリンクを入れない（cta帯は自動描画）。
- 本文に H1、斜体、脚注、`![]()`（diagram: 以外の画像）を使わない。新しい diagram を作らない。
- 「ノットリリースザボール」等の反則の罰則（ペナルティかフリーキックか）は、出典で確認できない限り書かない。
- 50:22 の細かい成立条件は定義1文＋キック記事へのリンクにとどめる。

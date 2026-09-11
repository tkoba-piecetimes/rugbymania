"""Rugby portal and searchable archive, generated from existing verified records."""
import json
from html import escape as e


def build(g, leagues, articles, meta):
    records, seasons = [], []
    active = [lg for lg in leagues if not lg["meta"].get("archive_only")]
    for lg in leagues:
        for year, matches in lg['matches_by_year']:
            for m in matches:
                season_source = next((h.get("source_url") for h in lg["hist"] if h["year"] == year), None) or lg["meta"]["source_url"]
                records.append(dict(m, year=year, league=lg['code'], label=lg['label'], region=lg['meta']['region'],
                                    url=f"{lg['code']}/matches/{m['id']}/index.html" if year == lg['meta']['season_year'] and not lg['meta'].get('archive_only') else '',
                                    source=m.get('source_url') or season_source))
        for year, standings in [(lg['meta']['season_year'], lg['standings'])] + [(h['year'],h['standings']) for h in lg['hist']]:
            seasons.append(dict(year=year, league=lg['code'], label=lg['label'], standings=standings, source=next((h.get('source_url') for h in lg['hist'] if h['year']==year),None) or lg['meta']['source_url']))
    data = dict(matches=records, seasons=seasons, leagues=[dict(code=l['code'],label=l['label'],region=l['meta']['region'],year=l['meta']['season_year'],archived=bool(l['meta'].get('archive_only')),teams=l['teams'],updated=l['meta']['fetched_at'][:10]) for l in leagues])
    (g.SITE/'assets'/'rugby-data.json').write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
    years = sorted({m['year'] for m in records},reverse=True)
    count = len({t for l in active for t in l['teams'] if 'の勝者' not in t and 'の敗者' not in t})
    body = f'''<div class="edition">COLLEGE RUGBY / {max(years)} <span>関東・関西・九州 / 収録 {len(active)}カテゴリ</span></div>
<section class="rugby-hero"><img src="assets/hero.jpg" alt="大学ラグビーのフィールド" width="1440" height="810"><div class="hero-copy"><p>JAPAN COLLEGE RUGBY JOURNAL</p><h1>その一戦が、<br>僕らをつなぐ。</h1><p>仲間の勝利も、ライバルの次戦も。<br>大学ラグビーに夢中な、すべての人へ。</p><a class="primary" href="#match-center">試合をチェック ↗</a></div><div class="hero-count"><b>{count}</b> TEAMS <span>{len(active)} CATEGORIES</span></div></section>
<section id="match-center" class="rugby-section"><p class="eyebrow">01 / MATCH CENTER</p><h2>試合の熱を、追いかけよう。</h2><p>収録データ更新：{e(meta['fetched_at'][:10])}。ライブ速報ではありません。大会ごとの更新日はリーグ一覧に記載。</p>{controls(active, years, False)}<div id="match-results" aria-live="polite"><p>検索データを読み込み中です。リーグ別の日程・順位表もご利用いただけます。</p></div><noscript><p>絞り込みにはJavaScriptが必要です。リーグ別ページから記録をご覧ください。</p></noscript><p><a href="archive/index.html">過去の試合・順位表を調べる →</a></p></section>
<section class="rugby-section" id="leagues"><p class="eyebrow">02 / THE LEAGUES</p><h2>あなたのリーグは、ここに。</h2><p>掲載対象：関東対抗戦A・B／リーグ戦1・2部、関西A・B、九州A〜D。その他の大会は未収録です。</p><div class="league-grid">'''
    for lg in active:
        body += f'''<article class="league-tile"><span>{e(lg['meta']['region'])} / {len(lg['teams'])} TEAMS</span><h3><a href="{lg['code']}/index.html">{e(lg['label'])} ↗</a></h3><div><a href="{lg['code']}/schedule/index.html">日程・結果</a><a href="{lg['code']}/standings/index.html">順位表</a><a href="{lg['code']}/teams/index.html">チーム</a></div><small>更新 {e(lg['meta']['fetched_at'][:10])} / {lg['meta']['season_year']}年 {len(lg['matches'])}試合収録</small></article>'''
    body += '''</div></section><section id="my-team" class="rugby-section"><p class="eyebrow">03 / MY TEAM</p><h2>いつものチームを、いちばん近くに。</h2><p>選んだチームをこのブラウザーに保存。次の訪問でもすぐ確認できます。</p><label>応援するチーム <select id="favorite-team"><option value="">チームを選ぶ</option></select></label><div id="favorite-result" aria-live="polite"></div></section>'''
    if articles:
        body += '<section class="rugby-section"><p class="eyebrow">04 / JOURNAL</p><h2>ラグビーを、もっと深く。</h2><div class="digest">' + ''.join(g.article_card(a,'') for a in articles[:3]) + '</div><a href="articles/index.html">読みもの一覧 →</a></section>'
    body += f'''<section id="support" class="rugby-section rugby-support"><p class="eyebrow">BEYOND THE SCORE / PR</p><h2>その熱量を、部活の未来につなげよう。</h2><p>遠征も、練習も、次の挑戦も。学生団体と企業をつなぐツナカレで、協賛について相談できます。</p><a class="primary" href="{g.LISTING_LP_URL}" target="_blank" rel="noopener">部活の協賛を相談する ↗</a></section>'''
    g.write_page('',g.page('', 'ラグビーマニア | 大学ラグビーの試合結果・順位・データ', body,meta))
    body = f'''<section class="rugby-section"><p class="eyebrow">RUGBY DATABASE / {min(years)}–{max(years)}</p><h1>あの一戦から、次の一戦へ。</h1><p>年度・リーグ・大学から記録を検索。順位表もこのページ内で確認できます。</p><p>収録範囲はリーグ・年度により異なります。未収録の試合を含む通算成績ではありません。順位・勝ち点はスコアのある試合だけの参考集計です。複数ステージは合算しており、公式最終順位ではありません。2021年の九州は当時のⅠ部・Ⅱ部で収録しています。不戦・中止等は別表示し、通常スコアの集計に含めません。</p>{controls(leagues, years, True)}<div id="match-results" aria-live="polite"><p>検索データを読み込み中です。リーグ別の日程・順位表もご利用いただけます。</p></div><noscript><p>絞り込みにはJavaScriptが必要です。リーグ別ページから記録をご覧ください。</p></noscript></section>'''
    coverage_rows = ''
    for lg in leagues:
        for year, matches in lg['matches_by_year']:
            src = next((h.get('source_url') for h in lg['hist'] if h['year']==year),None) or lg['meta']['source_url']
            coverage_rows += f'<tr><td>{year}</td><td>{e(lg["label"])}</td><td>{len(matches)}</td><td>{sum(m["status"]=="played" for m in matches)}</td><td><a href="{e(src)}" target="_blank" rel="noopener">公式資料 ↗</a></td></tr>'
    body += '<details class="rugby-section"><summary>年度・リーグ別の収録件数と出典</summary><p>対戦チームが確定した掲載試合が対象です。未確定の対戦枠や別ページの入替戦は含みません。</p><div class="archive-table"><table><thead><tr><th>年度</th><th>リーグ</th><th>収録試合</th><th>スコアあり</th><th>出典</th></tr></thead><tbody>' + coverage_rows + '</tbody></table></div></details>'
    g.write_page('archive',g.page('../','大学ラグビー データベース | ラグビーマニア',body,meta,path='archive/'))


def controls(leagues, years, archive):
    year_options = ('<option value="all">すべての年度</option>' if archive else '') + ''.join(f'<option value="{y}">{y}年</option>' for y in years)
    league_options = ''.join(f'<option value="{l["code"]}">{e(l["label"])}</option>' for l in leagues)
    views = '<option value="played">試合結果</option><option value="standings">参考成績表</option><option value="unscored">不戦・中止等</option><option value="all">日程・結果すべて</option>' if archive else '<option value="scheduled">今後の日程</option><option value="played">試合結果</option><option value="unscored">不戦・中止等</option>'
    return f'''<form class="rugby-filters" onsubmit="return false"><label>年度<select id="year">{year_options}</select></label><label>リーグ<select id="league"><option value="">すべてのリーグ</option>{league_options}</select></label><label>大学<select id="team"><option value="">すべての大学</option></select></label><label>対戦相手<select id="opponent"><option value="">指定なし</option></select></label><label>表示<select id="view">{views}</select></label><button type="button" id="reset-filters">条件をリセット</button></form>'''

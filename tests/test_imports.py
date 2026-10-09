import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'pipeline'))
from fetch_kyushu import parse_matches
from legacy_kansai import parse as parse_legacy
from grid_kansai import parse as parse_grid
from table_kansai import parse_all as parse_renewal
from fetch_rugby import parse_matches as parse_kanto

def fixture(name):return (ROOT/'tests'/'fixtures'/name).read_text(encoding='utf8')

class Imports(unittest.TestCase):
    def test_article_generation_excludes_archive_only_categories(self):
        import tempfile
        from unittest.mock import patch
        import generate_articles
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'kyushu-1'/'history').mkdir(parents=True)
            (root/'kyushu-a').mkdir()
            (root/'kyushu-a'/'meta.json').write_text('{}')
            with patch.object(generate_articles,'DATA_DIR',root):
                self.assertEqual(generate_articles.current_league_codes(),['kyushu-a'])

    def test_kyushu_combined_date_and_rowspan(self):
        ms=parse_matches(fixture('kyushu-2026-A.html'),'九州学生リーグA',2026)
        self.assertEqual(len(ms),15)
        first=[m for m in ms if m['date']=='2026-09-19']
        self.assertEqual(len(first),3)
        self.assertTrue(all(m['status']=='scheduled' and m['home_score'] is None for m in ms))
        self.assertEqual(next(m for m in ms if m['home']=='日本文理大学')['away'],'福岡工業大学')

    def test_ambiguous_date_and_forfeit(self):
        ms=parse_matches(fixture('kyushu-2026-C.html'),'九州学生リーグC',2026)
        self.assertEqual(len(ms),15)
        self.assertEqual(sum(m['date'] is None for m in ms),2)
        self.assertEqual(next(m for m in ms if m['home']=='九州産業大学' and m['away']=='佐賀大学')['date'],'2026-10-17')
        uncertain=next(m for m in ms if m['home']=='九州産業大学' and m['away']=='志學館大学')
        self.assertIsNone(uncertain['date'])
        self.assertIn('11月14日or15日',''.join(uncertain['note'].split()))
        forfeits=[m for m in ms if m['status']=='unscored']
        self.assertEqual(len(forfeits),4)
        self.assertTrue(all(m['home_score'] is None and m['away_score'] is None for m in forfeits))

    def test_kansai_renewal_table_rows(self):
        g=parse_renewal(fixture('kansai-2026-renewal.html'),'https://rugby-kansai.or.jp/gameuniversity')
        self.assertEqual(sorted(g),['a','c','junior','promotion'])  # 呼び出し側(fetch_kansai)がa/bのみ採用
        a=g['a']
        self.assertEqual(len(a),2)
        played=[m for m in a if m['status']=='played']
        self.assertEqual(len(played),1)
        self.assertEqual((played[0]['home'],played[0]['away'],played[0]['home_score'],played[0]['away_score']),('立命館大学','京都産業大学',24,45))
        self.assertEqual((played[0]['date'],played[0]['time'],played[0]['venue']),('2026-09-13','16:00','花園Ⅰ'))
        self.assertEqual(len({m['id'] for m in a}),2)
        self.assertEqual([m for m in a if m['status']=='scheduled'][0]['home_score'],None)
        forfeit=g['c'][0]
        self.assertEqual(forfeit['status'],'unscored')
        self.assertIsNone(forfeit['home_score'])

    def test_kansai_renewal_season_requires_a_and_b(self):
        import fetch_kansai
        with self.assertRaises(ValueError):
            fetch_kansai.parse_season(fixture('kansai-2026-renewal.html'),2026)

    def test_kansai_merged_date_columns(self):
        ms=parse_legacy(fixture('kansai-2022-A.html'),'関西大学Aリーグ',2022,'https://rugby-kansai.or.jp/gameuniversity2022')
        self.assertEqual(len(ms),28)
        m=ms[0]
        self.assertEqual((m['date'],m['home'],m['home_score'],m['away_score']),('2022-09-18','同志社大学',15,19))

    def test_kansai_second_stage_and_name_annotations(self):
        ms=parse_grid(fixture('kansai-2025-B.html'),'関西大学Bリーグ',2025,'https://rugby-kansai.or.jp/gameuniversity2025')
        self.assertEqual(len(ms),42)
        self.assertTrue(all('位' not in m['home']+m['away'] for m in ms))
        m=next(m for m in ms if m['date']=='2025-11-23' and m['home']=='大阪体育大学')
        self.assertEqual((m['away'],m['home_score'],m['away_score']),('追手門学院大学',69,7))

    def test_roster_link_is_still_a_scheduled_game(self):
        html='<h3 class="middle">9月12日（土）</h3><ul class="gameSche"><li><div class="kotime">15:00</div><div class="team">日本体育大</div><div class="result"><div class="score"><a href="/files/member_pdf/2026/26000.pdf">&nbsp;</a></div><div class="memo">メンバー表</div></div><div class="team">早稲田大</div><div class="stadium">駒沢</div></li></ul>'
        ms=parse_kanto(html,'対抗戦A',2026)
        self.assertEqual(len(ms),1)
        self.assertEqual(ms[0]['status'],'scheduled')
        self.assertIsNone(ms[0]['home_score'])

    def test_unscored_forfeit_is_not_dropped(self):
        html='<h3 class="middle">11月28日（日）</h3><ul class="gameSche"><li><div class="kotime"></div><div class="team">國學院大</div><div class="result"><span class="noscore">不戦勝 - 不戦敗<br>○-●</span></div><div class="team">拓殖大</div><div class="stadium"></div></li></ul>'
        ms=parse_kanto(html,'リーグ戦2部',2021)
        self.assertEqual(len(ms),1)
        self.assertEqual(ms[0]['status'],'unscored')
        self.assertIsNone(ms[0]['away_score'])

if __name__=='__main__':unittest.main()

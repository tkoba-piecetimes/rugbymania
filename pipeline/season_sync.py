"""Persist validated seasons; never erase a successful import after fetch failure."""
import json
from datetime import datetime, timezone
from pathlib import Path

DATA=Path(__file__).resolve().parent.parent/'data'/'leagues'

def sync(fetch_season, years, current, region, source):
    failures=[]
    for year in years:
        try:
            result=fetch_season(year)
            if not result:raise ValueError('No season records parsed')
            for code,d in result.items():
                matches=d['matches']
                ids=[m['id'] for m in matches]
                if not matches or len(ids)!=len(set(ids)):raise ValueError(f'{code}: empty or duplicate matches')
                stamp=datetime.now(timezone.utc).isoformat(timespec='seconds')
                target=DATA/code;target.mkdir(parents=True,exist_ok=True)
                common={'source_url':d['source_url'],'fetched_at':stamp,'import_version':2,
                        'coverage_note':d.get('coverage_note','公式日程ページの掲載試合。入替戦は対象外。'),
                        'standings_kind':'reference'}
                if year==current:
                    meta=dict(common,code=code,region=region,gender='男子',group='対抗戦' if 'taiko' in code else 'リーグ戦',league=d['label'],season_year=year,source=source,source_updated_at=d.get('source_updated_at',stamp[:10]))
                    for name,value in [('matches',matches),('standings',d['standings']),('teams',d['teams']),('meta',meta)]:
                        (target/f'{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=1),encoding='utf8')
                else:
                    (target/'history').mkdir(exist_ok=True)
                    value=dict(common,year=year,league=d['label'],matches=matches,standings=d['standings'])
                    (target/'history'/f'{year}.json').write_text(json.dumps(value,ensure_ascii=False,indent=1),encoding='utf8')
                print(f"{year}/{code}: {len(matches)} matches / {sum(m['status']=='played' for m in matches)} scored")
        except Exception as exc:
            failures.append(f'{year}: {exc}')
    if failures:raise RuntimeError('; '.join(failures))

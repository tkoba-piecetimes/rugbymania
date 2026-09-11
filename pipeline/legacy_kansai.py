"""2021–2023 official university tables (including merged date cells)."""
import re
from urllib.parse import urljoin
from html_tables import tables,text,clean_team,score
from common import match_date_iso
from team_slugs import slug_for

def parse(html,label,year,source):
    first=next(tables(html),[])
    if not first:return []
    headers=[text(c) for c in first[0][0]]
    ko=next((i for i,h in enumerate(headers) if h in ('K.O.','キックオフ','時間')),None)
    if ko is None:return []
    home=ko+2 if 'グループ' in headers else ko+1
    matches=[]
    for row,is_header in first[1:]:
        if is_header or len(row)<=home+2:continue
        a,b=clean_team(row[home]),clean_team(row[home+2])
        if not a or not b or '大学' not in a or '大学' not in b:continue
        dates=''.join(text(c) for c in row[1:ko])
        dm=re.search(r'(\d{1,2})月\s*(\d{1,2})日',dates)
        if not dm:continue
        date=match_date_iso(int(dm[1]),int(dm[2]),year)
        hs,away,status,note=score(row[home+1])
        detail=re.search(r'href=[\"\']([^\"\']+)',row[home+1])
        stage=text(row[0]);group=text(row[ko+1]) if home==ko+2 else ''
        matches.append(dict(id=f'{date}-{slug_for(a)}-vs-{slug_for(b)}',date=date,time=text(row[ko]) or '未定',
            category=label,home=a,away=b,home_slug=slug_for(a),away_slug=slug_for(b),
            home_score=hs,away_score=away,status=status,venue=text(row[home+3]) if len(row)>home+3 else '未定',
            note=note,stage=stage,group=group,source_url=urljoin(source,detail[1]) if detail else source))
    return matches

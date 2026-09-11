"""Check every generated link plus archive integrity before Pages deployment."""
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote

ROOT=Path(__file__).resolve().parents[1]/'site'
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):self.links.extend(v for k,v in attrs if k in ('href','src') and v)

def main():
    count=0;broken=[]
    for f in ROOT.rglob('*.html'):
        p=Links();p.feed(f.read_text(encoding='utf8'))
        for u in p.links:
            parsed=urlsplit(u)
            if parsed.scheme or parsed.netloc or not parsed.path:continue
            dest=(ROOT/parsed.path.lstrip('/') if parsed.path.startswith('/') else f.parent/unquote(parsed.path)).resolve()
            if dest.is_dir():dest=dest/'index.html'
            count+=1
            if not dest.exists():broken.append((str(f.relative_to(ROOT)),u))
    d=json.loads((ROOT/'assets/rugby-data.json').read_text(encoding='utf8'))
    ids=set()
    for m in d['matches']:
        key=(m['league'],m['year'],m['id'])
        assert key not in ids,('duplicate',key)
        ids.add(key)
        assert m['source'].startswith('https://'),('source',key)
        if m['date'] is None:assert '日程' in m['note'],('unexplained missing date',key)
        if m['url']:assert (ROOT/m['url']).exists(),('missing detail',key)
        if m['status']=='played':assert isinstance(m['home_score'],int) and isinstance(m['away_score'],int)
        else:assert m['home_score'] is None and m['away_score'] is None
        assert not m['home_slug'].startswith('team-') and not m['away_slug'].startswith('team-'),('unstable slug',key)
    assert set(range(2021,2027)) <= {m['year'] for m in d['matches']}
    assert not broken,broken[:20]
    print(f'Validated {len(list(ROOT.rglob("*.html")))} pages, {count} links, {len(ids)} records; zero broken links.')

if __name__=='__main__':main()

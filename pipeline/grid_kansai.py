"""Parse 7/8-column CSS grids, including line breaks and second-stage games."""
import re
from html.parser import HTMLParser
from urllib.parse import urljoin
from html_tables import text,clean_team,score
from common import match_date_iso
from team_slugs import slug_for

class Grids(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False);self.depth=0;self.grids=[];self.items=[];self.raw=[];self.width=0;self.attrs={}
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='div' and not self.depth and re.fullmatch(r'sche_cont[78]',attrs.get('class','')):
            self.depth=1;self.width=int(attrs['class'][-1]);self.items=[];return
        if not self.depth:return
        if tag=='div':
            if self.depth==1:self.raw=[];self.attrs=attrs
            else:self.raw.append(self.get_starttag_text())
            self.depth+=1
        elif self.depth>=2:self.raw.append(self.get_starttag_text())
    def handle_endtag(self,tag):
        if not self.depth:return
        if tag=='div':
            self.depth-=1
            if self.depth==1:self.items.append((self.attrs,''.join(self.raw)))
            elif self.depth==0:self.grids.append((self.width,self.items))
            else:self.raw.append('</div>')
        elif self.depth>=2:self.raw.append(f'</{tag}>')
    def handle_data(self,data):
        if self.depth>=2:self.raw.append(data)
    def handle_entityref(self,name):
        if self.depth>=2:self.raw.append('&'+name+';')
    def handle_charref(self,name):
        if self.depth>=2:self.raw.append('&#'+name+';')

def parse(html,label,year,source):
    parser=Grids();parser.feed(html);matches=[]
    for width,items in parser.grids:
        row=[];stage='リーグ戦'
        for attrs,raw in items:
            if 'grid-column' in attrs.get('style',''):
                stage=text(raw);continue
            row.append(raw)
            if len(row)<width:continue
            a,b=clean_team(row[3]),clean_team(row[5]);dm=re.search(r'(\d{1,2})月(\d{1,2})日',text(row[1]))
            if dm and '大学' in a and '大学' in b and not any(t in a+b for t in ['位','の勝者','の敗者']):
                d=match_date_iso(int(dm[1]),int(dm[2]),year);hs,away,status,note=score(row[4])
                detail=re.search(r'href=[\"\']([^\"\']+)',row[4])
                matches.append(dict(id=f'{d}-{slug_for(a)}-vs-{slug_for(b)}',date=d,time=text(row[2]) or '未定',
                    category=label,home=a,away=b,home_slug=slug_for(a),away_slug=slug_for(b),home_score=hs,away_score=away,
                    status=status,note=note,stage=stage,venue=text(row[6]) or '未定',source_url=urljoin(source,detail[1]) if detail else source))
            row=[]
        if row:raise ValueError('Incomplete official schedule grid')
    return sorted(matches,key=lambda m:(m['date'] or '9999',m['time']))

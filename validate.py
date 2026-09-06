import json
from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
from PIL import Image
from urllib.parse import urlparse,parse_qs,unquote
root=Path(__file__).resolve().parent
places=json.loads((root/'places.json').read_text())
N=len(places)
assert len({p['name'] for p in places})==N
cats=Counter(p['category'] for p in places)
assert len(cats)==6
for cat,n in cats.items():
 assert 10<=n<=15,(cat,n)
 assert sum(p['local'] for p in places if p['category']==cat)>=n/2
 assert any(not p['local'] for p in places if p['category']==cat)
total_images=0
for p in places:
 assert all(p.get(k) for k in ['name','description','address','source'])
 assert len(p['description'].split())>=20,(p['name'],'description too short')
 assert p['source'].startswith('http')
 assert len(p['images'])==3,(p['name'],'expected exactly 3 images, got',len(p['images']))
 assert len({im['src'] for im in p['images']})==3,(p['name'],'duplicate image path')
 for im in p['images']:
  assert all(im.get(k) for k in ['src','source','attribution'])
  assert im['src'].startswith('imágenes/')
  with Image.open(root/im['src']) as pic:pic.verify()
 total_images+=len(p['images'])
 assert 52.14<=p.get('lat',0)<=52.26,(p['name'],'lat out of range')
 assert 0.05<=p.get('lng',0)<=0.21,(p['name'],'lng out of range')
class Check(HTMLParser):
 def __init__(self):super().__init__();self.images=[];self.maps=[];self.ids=set();self.anchors=[];self.cards=[];self.dots=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:assert d['id'] not in self.ids;self.ids.add(d['id'])
  if tag=='img':self.images.append(d);assert d.get('alt')
  if tag=='article' and 'card' in d.get('class',''):self.cards.append(d)
  if tag=='span' and d.get('class','').startswith('dot'):self.dots.append(d)
  if tag=='a':
   href=d.get('href','')
   if href.startswith('#'):self.anchors.append(href[1:])
   if 'google.com/maps/dir/' in href:self.maps.append(href)
check=Check();check.feed((root/'index.html').read_text())
assert len(check.images)==total_images,(len(check.images),total_images)
assert len(check.maps)==N
assert len(check.cards)==N
assert len(check.dots)==total_images,(len(check.dots),total_images)
for c in check.cards:
 assert c.get('data-lat') and c.get('data-lng'),c
for img in check.images:assert (root/unquote(img['src'])).is_file()
for target in check.anchors:assert target in check.ids,target
for url in check.maps:
 q=parse_qs(urlparse(url).query)
 assert q['api']==['1'] and q['travelmode']==['walking'] and q['destination'][0]
print(f'Verified: {N} distinct places, 10-15 per category, >=50% local in each, {N} valid photos, {N} walking directions, all internal links.')
print(dict(cats))

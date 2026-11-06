#!/usr/bin/env python3
"""SuomiFlow: Ryhti open_permit_building -> GeoJSON. Requires requests, pyproj, shapely.
No guessed locations, no invented contacts. Run from your computer / GitHub Actions.
"""
import argparse, json, time, sys
from datetime import datetime, timezone
from urllib.parse import urljoin
import requests
from shapely.geometry import shape
from shapely.ops import transform
from pyproj import Transformer

BASE='https://paikkatiedot.ymparisto.fi/geoserver/ryhti_permit/ogc/features/v1'
COLLECTION='open_permit_building'

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--limit',type=int,default=1000,help='Records per page')
 ap.add_argument('--max-pages',type=int,default=30)
 ap.add_argument('--output',default='suomiflow_rakennushankkeet.json')
 args=ap.parse_args()
 s=requests.Session();s.headers.update({'Accept':'application/geo+json, application/json','User-Agent':'SuomiFlow-POC/0.1 (non-commercial evaluation)'})
 url=f'{BASE}/collections/{COLLECTION}/items?limit={min(3000,max(1,args.limit))}'
 features=[];seen=set(); transformer=Transformer.from_crs('EPSG:3067','EPSG:4326',always_xy=True)
 for page in range(args.max_pages):
  for attempt in range(4):
   try:
    r=s.get(url,timeout=70);r.raise_for_status();data=r.json();break
   except (requests.RequestException,ValueError) as e:
    if attempt==3: raise RuntimeError(f'Page {page+1} failed: {e}') from e
    time.sleep(2**attempt)
  for f in data.get('features',[]):
   if not f.get('geometry'):continue
   p=f.get('properties') or {}
   ident=str(f.get('id') or p.get('id') or '')
   if not ident or ident in seen:continue
   try:
    geom=shape(f['geometry'])
    if geom.is_empty:continue
    # OGC API GeoJSON is usually WGS84; inspect response CRS and geometry bounds.
    crs=(data.get('crs') or {}).get('properties',{}).get('name','') if isinstance(data.get('crs'),dict) else str(data.get('crs') or '')
    x,y=geom.representative_point().coords[0]
    if '3067' in crs or (abs(x)>180 or abs(y)>90): x,y=transformer.transform(x,y)
    if not (19<=x<=33 and 59<=y<=71):continue
   except Exception:continue
   seen.add(ident)
   source=f'{BASE}/collections/{COLLECTION}/items/{ident}'
   # Do not interpret unknown status or assign a contractor without evidence.
   features.append({'type':'Feature','geometry':{'type':'Point','coordinates':[round(x,6),round(y,6)]},'properties':{
    'id':'ryhti:'+ident,'name':'Lupavaiheen rakennus '+ident,'city':'','stage':'Lupavaihe','quality':'Selvitettävä',
    'description':'Ryhdin avoin rakennustieto. Tarkka käyttötarkoitus ja hankkeen eteneminen tarkistettava lähteestä.',
    'fit':'Kiinnikepajalle soveltuvuutta ei ole vielä arvioitu.','company':'Ei selvitetty','contact':'','email':'','phone':'',
    'source':source,'sourceSystem':'Ryhti / SYKE','locationAccuracy':'Ryhti-geometriasta johdettu piste',
    'sourceProperties':p}})
  nexts=[x.get('href') for x in data.get('links',[]) if x.get('rel')=='next' and x.get('href')]
  print(f'Page {page+1}: {len(data.get("features",[]))} records; accepted {len(features)}',file=sys.stderr)
  if not nexts:break
  url=urljoin(url,nexts[0]);time.sleep(.4)
 else:print('WARNING: max-pages reached; this is a partial dataset',file=sys.stderr)
 out={'type':'FeatureCollection','metadata':{'source':'Ryhti / SYKE open_permit_building','retrievedUTC':datetime.now(timezone.utc).isoformat(),'count':len(features),'notes':'Rakennustietoja, ei vahvistettuja myyntiliidejä. Ei automaattisesti koko Suomen kattava.'},'features':features}
 with open(args.output,'w',encoding='utf-8') as h:json.dump(out,h,ensure_ascii=False,separators=(',',':'))
 print(f'Wrote {len(features)} to {args.output}')
if __name__=='__main__':main()

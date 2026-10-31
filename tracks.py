import json,math,re
from pathlib import Path
all=[json.load(open(p)) for p in Path('data-source').glob('*.geojson')]
ids={'monza':'it-1922','monaco':'mc-1929','suzuka':'jp-1962','silverstone':'gb-1948','spa':'be-1925'}
tracks={}
for name,id in ids.items():
 f=next(f for f in all if f['properties']['id']==id)
 coords=f['geometry']['coordinates'];lat=sum(p[1] for p in coords)/len(coords)
 points=[(p[0]*math.cos(math.radians(lat)),-p[1]) for p in coords]
 tracks[name]=points

def norm(points):
 xs,ys=zip(*points)
 if max(ys)-min(ys)>1.2*(max(xs)-min(xs)):points=[(-y,x) for x,y in points]
 xs,ys=zip(*points);w=max(xs)-min(xs);h=max(ys)-min(ys);scale=min(430/w,210/h)
 return [[round(250+(x-(max(xs)+min(xs))/2)*scale,2),round(130+(y-(max(ys)+min(ys))/2)*scale,2)] for x,y in points]
paths={}
for name,points in tracks.items():
 p=norm(points);paths[name]={"path":"M"+" L".join(",".join(map(str,v)) for v in p)+" Z","points":p,"source":"https://github.com/bacinger/f1-circuits","layout":"Grand Prix"}
from fontTools.svgLib.path import parse_path
from fontTools.pens.recordingPen import RecordingPen
import xml.etree.ElementTree as E
r=E.parse('data-source/yeongam.svg').getroot();el=next(p for p in r.iter() if p.attrib.get('id')=='path2384');pen=RecordingPen();parse_path(el.attrib['d'],pen);pts=[];last=None
for cmd,args in pen.value:
 if cmd=='moveTo':last=args[0];pts.append(last)
 elif cmd=='lineTo':last=args[0];pts.append(last)
 elif cmd=='curveTo':
  a=last;b,c,d=args
  for j in range(1,17):
   t=j/16;u=1-t;pts.append(tuple(u**3*a[k]+3*u*u*t*b[k]+3*u*t*t*c[k]+t**3*d[k] for k in [0,1]))
  last=d
p=norm(pts);paths['yeongam']={'path':'M'+' L'.join(','.join(map(str,v)) for v in p)+' Z','points':p,'source':'https://commons.wikimedia.org/wiki/File:Korea_international_circuit_v2.svg','layout':'2010 Grand Prix'}
from pathlib import Path
Path('src/data/track-layouts.js').write_text('// Real GP layout data, normalized uniformly; see track-credits.html.\nexport const trackLayouts='+json.dumps(paths,separators=(',',':'))+';\n')


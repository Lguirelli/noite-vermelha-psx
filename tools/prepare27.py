from pathlib import Path
import json,shutil
from PIL import Image
R=Path('outputs/A-Noite-Vermelha-HTML-27');R.mkdir(exist_ok=True);old=R.with_name('A-Noite-Vermelha-HTML-26')
for f in ['JOGAR.html','ESTRUTURAS.json','REGRAS-DE-CRIACAO-E-CORRECAO.md']:shutil.copy2(old/f,R/f)
(R/'assets/rigged').mkdir(parents=True,exist_ok=True);(R/'tools').mkdir(exist_ok=True)
for f in ['mapa-completo.glb','mapa-navegacao.json','atlas-historia-22.png','noite-pixel.ttf']:shutil.copy2(old/'assets'/f,R/'assets'/f)
shutil.copytree(old/'assets/fonts',R/'assets/fonts',dirs_exist_ok=True)
r=json.load(open('work/source27.json'));detail=json.load(open('work/detail27.json'));used=set(n[1] for ob in detail.values() if isinstance(ob,dict) and 'mats' in ob for m in ob['mats'] for n in m['nodes'] if n[0]=='TEX_IMAGE');ims=sorted([im for im in r['images'] if im['name'] in used],key=lambda i:(-i['size'][1],-i['size'][0]));atlas=Image.new('RGB',(4096,4096));shelves=[];rects={}
for im in ims:
 w,h=im['size']
 shelf=next((s for s in shelves if s[2]>=h+4 and s[0]+w+4<=4096),None)
 if shelf is None:
  shelf=[0,sum(s[2] for s in shelves),h+4];shelves.append(shelf)
 x,y,rowh=shelf
 assert y+h+4<=4096
 a=Image.open(im['path']).convert('RGB');atlas.paste(a,(x+2,y+2));rects[im['name']]=[x+2,y+2,w,h];shelf[0]+=w+4
atlas.save(R/'assets/hero-atlas27.png');(R/'assets/atlas-layout27.json').write_text(json.dumps(rects,indent=2));print('Prepared source textures:',len(rects))


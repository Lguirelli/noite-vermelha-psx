from pathlib import Path
import re,base64,json,gzip,hashlib,shutil,struct
R=Path('outputs/A-Noite-Vermelha-HTML-27');p=R/'JOGAR.html';s=Path('outputs/A-Noite-Vermelha-HTML-26/JOGAR.html').read_text(encoding='utf8');old=s
blob=(R/'assets/heroes-runtime27.json.gz').read_bytes()
s,n=re.subn(r"const heroRaw=Uint8Array.from\(atob\('[^']*'\),c=>c.charCodeAt\(0\)\);",lambda m:"const heroRaw=Uint8Array.from(atob('"+base64.b64encode(blob).decode()+"'),c=>c.charCodeAt(0));",s);assert n==1
s,n=re.subn(r"heroImage.src='data:image/png;base64,[^']*'",lambda m:"heroImage.src='data:image/png;base64,"+base64.b64encode((R/'assets/hero-atlas27.png').read_bytes()).decode()+"'",s);assert n==1
s=s.replace('EDIÇÃO 26','EDIÇÃO 27').replace('EVOLUÇÃO 26','EVOLUÇÃO 27').replace('· E26 · Bases originais integradas','· E27 · Personagens enviados e animações Quaternius')
s=s.replace('Quatro protagonistas · bases enviadas integradas','Personagens do Blender · animações Quaternius')
a='vec2 cell=floor(clamp(tex,0.,.999)*4.)/4.;float density=2.;sampleUV=cell+vec2(.004)+fract(planar/density)*.242;'
b='''vec2 tile=floor(clamp(tex,0.,.999)*4.);vec2 cell=tile/4.;float id=tile.x+tile.y*4.;vec2 meters=vec2(1.2);if(id<.5)meters=vec2(1.2,2.4);else if(id<1.5)meters=vec2(3.);else if(id<2.5)meters=vec2(1.6);else if(id<3.5)meters=vec2(1.0);else if(id>11.5&&id<12.5)meters=vec2(1.2,.8);else if(id>12.5&&id<13.5)meters=vec2(1.5);bool unique=(id>3.5&&id<5.5)||(id>6.5&&id<8.5)||(id>13.5);sampleUV=unique?clamp(tex,cell+vec2(.004),cell+vec2(.246)):cell+vec2(.004)+fract(planar/meters)*.242;'''
assert a in s;s=s.replace(a,b);p.write_text(s,encoding='utf8')
getmap=lambda a:base64.b64decode(re.search(r'<script id="asset"[^>]*>(.*?)</script>',a,re.S)[1]);assert getmap(old)==getmap(s)
for f in ['index.html','ABRIR-JOGO.html','CAMPANHA.html']:(R/f).write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=JOGAR.html"><a href="JOGAR.html">Abrir A Noite Vermelha — Evolução 27</a>',encoding='utf8')
lib=Path('work/animations27/Universal Animation Library[Standard]');(R/'assets/animations').mkdir(exist_ok=True);shutil.copy2(lib/'Unreal-Godot/UAL1_Standard.glb',R/'assets/animations/Quaternius-UAL1-Standard.glb');shutil.copy2(lib/'License.txt',R/'assets/animations/LICENSE.txt')
shutil.copy2('work/prepare27.py',R/'tools/prepare27.py')
manifest={'edition':27,'sourceBlend':'Personagens_PSX_UV_Separadas.blend','mapSHA256':hashlib.sha256(getmap(s)).hexdigest(),'runtimeSHA256':hashlib.sha256(blob).hexdigest(),'animationLibrary':'Quaternius Universal Animation Library Standard, CC0','clips':['Idle_Loop','Walk_Loop'],'browserVisualCheck':'not performed','geometryPreview':'rendered from exact game frames'}
(R/'MANIFESTO-27.json').write_text(json.dumps(manifest,indent=2));scripts=re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>',s,re.S);(R/'tools/runtime-check.js').write_text(next(x for x in scripts if 'heroRaw' in x),encoding='utf8');print('Integrated new models, textures, clips; map unchanged')

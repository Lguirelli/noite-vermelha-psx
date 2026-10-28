from pathlib import Path
import json,gzip,base64,struct,re,hashlib,math
R=Path(__file__).resolve().parents[1];s=(R/'JOGAR.html').read_text(encoding='utf8');payload=json.loads(gzip.decompress((R/'assets/heroes-runtime27.json.gz').read_bytes()));embedded=base64.b64decode(re.search(r"const heroRaw=Uint8Array.from\(atob\('([^']+)'",s)[1]);assert embedded==(R/'assets/heroes-runtime27.json.gz').read_bytes()
assert [h['id'] for h in payload]==['octavio','damiao','baltazar','turak'];report=[]
for h in payload:
 assert h['source']=='Personagens_PSX_UV_Separadas.blend';assert len(h['frames'])==48
 sizes=[];motion=[]
 for f in h['frames']:
  raw=base64.b64decode(f);v=struct.unpack('<'+'f'*(len(raw)//4),raw);assert len(v)%33==0;assert all(math.isfinite(x) for x in v);assert abs(min(v[1::11]))<1e-5;assert max(v[1::11])<2.5
  assert all(0<=x<=1 for x in v[6::11]+v[7::11]);sizes.append(len(v));motion.append(hashlib.sha256(raw).hexdigest())
 assert len(set(sizes))==1;assert len(set(motion[:16]))>8 and len(set(motion[16:]))>24
 p=R/'assets/rigged'/(h['id']+'.glb');b=p.read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);assert g.get('skins');assert {a['name'] for a in g['animations']}=={'Idle_Loop','Walk_Loop'};assert all(im.get('bufferView') is not None for im in g['images'])
 if h['id']=='octavio':assert any(n.get('name')=='Octavio_Mascara_REMOVIVEL' for n in g['nodes'])
 report.append({'id':h['id'],'sourceVertices':h['sourceVertices'],'triangles':sizes[0]//33,'rig':True,'clips':2,'uniquePoses':len(set(motion)),'embeddedTextures':True})
source=R/'assets/source/Personagens_PSX_UV_Separadas.blend';provenance=json.loads((R/'PROVENIENCIA-27.json').read_text());assert hashlib.sha256(source.read_bytes()).hexdigest()==provenance['sourceSHA256']
manifest=json.loads((R/'MANIFESTO-27.json').read_text());mapbytes=base64.b64decode(re.search(r'<script id="asset"[^>]*>(.*?)</script>',s,re.S)[1]);assert hashlib.sha256(mapbytes).hexdigest()==manifest['mapSHA256'];assert 'fract(planar/meters)' in s
(R/'TESTES-PERSONAGENS-27.json').write_text(json.dumps({'characters':report,'sourcePreserved':True,'mapPreserved':True,'runtimeMatchesFiles':True,'browserVisualCheck':False},indent=2));print('PASS: source, four rigs, original textures, 192 poses, two clips per GLB, removable mask, map integrity')

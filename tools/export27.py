import bpy,math,json,struct,base64,gzip,hashlib,re
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1];SOURCE=R/'assets/source/Personagens_PSX_UV_Separadas.blend'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE),load_ui=False,use_scripts=False)
layout=json.loads((R/'assets/atlas-layout27.json').read_text());names=['Octavio','Damiao','Baltazar','Turak'];heroes=[];audit=[]
for name in names:
 rig=bpy.data.objects[name+'_RIG'];objects=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(name+'_')];heroes.append((name,rig,objects))
 for o in objects:o.hide_set(False);o.hide_viewport=False;o.hide_render=False
 rig.hide_set(False);rig.hide_viewport=False
 # Preserve bind matrices, vertices, topology, weights and UVs; convert Rigify to export-only deform hierarchy.
 rig.animation_data_clear()
 for pb in rig.pose.bones:
  for c in list(pb.constraints):pb.constraints.remove(c)
  pb.matrix_basis=Matrix.Identity(4)
 bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT');eb=rig.data.edit_bones
 for b in list(eb):
  if not b.name.startswith('DEF-') and b.name!='root':eb.remove(b)
 for b in eb:
  if b.name=='root':continue
  if not b.parent:b.parent=eb['root']
 for side in ['L','R']:
  chain=['thigh.'+side,'thigh.'+side+'.001','shin.'+side,'shin.'+side+'.001','foot.'+side,'toe.'+side];parent='DEF-spine'
  for n in chain:
   b=eb.get('DEF-'+n)
   if b:b.use_connect=False;b.parent=eb[parent];parent=b.name
  chain=['shoulder.'+side,'upper_arm.'+side,'upper_arm.'+side+'.001','forearm.'+side,'forearm.'+side+'.001','hand.'+side];parent='DEF-spine.003'
  for n in chain:
   b=eb.get('DEF-'+n)
   if b:b.use_connect=False;b.parent=eb[parent];parent=b.name
 bpy.ops.object.mode_set(mode='OBJECT')
 for pb in rig.pose.bones:pb.rotation_mode='QUATERNION'
 audit.append({'id':name.lower(),'objects':[{ 'name':o.name,'vertices':len(o.data.vertices),'faces':len(o.data.polygons),'uvLayers':[u.name for u in o.data.uv_layers]} for o in objects],'bones':len(rig.data.bones)})
# Library only used as motion source; its mannequin is never exported as a protagonist.
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(R/'assets/animations/Quaternius-UAL1-Standard.glb'));libobjects=set(bpy.data.objects)-before;src=next(o for o in libobjects if o.type=='ARMATURE');src.animation_data_create()
for t in src.animation_data.nla_tracks:t.mute=True
mapping={'DEF-spine':'pelvis','DEF-spine.001':'spine_01','DEF-spine.002':'spine_02','DEF-spine.003':'spine_03','DEF-spine.004':'neck_01','DEF-spine.005':'neck_01','DEF-spine.006':'Head'}
for side,short in [('L','l'),('R','r')]:
 for target,source in [('shoulder','clavicle'),('upper_arm','upperarm'),('forearm','lowerarm'),('hand','hand'),('thigh','thigh'),('shin','calf'),('foot','foot'),('toe','ball')]:
  mapping['DEF-'+target+'.'+side]=source+'_'+short;mapping['DEF-'+target+'.'+side+'.001']=source+'_'+short
 for finger,sf in [('f_index','index'),('f_middle','middle'),('f_ring','ring'),('f_pinky','pinky'),('thumb','thumb')]:
  for k in range(1,4):mapping[f'DEF-{finger}.{k:02d}.{side}']=f'{sf}_{k:02d}_{short}'
mapping={k:v for k,v in mapping.items() if not any(t in k for t in ['f_index','f_middle','f_ring','f_pinky','thumb'])}
(R/'assets/retarget-map27.json').write_text(json.dumps(mapping,indent=2))
payload=[]
for hi,(name,rig,objects) in enumerate(heroes):
 originalWorld=rig.matrix_world.copy();inv=originalWorld.inverted();bpy.context.view_layer.update()
 pts=[inv@o.matrix_world@v.co for o in objects for v in o.data.vertices];minz=min(v.z for v in pts);maxz=max(v.z for v in pts);height=2.04 if name=='Baltazar' else 1.8;factor=height/(maxz-minz);cx=(min(v.x for v in pts)+max(v.x for v in pts))/2
 # Keep bind-world transforms intact. Normalize only exported runtime coordinates.
 frames=[];actions=[]
 for clip,count in [('Idle_Loop',16),('Walk_Loop',32)]:
  sourceAction=bpy.data.actions[clip];src.animation_data.action=sourceAction
  if sourceAction.slots:src.animation_data.action_slot=sourceAction.slots[0]
  action=bpy.data.actions.new(name+'_'+('Idle' if count==16 else 'Walk'));rig.animation_data_create();rig.animation_data.action=action;actions.append(action);start,end=sourceAction.frame_range
  for k in range(count+1):
   f=start+(end-start)*k/count;bpy.context.scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();computed={}
   def calc(b):
    if b.name in computed:return computed[b.name]
    par=calc(b.parent) if b.parent else Matrix.Identity(4);pr=b.parent.matrix_local if b.parent else Matrix.Identity(4);base=par@pr.inverted()@b.matrix_local;sn=mapping.get(b.name)
    if sn and sn in src.pose.bones:
     sb=src.data.bones[sn];sp=src.pose.bones[sn];q=sp.matrix.to_quaternion()@sb.matrix_local.to_quaternion().inverted();align=Matrix.Identity(3).to_quaternion()
     if any(t in b.name for t in ['upper_arm','forearm','thigh','shin','foot','hand','toe']):align=(b.tail_local-b.head_local).normalized().rotation_difference((sb.tail_local-sb.head_local).normalized())
     rotation=q@b.matrix_local.to_quaternion()
     if any(t in b.name for t in ['upper_arm','forearm','thigh','shin','foot','hand','toe']):rotation=(b.tail_local-b.head_local).normalized().rotation_difference((sp.tail-sp.head).normalized())@b.matrix_local.to_quaternion()
     desired=rotation.to_matrix().to_4x4();desired.translation=base.translation
    else:desired=base
    computed[b.name]=desired;pb=rig.pose.bones[b.name];basis=b.convert_local_to_pose(desired,b.matrix_local,parent_matrix=par,parent_matrix_local=pr,invert=True);loc,rot,scale=basis.decompose();pb.location=loc;pb.rotation_quaternion=rot;pb.scale=scale
    return desired
   for b in rig.data.bones:calc(b)
   bpy.context.view_layer.update()
   for pb in rig.pose.bones:
    pb.keyframe_insert('rotation_quaternion',frame=f);pb.keyframe_insert('location',frame=f)
   if k==count:continue
   values=[];dg=bpy.context.evaluated_depsgraph_get()
   for o in objects:
    ev=o.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles();transform=inv@ev.matrix_world;nm=transform.to_3x3().inverted().transposed()
    for tri in me.loop_triangles:
     mat=o.data.materials[tri.material_index];tex=next(n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE');uvnode=next((n for n in mat.node_tree.nodes if n.type=='UVMAP'),None);uv=me.uv_layers.get(uvnode.uv_map) if uvnode else me.uv_layers.active;uv=uv or me.uv_layers.active;rx,ry,rw,rh=layout[tex.image.name]
     for vi,li in zip(tri.vertices,tri.loops):
      v=transform@me.vertices[vi].co;n=nm@tri.normal;n.normalize();u=uv.data[li].uv;values.extend([(v.x-cx)*factor,(v.z-minz)*factor,-v.y*factor,n.x,n.z,-n.y,(rx+max(0,min(1,u.x))*(rw-1)+.5)/4096,(ry+(1-max(0,min(1,u.y)))*(rh-1)+.5)/4096,1,1,1])
    ev.to_mesh_clear()
   floor=min(values[1::11])
   for j in range(1,len(values),11):values[j]-=floor
   frames.append(base64.b64encode(struct.pack('<'+'f'*len(values),*values)).decode())
  track=rig.animation_data.nla_tracks.new();track.name=clip;track.strips.new(clip,0,action);track.mute=True;rig.animation_data.action=None
 bpy.ops.object.select_all(action='DESELECT');rig.select_set(True)
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=rig
 rig.animation_data.action=actions[0];bpy.context.scene.frame_set(0)
 holder=bpy.data.objects.new(name+'_MetricRoot',None);bpy.context.collection.objects.link(holder);holder.matrix_world=Matrix.Scale(factor,4)@Matrix.Translation(Vector((-cx,0,-minz)))@originalWorld.inverted();rig.parent=holder;rig.matrix_parent_inverse=Matrix.Identity(4);rig.matrix_basis=originalWorld;holder.select_set(True);bpy.context.view_layer.update()
 bpy.ops.export_scene.gltf(filepath=str(R/'assets/rigged'/(name.lower()+'.glb')),use_selection=True,export_format='GLB',export_animations=True,export_animation_mode='NLA_TRACKS',export_def_bones=True,export_force_sampling=True)
 rig.parent=None;rig.matrix_world=originalWorld;bpy.data.objects.remove(holder,do_unlink=True)
 payload.append({'id':name.lower(),'source':SOURCE.name,'sourceVertices':sum(len(o.data.vertices) for o in objects),'frames':frames,'idleFrames':16,'walkFrames':32,'stride':1.04 if hi==2 else .88,'animations':['Quaternius/Idle_Loop','Quaternius/Walk_Loop']})
 print('EXPORTED',name,len(frames),len(values)//11,flush=True)
(R/'assets/heroes-runtime27.json.gz').write_bytes(gzip.compress(json.dumps(payload).encode()));(R/'PROVENIENCIA-27.json').write_text(json.dumps({'source':str(SOURCE),'sourceSHA256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'heroes':audit},indent=2))
for o in libobjects:bpy.data.objects.remove(o,do_unlink=True)
for o in list(bpy.data.objects):
 if o.name.startswith(('WGT','METARIG')):bpy.data.objects.remove(o,do_unlink=True)
for i,(name,rig,objects) in enumerate(heroes):
 rig.animation_data.action=bpy.data.actions[name+'_Idle']
 for im in bpy.data.images:
  if im.size[0] and not im.packed_file:
   try:im.pack()
   except:pass
bpy.context.scene.frame_set(0);bpy.ops.wm.save_as_mainfile(filepath=str(R/'assets/rigged/protagonistas-animados27.blend'))


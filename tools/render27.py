import bpy,json,gzip,base64,struct,math
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/GrupoFarma/Documents/Codex/2026-10-21/ana/outputs/A-Noite-Vermelha-HTML-27');bpy.ops.wm.read_factory_settings(use_empty=True);heroes=json.loads(gzip.decompress((R/'assets/heroes-runtime27.json.gz').read_bytes()));im=bpy.data.images.load(str(R/'assets/hero-atlas27.png'));mat=bpy.data.materials.new('Texturas originais');mat.use_nodes=True;tex=mat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=im;tex.interpolation='Closest';mat.node_tree.links.new(tex.outputs['Color'],mat.node_tree.nodes['Principled BSDF'].inputs['Base Color']);mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=1
objects=[]
for i,h in enumerate(heroes):
 raw=base64.b64decode(h['frames'][0]);v=struct.unpack('<'+'f'*(len(raw)//4),raw);rows=[v[j:j+11] for j in range(0,len(v),11)];mesh=bpy.data.meshes.new(h['id']);mesh.from_pydata([(r[0],-r[2],r[1]) for r in rows],[],[(j,j+1,j+2) for j in range(0,len(rows),3)]);uv=mesh.uv_layers.new()
 for loop in mesh.loops:r=rows[loop.vertex_index];uv.data[loop.index].uv=(r[6],1-r[7])
 ob=bpy.data.objects.new(h['id'],mesh);bpy.context.collection.objects.link(ob);ob.location.x=(i-1.5)*1.5;mesh.materials.append(mat);objects.append(ob)
 bpy.ops.object.text_add(location=(ob.location.x,-.3,-.18));t=bpy.context.object;t.data.body=h['id'].upper();t.data.align_x='CENTER';t.data.size=.16;t.rotation_euler=(math.pi/2,0,0)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=16;scene.render.resolution_x=1500;scene.render.resolution_y=700;scene.render.resolution_percentage=100
bpy.ops.object.camera_add(location=(.8,-12,3.3));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,1))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=7.;scene.camera=cam
scene.world=bpy.data.worlds.new('World');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.25,.25,.25,1)
for loc in [(0,-4,6),(-4,-2,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=800;o.data.size=6;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
scene.view_settings.view_transform='Standard';scene.render.filepath=str(R/'assets/previa-repouso27.png');bpy.ops.render.render(write_still=True)
for ob,h in zip(objects,heroes):
 raw=base64.b64decode(h['frames'][24]);v=struct.unpack('<'+'f'*(len(raw)//4),raw)
 for j,vert in enumerate(ob.data.vertices):vert.co=(v[j*11],-v[j*11+2],v[j*11+1])
scene.render.filepath=str(R/'assets/previa-caminhada27.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'assets/rigged/avaliacao-poses27.blend'))

# Tray for 3x3_+1_OLED_2026.9.26c with "choyapad" cut into the bottom (bed) face (the choya drawing was dropped 2026-10-17).
# Reuses the geometry/tray() from build_cover-plate.py; art lives in choya_art.py.
# 2026-10-18: tilted 10 deg (wedge bottom, deeper Pro Micro pocket; same cover plate).
# 2026-10-18: text back to the size/spot it had under the choya (h=6, ~32 mm wide, low on the floor),
# and the 2-colour 3mf is now written in Bambu Studio's own project layout so it isn't loaded as "geometry only".
import sys, os
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
src = open(os.path.join(here, "build_cover-plate.py")).read()
exec(src[:src.index("def stl(")])                    # params + rrect/box/tray()
exec(src[src.index("def stl("):src.index("out = sys.argv[1]")])
from shapely import affinity
from choya_art import art as choya_art, text        # text only, placed where it sat under the choya
from manifold3d import FillRule
art_depth = 0.6                                       # 3 layers @ 0.2

out = sys.argv[1]
# the choya+text group was centred on the floor with the text under the choya; keep the text in that exact spot
minx, miny, maxx, maxy = choya_art().bounds
a = text()
# viewed from underneath the tray is mirrored left-right, so mirror x; centre on the tray floor
cx, cy = pcb_w / 2, pcb_h / 2
a = affinity.translate(affinity.scale(a, -1, 1, origin=((minx + maxx) / 2, (miny + maxy) / 2)), cx - (minx + maxx) / 2, cy - (miny + maxy) / 2)
feet_ok = all(not a.intersects(__import__("shapely").geometry.Point(p).buffer(feet_d / 2 + 0.5)) for p in holes)

# --- 2026-10-18 tilt: wedge under the tray so the back (OLED / Pro Micro end, high y) sits higher on the desk.
# PCB + cover geometry unchanged (same cover plate); the bottom plane runs from the front-bottom edge down toward the back.
# The extra thickness at the back is used for a deeper pocket under the Pro Micro (tall headers / sockets).
import math
tilt = 10.0                                           # degrees
min_floor = 1.2                                       # plastic left under the Pro Micro pocket at its shallowest (front) edge
ta = math.tan(math.radians(tilt)); depth_y = pcb_h + 2 * o
rise = depth_y * ta                                   # extra height at the back
plane_z = lambda y: -(y + o) * ta                     # bottom plane in tray coords
T0 = tray() + U([cyl(p[0], p[1], -0.01, feet_depth + 0.02, feet_d) for p in holes])    # flat tray with the feet recesses filled back in
wedge = rrect(-o, -o, pcb_w + o, pcb_h + o, outer_r, rise + 0.02).translate([0, 0, -rise - 0.01])
wedge = wedge.trim_by_plane([0, math.sin(math.radians(tilt)), math.cos(math.radians(tilt))], -o * math.sin(math.radians(tilt)))
mcu_pocket = [promicro[0] - 0.5, promicro[1] - 0.5, pcb_w + clr, promicro[3]]   # Pro Micro footprint + 0.5 mm, out to the inner wall
pocket_z = plane_z(mcu_pocket[1]) + min_floor
Tt = T0 + wedge - box(mcu_pocket[0], mcu_pocket[1], pocket_z, mcu_pocket[2], mcu_pocket[3], floor_t + 0.01)
zpb = floor_t + standoff_h                            # PCB bottom
print("tilt %.1f deg: front %.1f mm, back %.1f mm tall (tray only; +%.1f cover)" % (tilt, H, H + rise, zt - H))
print("under-PCB room: %.1f mm elsewhere, %.1f mm over the Pro Micro pocket (was %.1f)" % (standoff_h, zpb - pocket_z, standoff_h))
# into the print/bed frame: bottom plane -> z = 0 (shift y by o, rotate +tilt about x); bed y = (tray y + o) / cos
T = Tt.translate([0, o, 0]).rotate([tilt, 0, 0])
bed_y = lambda y: (y + o) / math.cos(math.radians(tilt))
T = T - U([cyl(p[0], bed_y(p[1]), -0.01, feet_depth + 0.01, feet_d) for p in holes])
a = affinity.translate(a, 0, bed_y((a.bounds[1] + a.bounds[3]) / 2) - (a.bounds[1] + a.bounds[3]) / 2)   # text keeps its size, centre mapped onto the slope
print("tilted tray bbox", [round(v, 2) for v in T.bounding_box()], "genus", T.genus())

polys = []
for g in getattr(a, "geoms", [a]):
    polys.append([list(c) for c in g.exterior.coords[:-1]][::1 if g.exterior.is_ccw else -1])
    for h in g.interiors:
        polys.append([list(c) for c in h.coords[:-1]][::-1 if h.is_ccw else 1])
cs = CrossSection(polys, FillRule.Positive)
cut = Manifold.extrude(cs, art_depth + 0.01).translate([0, 0, -0.01])
Ta = T - cut
print("art bbox (bed coords)", [round(v, 2) for v in a.bounds], "cut volume %.1f mm3" % (T.volume() - Ta.volume()))
print("clear of feet recesses:", feet_ok, " floor left above art %.2f mm (front edge)" % (floor_t - art_depth))
stl(Ta, out + "_tray-choya.stl")

# --- 2-colour version for manual filament swaps (no AMS): text is a separate part filling a 2-layer recess ---
mm_depth = 0.4                                        # 2 layers @ 0.2 -> 2 swaps (into text on layer 1, back on layer 2)
cut2 = Manifold.extrude(cs, mm_depth + 0.01).translate([0, 0, -0.01])
body = T - cut2
inlay = Manifold.extrude(cs, mm_depth)
print("2-colour: body vol %.1f, inlay vol %.1f, overlap %.4f mm3" % (body.volume(), inlay.volume(), (body ^ inlay).volume()))
stl(body, out + "_tray-choya-2color_body.stl"); stl(inlay, out + "_tray-choya-2color_choya-inlay.stl")

# Bambu Studio project layout (as BambuStudio 02.x writes it): meshes in 3D/Objects/object_1.model, the plate object in
# 3D/3dmodel.model referencing them as components, part -> filament in Metadata/model_settings.config.
# Plate filament order is pinned (layer 1: case then text; layers 2+: text then case) so every Bambu slices the same
# 2 manual swaps: start on CASE colour, swap to text mid-layer-1, back to case mid-layer-2. (Unpinned, GUI and CLI picked
# different orders and the manual swaps came out inverted.)
# Metadata/project_settings.config = bambu_A1_project_settings.config: stock A1 0.4 / 0.20mm Standard / 2x Generic PLA,
# flattened from Bambu Studio 02.05.00.66 (Bambu Studio 2.5 refuses newer-stamped 3mfs)'s system profiles and exported by its CLI, with two recorded edits
# (change_filament_gcode = "M400 U1" for manual swaps, enable_prime_tower = 0). Without it Bambu says "not from Bambu Lab".
import zipfile, uuid, numpy as np
x0, y0, _, x1, y1, _ = body.bounding_box()
centre = [-(x0 + x1) / 2, -(y0 + y1) / 2, 0]          # mesh centred on its own origin; build item puts it mid-bed
parts = [(1, "tray (case colour)", 1, body.translate(centre)), (2, "choyapad text (accent colour)", 2, inlay.translate(centre))]
def mesh_xml(oid, m):
    mesh = m.to_mesh(); v = np.asarray(mesh.vert_properties)[:, :3]; tri = np.asarray(mesh.tri_verts)
    return ['<object id="%d" p:UUID="%s" type="model"><mesh><vertices>' % (oid, uuid.uuid4())] + \
           ['<vertex x="%.5f" y="%.5f" z="%.5f"/>' % tuple(p) for p in v] + ['</vertices><triangles>'] + \
           ['<triangle v1="%d" v2="%d" v3="%d"/>' % tuple(t) for t in tri] + ['</triangles></mesh></object>'], len(tri)
NS = 'unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" ' \
     'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p"'
objs, faces = [], {}
for pid, _, _, m in parts:
    xml, faces[pid] = mesh_xml(pid, m); objs += xml
obj_model = ['<?xml version="1.0" encoding="UTF-8"?>\n<model %s>' % NS, '<metadata name="BambuStudio:3mfVersion">1</metadata><resources>'] + \
            objs + ['</resources><build/></model>']
main_model = '''<?xml version="1.0" encoding="UTF-8"?>
<model %s>
 <metadata name="Application">BambuStudio-02.05.00.66</metadata>
 <metadata name="BambuStudio:3mfVersion">1</metadata>
 <metadata name="Title">3x3_+1_OLED_2026.9.26c tray choyapad</metadata>
 <resources>
  <object id="3" p:UUID="%s" type="model">
   <components>
%s
   </components>
  </object>
 </resources>
 <build p:UUID="%s">
  <item objectid="3" p:UUID="%s" transform="1 0 0 0 1 0 0 0 1 128 128 0" printable="1"/>
 </build>
</model>
''' % (NS, uuid.uuid4(), "\n".join('    <component p:path="/3D/Objects/object_1.model" objectid="%d" p:UUID="%s" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>'
                                    % (pid, uuid.uuid4()) for pid, _, _, _ in parts), uuid.uuid4(), uuid.uuid4())
part_cfg = "".join('''    <part id="%d" subtype="normal_part">
      <metadata key="name" value="%s"/>
      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>
      <metadata key="extruder" value="%d"/>
      <mesh_stat face_count="%d" edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>
    </part>
''' % (pid, name, ext, faces[pid]) for pid, name, ext, _ in parts)
cfg = '''<?xml version="1.0" encoding="UTF-8"?>
<config>
  <object id="3">
    <metadata key="name" value="3x3_+1_OLED_2026.9.26c tray choyapad"/>
    <metadata key="extruder" value="1"/>
    <metadata face_count="%d"/>
%s  </object>
  <plate>
    <metadata key="plater_id" value="1"/>
    <metadata key="plater_name" value="tray"/>
    <metadata key="locked" value="false"/>
    <metadata key="filament_map_mode" value="Auto For Flush"/>
    <metadata key="filament_maps" value="1 1"/>
    <metadata key="print_sequence" value="by layer"/>
    <metadata key="first_layer_print_sequence" value="1 2"/>
    <metadata key="other_layers_print_sequence" value="2 2147483646 2 1"/>
    <metadata key="other_layers_print_sequence_nums" value="1"/>
    <model_instance>
      <metadata key="object_id" value="3"/>
      <metadata key="instance_id" value="0"/>
      <metadata key="identify_id" value="100"/>
    </model_instance>
  </plate>
  <assemble>
   <assemble_item object_id="3" instance_id="0" transform="1 0 0 0 1 0 0 0 1 128 128 0" offset="0 0 0" />
  </assemble>
</config>
''' % (sum(faces.values()), part_cfg)
REL = "http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"
with zipfile.ZipFile(out + "_tray-choya-2color.3mf", "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>\n <Default Extension="png" ContentType="image/png"/>\n <Default Extension="gcode" ContentType="text/x.gcode"/>\n</Types>')
    z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="%s"/>\n</Relationships>' % REL)
    z.writestr("3D/_rels/3dmodel.model.rels", '<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n <Relationship Target="/3D/Objects/object_1.model" Id="rel-1" Type="%s"/>\n</Relationships>' % REL)
    z.writestr("3D/3dmodel.model", main_model)
    z.writestr("3D/Objects/object_1.model", "".join(obj_model))
    z.writestr("Metadata/model_settings.config", cfg)
    z.write(os.path.join(here, "bambu_A1_project_settings.config"), "Metadata/project_settings.config")
    z.writestr("Metadata/slice_info.config", '<?xml version="1.0" encoding="UTF-8"?>\n<config>\n  <header>\n    <header_item key="X-BBL-Client-Type" value="slicer"/>\n    <header_item key="X-BBL-Client-Version" value="02.05.00.66"/>\n  </header>\n</config>\n')

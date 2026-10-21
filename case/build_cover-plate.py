# Python/manifold3d cover-plate for 3x3_+1_OLED_2026.9.26c: top-left MX at case y 68.85
import sys, struct, numpy as np
from manifold3d import Manifold, CrossSection, JoinType
FN = 64
pcb_w, pcb_h, pcb_t = 65.6, 81.5, 1.6
clr, wall, floor_t = 0.4, 2.4, 2.0
mcu_hang, pin_hang, under_clr, rim_above = 5.0, 3.5, 1.5, 1.0
standoff_d, insert_d, insert_depth = 5.6, 3.2, 4.5
usb_w, usb_sill = 13.0, 1.0
feet_d, feet_depth = 10.0, 0.8
cover_top, plate_t, sw_open, sw_cut = 5.0, 1.5, 16.2, 14.0
boss_d, screw_d, cbore_d, cbore_depth = 5.0, 2.4, 4.4, 2.0
outer_r, inner_r = 3.0, 1.0
standoff_h = max(mcu_hang, pin_hang) + under_clr
H = floor_t + standoff_h + pcb_t + rim_above
zpt = floor_t + standoff_h + pcb_t; zt = zpt + cover_top; zp = zt - plate_t
o = clr + wall
holes = [[3.5, 3.5], [62.1, 3.5], [3.5, 78.0], [62.1, 78.0]]
promicro = [32.2, 57.0, 65.8, 75.5]
usb_cy = 126 - 59.77
switches = [[14.3, 68.85], [14.3, 49.8], [33.35, 49.8], [52.4, 49.8], [14.3, 30.75], [33.35, 30.75], [52.4, 30.75],
            [14.3, 11.7], [33.35, 11.7], [52.4, 11.7]]
oled_win = [24.4, 60.4, 63.6, 74.8]   # old: whole module + top Pro Micro pin row (no longer cut)
# OLED J1 header pins at case x 26.6, y 63.2..70.82 (centre 67.01). Measured module (2026-10-08): 38.09 x 12.12,
# pins 2.73 from left edge -> module x 23.87..61.96; glass 5.97 from left / 5.32 from right -> x 29.84..56.64,
# 12.26 tall centred on pins -> y 60.88..73.14
oled_glass  = [30.54, 60.78, 57.44, 73.24] # through-window: glass + 0.1 mm top/bottom; test fit 2026-10-08: left edge +1, right edge +0.5
# header pin tips measured 7.58 above PCB bottom -> z 16.08, ~1 mm above the plate top: they poke through a slot
# and are covered by a glue-on cap (printed separately; a raised hood on the cover would ruin the face-down print)
oled_pin_slot = [25.2, 61.9, 28.0, 72.1]   # pins at x 26.6, y 63.2..70.82 + solder joints
pin_top = zpt - pcb_t + 7.58
cap_outer, cap_r, cap_roof = [24.0, 60.78, 30.44, 73.24], 0.8, 0.8
cap_h = pin_top + 0.3 + cap_roof - zt     # sits on the plate top
oled_pocket = [23.4, 60.5, 64.9, 74.8]     # underside recess: module + header + top Pro Micro pin row
oled_skin   = 0.6                          # plate left over the module PCB (pocket ceiling = zt - skin)

def rrect(x0, y0, x1, y1, r, h):
    cs = CrossSection.square([x1 - x0 - 2 * r, y1 - y0 - 2 * r]).offset(r, JoinType.Round, circular_segments=FN)
    return Manifold.extrude(cs, h).translate([x0 + r, y0 + r, 0])
def box(x0, y0, z0, x1, y1, z1):
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])
def cyl(x, y, z, h, d):
    return Manifold.cylinder(h, d / 2, d / 2, FN).translate([x, y, z])
def U(ms):
    r = ms[0]
    for m in ms[1:]: r = r + m
    return r

def tray():
    shell = rrect(-o, -o, pcb_w + o, pcb_h + o, outer_r, H) - rrect(-clr, -clr, pcb_w + clr, pcb_h + clr, inner_r, H + 1).translate([0, 0, floor_t])
    so = [cyl(p[0], p[1], floor_t - 0.01, standoff_h + 0.01, standoff_d) - box(promicro[0], promicro[1], 0, promicro[2], promicro[3], H + 1) for p in holes]
    t = U([shell] + so)
    cuts = []
    for p in holes:
        cuts.append(cyl(p[0], p[1], floor_t + standoff_h - insert_depth, insert_depth + 0.1, insert_d))
        cuts.append(cyl(p[0], p[1], -0.01, feet_depth + 0.01, feet_d))
    cuts.append(box(pcb_w - 0.1, usb_cy - usb_w / 2, usb_sill, pcb_w + o + 1, usb_cy + usb_w / 2, H + 1))
    return t - U(cuts)

def cover():
    shell = rrect(-o, -o, pcb_w + o, pcb_h + o, outer_r, zt - H).translate([0, 0, H]) - \
            rrect(-clr, -clr, pcb_w + clr, pcb_h + clr, inner_r, zp - H + 0.01).translate([0, 0, H - 0.01])
    bosses = [cyl(p[0], p[1], zpt, zp - zpt + 0.01, boss_d) for p in holes]
    usbfill = box(pcb_w + clr + 0.1, usb_cy - usb_w / 2, zpt - pcb_t + 0.3, pcb_w + o, usb_cy + usb_w / 2, H + 0.01)
    c = U([shell] + bosses + [usbfill])
    cuts = [box(s[0] - sw_cut / 2, s[1] - sw_cut / 2, zpt - 1, s[0] + sw_cut / 2, s[1] + sw_cut / 2, zt + 1) for s in switches]
    cuts.append(box(oled_pocket[0], oled_pocket[1], zp - 1, oled_pocket[2], oled_pocket[3], zt - oled_skin))
    cuts.append(box(oled_glass[0], oled_glass[1], zp - 1, oled_glass[2], oled_glass[3], zt + 1))
    cuts.append(box(oled_pin_slot[0], oled_pin_slot[1], zp - 1, oled_pin_slot[2], oled_pin_slot[3], zt + 1))
    for p in holes:
        cuts.append(cyl(p[0], p[1], zpt - 1, zt - zpt + 2, screw_d))
        cuts.append(cyl(p[0], p[1], zt - cbore_depth, cbore_depth + 1, cbore_d))
    return c - U(cuts)

def stl(m, fn):
    mesh = m.to_mesh(); v = np.asarray(mesh.vert_properties)[:, :3]; tri = np.asarray(mesh.tri_verts)
    with open(fn, "wb") as f:
        f.write(b"manifold3d".ljust(80, b" ")); f.write(struct.pack("<I", len(tri)))
        for a, b, c in tri:
            n = np.cross(v[b] - v[a], v[c] - v[a]); ln = np.linalg.norm(n); n = n / ln if ln else n
            f.write(struct.pack("<12fH", *n, *v[a], *v[b], *v[c], 0))
    return mesh

out = sys.argv[1]
def pin_cap():   # in case coords, sitting on the plate top; hollow underneath over the pin slot
    x0, y0, x1, y1 = cap_outer
    k = rrect(x0, y0, x1, y1, cap_r, cap_h).translate([0, 0, zt])
    return k - box(oled_pin_slot[0], oled_pin_slot[1], zt - 1, oled_pin_slot[2], oled_pin_slot[3], zt + cap_h - cap_roof)

T = tray(); C = cover(); K = pin_cap()
print("pin tips z %.2f, cap height %.2f above plate, cap/cover overlap %.4f mm3" % (pin_top, cap_h, (K ^ C).volume()))
Kp = K.rotate([0, 180, 0]).translate([cap_outer[2] + pcb_w + 2 * o + 5, -cap_outer[1], zt + cap_h])  # roof down, beside the cover
Cp = C.rotate([0, 180, 0]).translate([pcb_w + o, o, zt])   # cover_print: top face down
for m, n in ((T, "tray"), (C, "cover-plate"), (Cp, "cover-plate_print")):
    print(n, "genus", m.genus(), "vol %.1f" % m.volume(), "bbox", [round(x, 2) for x in m.bounding_box()])
stl(T, out + "_tray.stl"); stl(Cp, out + "_cover-plate.stl"); stl(Kp, out + "_oled-pin-cap.stl")
print("H", H, "zpt", zpt, "zt", zt, "zp", zp)

# top-view slice through the plate for a quick visual check
from PIL import Image, ImageDraw
S = 10; pad = 20
sl = C.slice(zt - oled_skin / 2)   # through the top skin: shows the visible openings
polys = sl.to_polygons()
W = int((pcb_w + 2 * o) * S) + 2 * pad; Hh = int((pcb_h + 2 * o) * S) + 2 * pad + 30
im = Image.new("RGB", (W, Hh), "white"); d = ImageDraw.Draw(im)
P = lambda x, y: (pad + (x + o) * S, pad + (pcb_h + o - y) * S)
import numpy as np
areas = [0.5 * np.sum(p[:, 0] * np.roll(p[:, 1], -1) - np.roll(p[:, 0], -1) * p[:, 1]) for p in polys]
for p, a in sorted(zip(polys, areas), key=lambda q: -abs(q[1])):
    d.polygon([P(*q) for q in p], fill=(120, 160, 220) if a > 0 else "white", outline="black")
d.text((pad, Hh - 28), f"top-skin slice @ z={zt - oled_skin/2:.2f}  cutouts {sw_cut} mm  plate {plate_t} mm", fill="black")
im.save(out + "_cover-plate-layout.png")

# DO-35 clearance: diode bodies (B side, 2.2 mm tall incl. lead) + front solder joints (2.0 mm) vs tray/cover
if len(sys.argv) > 2:
    DS = [(x - 100, 126 - y) for x in (123.5, 142.55, 161.6) for y in (79.0575, 98.1075, 117.1575)]  # cathode, case frame
    zpb = zpt - pcb_t
    hit_t = hit_c = 0.0
    for cx, cy in DS:
        body = box(cx - 1.25, cy - 1.05, zpb - 2.2, cx + 1.25, cy + 8.67, zpb)            # courtyard footprint, below PCB
        joints = box(cx - 0.8, cy - 0.8, zpt, cx + 0.8, cy + 8.42, zpt + 2.0)             # both pads, above PCB
        hit_t += (T ^ body).volume(); hit_c += (C ^ joints).volume() + (C ^ body).volume()
    print("diode/tray overlap %.4f mm3, diode/cover overlap %.4f mm3" % (hit_t, hit_c))

# 3MF of the print-oriented cover + pin cap (same meshes as the STLs), one plate
import zipfile
model = ['<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources>']
for oid, m in ((1, Cp), (2, Kp)):
    mesh = m.to_mesh(); v = np.asarray(mesh.vert_properties)[:, :3]; tri = np.asarray(mesh.tri_verts)
    model += ['<object id="%d" type="model"><mesh><vertices>' % oid] + ['<vertex x="%.5f" y="%.5f" z="%.5f"/>' % tuple(p) for p in v]
    model += ['</vertices><triangles>'] + ['<triangle v1="%d" v2="%d" v3="%d"/>' % tuple(t) for t in tri] + ['</triangles></mesh></object>']
model += ['</resources><build><item objectid="1"/><item objectid="2"/></build></model>']
with zipfile.ZipFile(out + "_cover-plate.3mf", "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr("3D/3dmodel.model", "".join(model))

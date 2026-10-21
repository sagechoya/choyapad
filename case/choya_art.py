# Choya + "choyapad" artwork for the tray bottom, as shapely geometry in mm (y up, feet at y=0, centred on x=0).
# art() returns (cut, islands): cut = area recessed into the bed face; islands are already removed from it.
# Mix of the GW2 choya refs: blue one's flower + clasped hands, pink/green spikes, pink belly seam.
import math
from shapely.geometry import Point, LineString, Polygon, box
from shapely.ops import unary_union
from shapely import affinity

G = 0.9          # detail-line width (>= 2 extrusion lines at 0.4 nozzle)

def ell(cx, cy, rx, ry, rot=0):
    e = affinity.scale(Point(0, 0).buffer(1, 64), rx, ry)
    return affinity.translate(affinity.rotate(e, rot, origin=(0, 0)), cx, cy)

def mirror(g):
    return affinity.scale(g, -1, 1, origin=(0, 0))

def both(g):
    return unary_union([g, mirror(g)])

def bez(p0, p1, p2, n=24):
    return [((1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0], (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1])
            for t in (i / n for i in range(n + 1))]

def stroke(pts, w):
    return LineString(pts).buffer(w / 2, 32)

def spike(x, y, ang, length, base):
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); px, py = -uy, ux
    return Polygon([(x + px*base/2 - ux*1.5, y + py*base/2 - uy*1.5), (x + ux*length, y + uy*length),
                    (x - px*base/2 - ux*1.5, y - py*base/2 - uy*1.5)])

def edge_line(shape, inside):
    """Detail line along shape's outline, only where it runs inside `inside` (so the silhouette isn't notched)."""
    return shape.exterior.intersection(inside.buffer(-0.35)).buffer(G / 2, 16)

def petal(cx, cy, ang, length, width):
    p = Polygon([(0, 0), (length*0.35, width/2), (length, 0), (length*0.35, -width/2)]).buffer(0.25, 16)
    return affinity.translate(affinity.rotate(p, ang, origin=(0, 0)), cx, cy)

def choya():
    body = unary_union([ell(0, 21, 16.5, 19), ell(0, 33, 15, 13.5)])
    feet = [ell(s*8.5, 3.0, 6.3, 3.1) for s in (-1, 1)]
    toes = [Point(s*8.5 + dx, 0.9).buffer(1.5, 24) for s in (-1, 1) for dx in (-3.6, 0, 3.6)]
    feet = [unary_union([f] + [t for t in toes if t.intersects(f)]) for f in feet]
    spikes = both(unary_union([spike(14.6, 39.5, 40, 5.0, 1.8), spike(15.6, 36.5, 22, 5.8, 1.9),
                               spike(16.2, 33.0, 6, 4.2, 1.7), spike(16.4, 24.0, -8, 2.8, 1.5)]))
    petal_angles = [15 + 25*k for k in range(7)]
    petals = [petal(0, 45.5, a, 8.6 if k % 2 else 7.4, 3.6) for k, a in enumerate(petal_angles)]
    notches = unary_union([Polygon([(3.4*math.cos(math.radians(a)), 45.5 + 3.4*math.sin(math.radians(a))),
                                    (12*math.cos(math.radians(a - 4.5)), 45.5 + 12*math.sin(math.radians(a - 4.5))),
                                    (12*math.cos(math.radians(a + 4.5)), 45.5 + 12*math.sin(math.radians(a + 4.5)))])
                           for a in (27.5 + 25*k for k in range(6))])
    flower = unary_union(petals + [Point(0, 45.5).buffer(3.0, 32)]) - notches
    arms = both(stroke(bez((-15.2, 21.5), (-12.5, 13.0), (-4.5, 13.6)), 5.4))
    hand_l, hand_r = ell(-2.9, 14.6, 3.5, 3.1, -10), ell(2.9, 14.6, 3.5, 3.1, 10)
    arms_hands = unary_union([arms, hand_l, hand_r])

    sil = unary_union([body - notches, flower, spikes] + feet)
    lines = [edge_line(f, body) for f in feet]                                   # feet vs body
    lines.append(edge_line(arms_hands, body))                                    # arms + hands outline
    lines.append(hand_r.exterior.intersection(hand_l.buffer(-0.3)).buffer(G / 2, 16))   # right hand over left
    for s in (-1, 1):
        for dx in (-2.4, 2.4):                                                   # toe splits
            lines.append(stroke([(s*8.5 + dx, -0.2), (s*8.5 + dx, 1.6)], G))
    lines.append(edge_line(body, flower.buffer(0.6)))                            # flower vs head
    lines.append(stroke(bez((-9.8, 32.6), (0, 43.0), (9.8, 32.6)), G))           # snout ridge over the overbite

    isl = []
    for s in (-1, 1):
        isl.append(ell(s*11.2, 35.6, 2.2, 2.4) - Point(s*11.2 + 0.6, 36.3).buffer(0.5, 16))    # eyes + glint
        isl.append(ell(s*2.4, 35.4, 0.75, 0.55))                                              # nostrils
        isl += [Point(s*13.6, 30.6).buffer(0.5, 16), Point(s*12.6, 28.0).buffer(0.5, 16)]    # freckles
    for y in (7.0, 9.4):                                                         # belly seam
        isl.append(Point(0, y).buffer(0.5, 16))
    mouth = ell(0, 29.0, 10.6, 4.9) - ell(0, 33.8, 12.2, 4.6)                    # wide overbite grin
    teeth = []
    for x in (-7.6, -4.6, -1.6, 1.6, 4.6, 7.6):                                  # upper fangs hang from the lip
        yt = 33.8 - 4.6*math.sqrt(1 - (x/12.2)**2)
        teeth.append(Polygon([(x - 0.9, yt + 0.5), (x + 0.9, yt + 0.5), (x, yt - 2.0)]).buffer(0.15))
    for x in (-5.6, 0.0, 5.6):                                                   # lower teeth point up
        yb = 29.0 - 4.9*math.sqrt(1 - (x/10.6)**2)
        teeth.append(Polygon([(x - 0.8, yb - 0.5), (x + 0.8, yb - 0.5), (x, yb + 1.6)]).buffer(0.15))
    isl.append(mouth - unary_union(teeth))
    for s in (-1, 1):                                                            # pale claw tips on the clasped hands
        for dx in (-1.6, 0.0, 1.6):
            x = s*2.9 + dx
            isl.append(Polygon([(x - 0.55, 17.3), (x + 0.55, 17.3), (x, 19.0)]).buffer(0.1))
    return sil, unary_union(lines + isl)

def text(s="choyapad", h=6.0, y_top=-3.0, font="/path/to/DejaVuSans-Bold.ttf"):
    """Raster the text at 40 px/mm and turn pixel runs into polygons (no font-outline libs on this box)."""
    from PIL import Image, ImageDraw, ImageFont
    px = 40; f = ImageFont.truetype(font, int(h * px))
    l, t, r, b = f.getbbox(s); im = Image.new("1", (r - l + 4, b - t + 4), 0)
    ImageDraw.Draw(im).text((2 - l, 2 - t), s, font=f, fill=1)
    W, H = im.size; data = im.load(); rects = []
    for yy in range(H):
        xx = 0
        while xx < W:
            if data[xx, yy]:
                x0 = xx
                while xx < W and data[xx, yy]: xx += 1
                rects.append(box(x0, -yy - 1, xx, -yy))
            xx += 1
    g = unary_union(rects).buffer(0.5).buffer(-0.5).simplify(0.4)
    g = affinity.scale(g, 1 / px, 1 / px, origin=(0, 0))
    minx, miny, maxx, maxy = g.bounds
    return affinity.translate(g, -(minx + maxx) / 2, y_top - maxy)

def art():
    sil, det = choya()
    cut = unary_union([sil - det, text()])
    return cut.buffer(0.05).buffer(-0.05)

def art_text():
    """Text-only version: just "choyapad", ~54 mm wide."""
    return text(h=10.2, y_top=0.0).buffer(0.05).buffer(-0.05)

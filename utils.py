import time
import math
import cv2
import numpy as np
from shapely.geometry import box, Point, Polygon as ShapelyPoly, MultiPolygon
from shapely.affinity import translate
from PySide6.QtGui import QImage, QPixmap

def get_superellipse_n(slider_val):
    if slider_val <= 50:
        return 0.8 + (slider_val / 50.0) * 1.25
    else:
        return 2.0 + ((slider_val - 50) / 50.0) * 6.0

def create_superellipse(center, w, h, n, points=64):
    pts = []
    if n < 0.1:
        n = 0.1
    if n > 50:
        n = 50 
    a = w / 2.0
    b = h / 2.0
    for i in range(points):
        theta = 2 * math.pi * i / points
        cos_t = math.cos(theta); sin_t = math.sin(theta)
        x = a * (abs(cos_t) ** (2/n)) * np.sign(cos_t)
        y = b * (abs(sin_t) ** (2/n)) * np.sign(sin_t)
        pts.append((x, y))
    return translate(ShapelyPoly(pts), center.x, center.y)

def create_squircle(center, size, radius):
    if radius <= 0:
        return box(center.x - size/2, center.y - size/2, center.x + size/2, center.y + size/2)
    b = box(-size/2, -size/2, size/2, size/2)
    if radius >= size / 2.0 - 0.001:
        shape = Point(0,0).buffer(size / 2.0)
    else:
        shape = b.buffer(-radius).buffer(radius).simplify(0.001)
    return translate(shape, center.x, center.y)

# ============================================================================
# VECTOR STITCHING
# ============================================================================

def find_closest_points(outer, inner):
    out_pts = np.array(outer).reshape(-1, 2)
    in_pts = np.array(inner).reshape(-1, 2)
    min_dist = float('inf'); best_pair = (0, 0)
    for i, p_out in enumerate(out_pts):
        dists = np.linalg.norm(in_pts - p_out, axis=1)
        min_d = np.min(dists)
        if min_d < min_dist:
            min_dist = min_d; j = np.argmin(dists); best_pair = (i, j)
    return best_pair

def stitch_contours_numpy(outer, inner):
    outer = np.array(outer).reshape(-1, 2)
    inner = np.array(inner).reshape(-1, 2)
    idx_out, idx_in = find_closest_points(outer, inner)
    new_inner = np.roll(inner, -idx_in, axis=0)
    p_out = outer[idx_out].reshape(1, 2)
    p_in = new_inner[0].reshape(1, 2)
    combined = np.concatenate((outer[:idx_out+1], new_inner, p_in, p_out, outer[idx_out+1:]))
    return combined

# ============================================================================
# GUI & LOGIC
# ============================================================================

def pil2pixmap(im):
    if im is None:
        return QPixmap()
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    data = im.tobytes("raw", "RGBA")
    qim = QImage(data, im.size[0], im.size[1], QImage.Format_RGBA8888)
    return QPixmap.fromImage(qim.copy())

def vectorize_logo(path, width_mm, thresh, invert, smooth):
    if not path:
        return []
    try:
        src = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if src is None:
            return []
        if len(src.shape)==3 and src.shape[2]==4:
            bg=255*np.ones_like(src[:,:,:3]); a=src[:,:,3:]/255.0
            src=(src[:,:,:3]*a + bg*(1-a)).astype(np.uint8)
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) if len(src.shape)==3 else src
        h,w = gray.shape; s=2000/max(h,w)
        gray = cv2.resize(gray, (int(w*s), int(h*s)), interpolation=cv2.INTER_LANCZOS4)
        type_ = cv2.THRESH_BINARY if invert else cv2.THRESH_BINARY_INV
        _, bi = cv2.threshold(gray, thresh, 255, type_)
        cnts, hier = cv2.findContours(bi, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        if not cnts:
            return []
        hier = hier[0]; p_map = {}
        for i, h in enumerate(hier):
            if h[3] == -1:
                p_map[i] = []
            elif h[3] in p_map:
                p_map[h[3]].append(i)
        scale_fac = width_mm / gray.shape[1]
        ox, oy = -(gray.shape[1]*scale_fac)/2, -(gray.shape[0]*scale_fac)/2
        res = []
        for pid, kids in p_map.items():
            poly = cv2.approxPolyDP(cnts[pid], smooth*cv2.arcLength(cnts[pid],True), True)
            poly_np = poly.reshape(-1, 2)
            for k in kids:
                pk = cv2.approxPolyDP(cnts[k], smooth*cv2.arcLength(cnts[k],True), True)
                pk_np = pk.reshape(-1, 2)
                poly_np = stitch_contours_numpy(poly_np, pk_np)
            pts = [(p[0]*scale_fac+ox, p[1]*scale_fac+oy) for p in poly_np]
            res.append(pts)
        return res
    except:
        return []

def export_kicad(polys, name, layer):
    ts = hex(int(time.time()))[2:].upper()
    lines = [f'(footprint "{name}" (layer "{layer}") (tedit {ts}) (generator python_qr_pro)',
             '  (attr board_only exclude_from_pos_files exclude_from_bom)']
    for p in polys:
        if len(p)<3: continue
        pts = " ".join([f"(xy {x:.4f} {y:.4f})" for x,y in p])
        lines.append(f'  (fp_poly (pts {pts}) (layer "{layer}") (width 0))')
    lines.append(")")
    return "\n".join(lines)

import math
import qrcode
import numpy as np
from shapely.geometry import box, Point, Polygon as ShapelyPoly, MultiPolygon
from shapely.ops import unary_union
from shapely.affinity import rotate, translate, scale

# ============================================================================
# GEOMETRY ENGINE
# ============================================================================

def get_superellipse_n(slider_val):
    if slider_val <= 50:
        return 0.8 + (slider_val / 50.0) * 1.2
    else:
        return 2.0 + ((slider_val - 50) / 50.0) * 6.0

def create_superellipse(center, w, h, n, points=64):
    pts = []
    if n < 0.1: n = 0.1
    if n > 50: n = 50 
    a = w / 2.0; b = h / 2.0
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
# CORE RENDERER
# ============================================================================

class QRRenderer:
    def __init__(self, content, ec=qrcode.constants.ERROR_CORRECT_H):
        self.qr = qrcode.QRCode(version=None, error_correction=ec, box_size=1, border=0)
        try:
            self.qr.add_data(content)
            self.qr.make(fit=True)
        except:
            pass
        self.matrix = self.qr.get_matrix()
        self.rows = len(self.matrix); self.cols = len(self.matrix[0])
        self.full_grid = {} 
        self.min_r, self.max_r = 0, self.rows
        self.min_c, self.max_c = 0, self.cols
        self.rotation_rad = 0.0

    def is_finder_module(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        if r < 7 and c < 7:
            return True
        if r < 7 and c >= self.cols - 7:
            return True
        if r >= self.rows - 7 and c < 7:
            return True
        return False

    def transform_vector(self, vx, vy):
        if self.rotation_rad == 0:
            return vx, vy
        cos_a = math.cos(self.rotation_rad)
        sin_a = math.sin(self.rotation_rad)
        rx = vx * cos_a - vy * sin_a
        ry = vx * sin_a + vy * cos_a
        return rx, ry

    def prepare_grid(self, global_shape, mod_size_mm, size_mm, noise_seed):
        self.full_grid = {}
        cx = (self.cols - 1) / 2.0
        cy = (self.rows - 1) / 2.0

        if global_shape == "Heart":
            self.rotation_rad = math.radians(45) 
        else:
            self.rotation_rad = 0.0

        # Real Data
        for r in range(self.rows):
            for c in range(self.cols):
                if self.matrix[r][c]:
                    self.full_grid[(r,c)] = True

        if global_shape == "Square":
            self.min_r, self.max_r = 0, self.rows
            self.min_c, self.max_c = 0, self.cols
            return

        # Fake Data Logic
        diag_modules = math.sqrt(self.rows**2 + self.cols**2)
        
        if global_shape == "Heart":
            R = self.cols / 2.0 
            R_sq = R**2
            pad = int(R) + 2
            self.min_r = -pad; self.max_r = self.rows
            self.min_c = -pad; self.max_c = self.cols
            # Centers in grid units
            self.heart_top_center_r = 0
            self.heart_top_center_c = R - 0.5
            self.heart_left_center_r = R - 0.5
            self.heart_left_center_c = 0
            
            for r in range(self.min_r, self.max_r):
                for c in range(self.min_c, self.max_c):
                    if 0 <= r < self.rows and 0 <= c < self.cols: 
                        continue
                    is_in_lobe = False
                    if r < 0:
                        if (r - self.heart_top_center_r)**2 + (c - self.heart_top_center_c)**2 <= R_sq:
                            is_in_lobe = True
                    if c < 0:
                        if (r - self.heart_left_center_r)**2 + (c - self.heart_left_center_c)**2 <= R_sq:
                            is_in_lobe = True
                    
                    if is_in_lobe:
                        s_r = r + 1000
                        s_c = c + 1000
                        seed = (s_r * 37 + s_c * 31337 + int(noise_seed)) ^ (s_r * s_c)
                        if (seed ^ (seed << 13)) % 100 < 45:
                            self.full_grid[(r,c)] = True

        elif global_shape == "Circle":
            scan_r = int(diag_modules * 0.65) + 2
            self.min_r = int(cy - scan_r); self.max_r = int(cy + scan_r)
            self.min_c = int(cx - scan_r); self.max_c = int(cx + scan_r)
            radius_real_sq = ((size_mm * math.sqrt(2) / 2.0) * 1.15)**2
            
            for r in range(self.min_r, self.max_r):
                for c in range(self.min_c, self.max_c):
                    if 0 <= r < self.rows and 0 <= c < self.cols:
                        continue
                    vx0 = (c - cx) * mod_size_mm
                    vy0 = (r - cy) * mod_size_mm
                    if vx0**2 + vy0**2 <= radius_real_sq:
                        s_r = r + 1000; s_c = c + 1000
                        seed = (s_r * 37 + s_c * 31337 + int(noise_seed)) ^ (s_r * s_c)
                        if (seed ^ (seed << 13)) % 100 < 40:
                            self.full_grid[(r,c)] = True

    def get_neighbors_extended(self, r, c):
        n = [False]*4
        n[0] = self.full_grid.get((r-1, c), False)
        n[1] = self.full_grid.get((r, c+1), False)
        n[2] = self.full_grid.get((r+1, c), False)
        n[3] = self.full_grid.get((r, c-1), False)
        return n

    def render_finder_pattern(self, r_center, c_center, mod_size, style, round_val, pivot_r, pivot_c):
        center_origin = Point(0,0)
        outer_sz = 7 * mod_size
        inner_void = 5 * mod_size
        dot_sz = 3 * mod_size
        
        if style == "Superellipse":
            n = get_superellipse_n(round_val)
            outer = create_superellipse(center_origin, outer_sz, outer_sz, n)
            void = create_superellipse(center_origin, inner_void, inner_void, n)
            dot = create_superellipse(center_origin, dot_sz, dot_sz, n)
        elif style == "Rounded":
            f = round_val / 100.0
            outer = create_squircle(center_origin, outer_sz, f * outer_sz / 2.0)
            void = create_squircle(center_origin, inner_void, f * inner_void / 2.0)
            dot = create_squircle(center_origin, dot_sz, f * dot_sz / 2.0)
        elif style == "Circle":
            outer = center_origin.buffer(outer_sz/2)
            void = center_origin.buffer(inner_void/2)
            dot = center_origin.buffer(dot_sz/2)
        elif style == "Diamond":
            # 1. Tạo hình vuông cơ bản (kích thước gốc 7, 5, 3)
            sq_outer = box(-outer_sz/2, -outer_sz/2, outer_sz/2, outer_sz/2)
            sq_void  = box(-inner_void/2, -inner_void/2, inner_void/2, inner_void/2)
            sq_dot   = box(-dot_sz/2, -dot_sz/2, dot_sz/2, dot_sz/2)
            
            # 2. Xoay 45 độ
            outer_rot = rotate(sq_outer, 45, origin=(0,0))
            void_rot  = rotate(sq_void, 45, origin=(0,0))
            dot_rot   = rotate(sq_dot, 45, origin=(0,0))

            # Tỷ lệ scale là 1 / sqrt(2) sắp xỉ 0.7071
            sf = 0.7071 
            outer = scale(outer_rot, xfact=sf, yfact=sf, origin=(0,0))
            void  = scale(void_rot, xfact=sf, yfact=sf, origin=(0,0))
            dot   = scale(dot_rot, xfact=sf, yfact=sf, origin=(0,0))
        else: # Square
            outer = box(-outer_sz/2, -outer_sz/2, outer_sz/2, outer_sz/2)
            void = box(-inner_void/2, -inner_void/2, inner_void/2, inner_void/2)
            dot = box(-dot_sz/2, -dot_sz/2, dot_sz/2, dot_sz/2)
            
        shape = unary_union([outer.difference(void), dot])
        
        if self.rotation_rad != 0:
            shape = rotate(shape, math.degrees(self.rotation_rad), origin=(0,0))
            
        vr_mm = (r_center - pivot_r) * mod_size
        vc_mm = (c_center - pivot_c) * mod_size
        tx, ty = self.transform_vector(vc_mm, vr_mm)
        return translate(shape, tx, ty)

    def render(self, size_mm, data_style, finder_style, round_find, round_data, module_scale, global_shape, noise_seed):
        mod_size_mm = size_mm / self.cols
        self.prepare_grid(global_shape, mod_size_mm, size_mm, noise_seed)
        
        pivot_r = (self.rows - 1) / 2.0
        pivot_c = (self.cols - 1) / 2.0

        # --- Calculate Debug Overlay ---
        debug_overlay = None
        if global_shape == "Circle":
            r_mm = (size_mm * math.sqrt(2) / 2.0) * 1.15
            debug_overlay = ("Circle", r_mm)
        elif global_shape == "Heart":
            R_mm = (self.cols / 2.0) * mod_size_mm
            vr_top = (self.heart_top_center_r - pivot_r) * mod_size_mm
            vc_top = (self.heart_top_center_c - pivot_c) * mod_size_mm
            tx_top, ty_top = self.transform_vector(vc_top, vr_top)
            vr_left = (self.heart_left_center_r - pivot_r) * mod_size_mm
            vc_left = (self.heart_left_center_c - pivot_c) * mod_size_mm
            tx_left, ty_left = self.transform_vector(vc_left, vr_left)
            debug_overlay = ("Heart", R_mm, (tx_top, ty_top), (tx_left, ty_left))
        # -------------------------------

        geoms = []
        eff_size = mod_size_mm * module_scale
        half_eff = eff_size / 2.0
        origin = Point(0,0)
        
        base_shape = None
        if data_style != "Liquid":
            try:
                if data_style == "Superellipse":
                    n = get_superellipse_n(round_data)
                    base_shape = create_superellipse(origin, eff_size, eff_size, n, points=32)
                elif data_style == "Rounded":
                    base_shape = create_squircle(origin, eff_size, (round_data/100.0)*half_eff)
                elif data_style == "Circle":
                    base_shape = origin.buffer(half_eff)
                elif data_style == "Diamond":
                    sq = box(-half_eff, -half_eff, half_eff, half_eff)
                    base_shape = rotate(sq, 45, origin=origin)
                else: 
                    base_shape = box(-half_eff, -half_eff, half_eff, half_eff)
            except:
                base_shape = box(-half_eff, -half_eff, half_eff, half_eff)

        for r in range(self.min_r, self.max_r):
            for c in range(self.min_c, self.max_c):
                if not self.full_grid.get((r, c), False):
                    continue
                if self.is_finder_module(r, c):
                    continue

                shape = None
                
                if data_style == "Liquid":
                    parts = [origin.buffer(half_eff)]
                    nbs = self.get_neighbors_extended(r, c)
                    bw = half_eff
                    if nbs[0] and not self.is_finder_module(r-1,c):
                        parts.append(box(-bw, -mod_size_mm, bw, 0)) 
                    if nbs[1] and not self.is_finder_module(r,c+1):
                        parts.append(box(0, -bw, mod_size_mm, bw)) 
                    if nbs[2] and not self.is_finder_module(r+1,c):
                        parts.append(box(-bw, 0, bw, mod_size_mm)) 
                    if nbs[3] and not self.is_finder_module(r,c-1):
                        parts.append(box(-mod_size_mm, -bw, 0, bw)) 
                    shape = unary_union(parts)
                else:
                    shape = base_shape

                if self.rotation_rad != 0 and data_style != "Circle":
                    shape = rotate(shape, math.degrees(self.rotation_rad), origin=(0,0))
                
                vr_mm = (r - pivot_r) * mod_size_mm
                vc_mm = (c - pivot_c) * mod_size_mm
                tx, ty = self.transform_vector(vc_mm, vr_mm)
                
                if shape and not shape.is_empty:
                    geoms.append(translate(shape, tx, ty))

        finders = []
        finders.append(self.render_finder_pattern(3.0, 3.0, mod_size_mm, finder_style, round_find, pivot_r, pivot_c))
        finders.append(self.render_finder_pattern(3.0, self.cols-3.0-1, mod_size_mm, finder_style, round_find, pivot_r, pivot_c))
        finders.append(self.render_finder_pattern(self.rows-3.0-1, 3.0, mod_size_mm, finder_style, round_find, pivot_r, pivot_c))

        final_list = []
        if geoms:
            valid_geoms = [g for g in geoms if g and not g.is_empty]
            if valid_geoms:
                merged_data = unary_union(valid_geoms)
                if data_style == "Liquid":
                    smooth_amount = eff_size * 0.3
                    merged_data = merged_data.buffer(smooth_amount).buffer(-smooth_amount).simplify(0.002)
                final_list.extend(self._geom_to_list(merged_data))
            
        for f in finders:
            if f and not f.is_empty:
                final_list.extend(self._geom_to_list(f))
        
        return final_list, mod_size_mm, debug_overlay

    def _geom_to_list(self, geom):
        polys_out = []
        if not geom or geom.is_empty: return []
        if isinstance(geom, ShapelyPoly):
            if len(geom.interiors) == 0:
                polys_out.append(list(geom.exterior.coords))
            else:
                ext_pts = np.array(geom.exterior.coords)
                current_poly = ext_pts
                for interior in geom.interiors:
                    int_pts = np.array(interior.coords)
                    current_poly = stitch_contours_numpy(current_poly, int_pts)
                polys_out.append(current_poly.tolist())
        elif isinstance(geom, MultiPolygon):
            for g in geom.geoms:
                polys_out.extend(self._geom_to_list(g))
        return polys_out

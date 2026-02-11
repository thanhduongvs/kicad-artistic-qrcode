from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtCore import Qt, QPointF

DEBUG_PREVIEW = 0

class PreviewWidget(QWidget):
    def __init__(self, p=None):
        super().__init__(p)
        self.polys = []
        self.overlay = None 
        self.bgCol = QColor("#2b2b2b") 
        self.fgCol = QColor("#F2EDA1")
        self.scale_factor = 1.0
        self.offset = QPointF(0, 0)
        self.is_dragging = False
        self.last_mouse_pos = QPointF()
        self.setCursor(Qt.OpenHandCursor)
        self.setMouseTracking(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_to_view()
        self.update()

    def set_color(self, color_code):
        self.fgCol = QColor(color_code)
        self.update()

    def update_data(self, p, overlay=None):
        self.polys = p
        self.overlay = overlay
        self.fit_to_view()
        self.update()

    def fit_to_view(self):
        if not self.polys:
            return
        allp = [pt for pl in self.polys for pt in pl]
        if not allp:
            return
        mnx = min(x for x,y in allp)
        mxx = max(x for x,y in allp)
        mny = min(y for x,y in allp)
        mxy = max(y for x,y in allp)
        w_qr = mxx - mnx; h_qr = mxy - mny
        if w_qr <= 0 or h_qr <= 0:
            return
        scale_w = (self.width()-40)/w_qr
        scale_h = (self.height()-40)/h_qr
        self.scale_factor = min(scale_w, scale_h)
        cx_qr = (mnx+mxx)/2
        cy_qr = (mny+mxy)/2
        self.offset = QPointF(
            self.width()/2 - cx_qr*self.scale_factor,
            self.height()/2 - cy_qr*self.scale_factor
        )

    def wheelEvent(self, e):
        f = 1.1 if e.angleDelta().y()>0 else 0.9
        self.scale_factor *= f
        self.offset = e.position() - (e.position() - self.offset) * f
        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.is_dragging=True
            self.last_mouse_pos=e.position()
            self.setCursor(Qt.ClosedHandCursor)
    def mouseMoveEvent(self, e):
        if self.is_dragging:
            self.offset += e.position()-self.last_mouse_pos
            self.last_mouse_pos=e.position()
            self.update()

    def mouseReleaseEvent(self, e):
        self.is_dragging=False
        self.setCursor(Qt.OpenHandCursor)

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.fillRect(self.rect(), self.bgCol)
        qp.translate(self.offset)
        qp.scale(self.scale_factor, self.scale_factor)
        
        # 1. Draw Polygons (QR)
        if self.polys:
            qp.setBrush(QBrush(self.fgCol))
            qp.setPen(Qt.NoPen)
            for pl in self.polys:
                qp.drawPolygon([QPointF(x,y) for x,y in pl])
            
        # 2. Draw Overlay (If exists)
        if DEBUG_PREVIEW and self.overlay:
            pen = QPen(QColor("#00FFFF"), 0)
            pen.setStyle(Qt.DashLine)
            qp.setPen(pen)
            qp.setBrush(Qt.NoBrush)

            if self.overlay[0] == "Circle":
                r = self.overlay[1]
                qp.drawEllipse(QPointF(0,0), r, r)
            elif self.overlay[0] == "Heart":
                r = self.overlay[1]
                c1 = self.overlay[2] # Top Lobe Center (x,y)
                c2 = self.overlay[3] # Left Lobe Center (x,y)
                qp.drawEllipse(QPointF(c1[0], c1[1]), r, r)
                qp.drawEllipse(QPointF(c2[0], c2[1]), r, r)
        qp.end()

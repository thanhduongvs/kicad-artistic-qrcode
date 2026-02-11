from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal

class ZoomableLabel(QLabel):
    zoomChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background: transparent;")

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            self.zoomChanged.emit(0.1)
        else:
            self.zoomChanged.emit(-0.1)
        event.accept()
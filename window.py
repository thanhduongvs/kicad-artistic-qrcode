from PySide6.QtWidgets import (
    QApplication, QMainWindow,
    QMessageBox, QFileDialog, QVBoxLayout
)
from PySide6.QtCore import QTimer
from gui import Ui_MainWindow
from preview_widget import PreviewWidget
from zoom_label import ZoomableLabel
from version import version
from qr_render import QRRenderer

from utils import (
    get_superellipse_n,pil2pixmap,
    vectorize_logo, export_kicad
)

from PIL import Image, ImageOps
from shapely.geometry import box, Point, Polygon as ShapelyPoly, MultiPolygon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f"QR Generator v{version}")

        self.polys = []
        self.logo_path = None
        self.logo_scale = 1.0
        self.need_fit_logo = False

        self.canvas = PreviewWidget()
        layout = QVBoxLayout(self.ui.groupBoxPreview)
        layout.setContentsMargins(10, 10, 10, 10) 
        layout.addWidget(self.canvas)


        self.preLogo = ZoomableLabel("Logo\nPreview")
        self.preLogo.zoomChanged.connect(self.change_logo_zoom)
        self.ui.scrollLogo.setWidgetResizable(True)
        self.ui.scrollLogo.setStyleSheet("border: 1px dashed #555; background: #333;")
        self.ui.scrollLogo.setWidget(self.preLogo)
       
        self.ui.lineEdit.setText("QR Generator")
        self.ui.comboLayer.addItems(["F.SilkS", "B.SilkS", "F.Cu", "B.Cu"])
        self.ui.comboGlobalShape.addItems(["Square", "Circle", "Heart"])
        self.ui.comboFinderStyle.addItems(["Square", "Circle", "Diamond", "Rounded", "Superellipse"])
        self.ui.comboDataStyle.addItems(["Square", "Circle", "Diamond", "Liquid", "Rounded", "Superellipse"])

        self.ui.sliderNoiseSeed.setEnabled(False)
        self.ui.spinNoiseSeed.setEnabled(False)
        self.ui.sliderFinderRound.setEnabled(False)
        self.ui.sliderDataRound.setEnabled(False)
        self.ui.spinFinderRound.setEnabled(False)
        self.ui.spinDataRound.setEnabled(False)
        
        self.ui.lineEdit.textChanged.connect(self.create_qr)
        self.ui.spinSizeQr.valueChanged.connect(self.create_qr)

        self.ui.comboLayer.currentIndexChanged.connect(self.update_layer_color)

        self.ui.comboGlobalShape.currentIndexChanged.connect(self.on_global_changed)
        
        self.ui.comboDataStyle.currentIndexChanged.connect(self.create_qr)
        self.ui.comboFinderStyle.currentIndexChanged.connect(self.update_labels)
        self.ui.comboFinderStyle.currentIndexChanged.connect(self.create_qr)
        self.ui.comboFinderStyle.currentIndexChanged.connect(self.on_finderstyle_changed)
        
        self.ui.sliderFinderRound.valueChanged.connect(self.on_finder_slide)
        self.ui.sliderFinderRound.valueChanged.connect(self.update_labels)
        self.ui.sliderFinderRound.valueChanged.connect(self.slider_finderround_changed)
        self.ui.spinFinderRound.valueChanged.connect(self.spin_finderround_changed)

        self.ui.sliderDataRound.valueChanged.connect(self.update_labels)
        self.ui.sliderDataRound.valueChanged.connect(self.create_qr)
        self.ui.sliderDataRound.valueChanged.connect(self.slider_dataround_changed)
        self.ui.spinDataRound.valueChanged.connect(self.spin_dataround_changed)

        self.ui.sliderModuleSize.valueChanged.connect(self.create_qr)
        self.ui.sliderModuleSize.valueChanged.connect(self.slider_modulesize_changed)
        self.ui.spinModuleSize.valueChanged.connect(self.spin_modulesize_changed)
        
        self.ui.sliderNoiseSeed.valueChanged.connect(self.update_labels)
        self.ui.sliderNoiseSeed.valueChanged.connect(self.create_qr)
        self.ui.sliderNoiseSeed.valueChanged.connect(self.slider_noiseseed_changed)
        self.ui.spinNoiseSeed.valueChanged.connect(self.spin_noiseseed_changed)
        
        
        self.ui.checkInvertLogo.toggled.connect(self.update_preview)
        self.ui.checkInvertLogo.toggled.connect(self.create_qr)
        self.ui.sliderSizeLogo.valueChanged.connect(self.create_qr)
        self.ui.sliderSizeLogo.valueChanged.connect(self.slider_sizelogo_changed)
        self.ui.spinSizeLogo.valueChanged.connect(self.spin_sizelogo_changed)
        
        self.ui.sliderThreshLogo.valueChanged.connect(self.update_preview)
        self.ui.sliderThreshLogo.valueChanged.connect(self.create_qr)
        self.ui.sliderThreshLogo.valueChanged.connect(self.slider_threshlogo_changed)
        self.ui.spinThreshLogo.valueChanged.connect(self.spin_threshlogo_changed)

        self.ui.checkLinkData.toggled.connect(self.on_linkdata_toggle)
        self.ui.buttonSelectLogo.clicked.connect(self.button_pick_logo_clicked)
        self.ui.buttonRemoveLogo.clicked.connect(self.button_remove_logo_clicked)
        self.ui.buttonClose.clicked.connect(self.button_close_clicked)
        self.ui.buttonSave.clicked.connect(self.button_save_clicked)
        self.ui.buttonCopy.clicked.connect(self.button_copy_clicked)

        self.update_layer_color()
        QTimer.singleShot(100, self.create_qr)
    
    def slider_finderround_changed(self):
        style = self.ui.comboFinderStyle.currentText()
        value = self.ui.sliderFinderRound.value()
        
        if style == "Superellipse":
            target_val = get_superellipse_n(value)
        else:
            target_val = float(value)
            
        self.ui.spinFinderRound.blockSignals(True)
        self.ui.spinFinderRound.setValue(target_val)
        self.ui.spinFinderRound.blockSignals(False)
    
    def spin_finderround_changed(self):
        style = self.ui.comboFinderStyle.currentText()
        value = self.ui.spinFinderRound.value()
        
        target_val = 0
        if style == "Superellipse":
            if value <= 2.0:
                target_val = int(round(((value - 0.8) / 1.2) * 50))
            else:
                target_val = int(round(((value - 2.0) / 6.0) * 50 + 50))
        else:
            target_val = int(value)
            
        #target_val = max(0, min(100, target_val))

        self.ui.sliderFinderRound.blockSignals(True)
        self.ui.sliderFinderRound.setValue(target_val)
        self.ui.labelFinderRound.setText(f"Finder Roundness (n={value:.2f})")
        self.ui.sliderFinderRound.blockSignals(False)

    def slider_dataround_changed(self):
        value = self.ui.sliderDataRound.value()
        self.ui.spinDataRound.setValue(value)
    
    def spin_dataround_changed(self):
        value = self.ui.spinDataRound.value()
        self.ui.sliderDataRound.setValue(value)

    def slider_modulesize_changed(self):
        value = self.ui.sliderModuleSize.value()
        self.ui.spinModuleSize.setValue(value)
    
    def spin_modulesize_changed(self):
        value = self.ui.spinModuleSize.value()
        self.ui.sliderModuleSize.setValue(value)

    def slider_noiseseed_changed(self):
        value = self.ui.sliderNoiseSeed.value()
        self.ui.spinNoiseSeed.setValue(value)
    
    def spin_noiseseed_changed(self):
        value = self.ui.spinNoiseSeed.value()
        self.ui.sliderNoiseSeed.setValue(value)

    def slider_sizelogo_changed(self):
        value = self.ui.sliderSizeLogo.value()
        self.ui.spinSizeLogo.setValue(value)

    def spin_sizelogo_changed(self):
        value = self.ui.spinSizeLogo.value()
        self.ui.sliderSizeLogo.setValue(value)

    def slider_threshlogo_changed(self):
        value = self.ui.sliderThreshLogo.value()
        self.ui.spinThreshLogo.setValue(value)
    
    def spin_threshlogo_changed(self):
        value = self.ui.spinThreshLogo.value()
        self.ui.sliderThreshLogo.setValue(value)

    def update_layer_color(self):
        layer = self.ui.comboLayer.currentText()
        # KiCad Colors mapping
        colors = {
            "F.SilkS": "#F5B041",
            "B.SilkS": "#E8B2A7",
            "F.Cu":    "#C83434",
            "B.Cu":    "#4D7FC4"
        }
        # Fallback color if not found
        col = colors.get(layer, "#F2EDA1")
        self.canvas.set_color(col)

    def change_logo_zoom(self, delta):
        self.logo_scale += delta
        if self.logo_scale < 0.1: self.logo_scale = 0.1
        if self.logo_scale > 10.0: self.logo_scale = 10.0
        self.update_preview()

    def on_global_changed(self):
        value = self.ui.comboGlobalShape.currentText()
        if value == "Square":
            self.ui.sliderNoiseSeed.setEnabled(False)
            self.ui.spinNoiseSeed.setEnabled(False)
        else:
            self.ui.sliderNoiseSeed.setEnabled(True)
            self.ui.spinNoiseSeed.setEnabled(True)
        self.create_qr()

    def on_linkdata_toggle(self):
        is_linked = self.ui.checkLinkData.isChecked()
        self.ui.sliderDataRound.setEnabled(not is_linked)
        self.ui.comboDataStyle.setEnabled(not is_linked)
        self.ui.spinDataRound.setEnabled(not is_linked)
        if is_linked:
            self.ui.sliderDataRound.setValue(self.ui.sliderFinderRound.value())
            self.ui.spinDataRound.setValue(self.ui.sliderFinderRound.value())
            self.ui.comboDataStyle.setCurrentText(self.ui.comboFinderStyle.currentText())
        self.create_qr()

    def on_finder_slide(self):
        if self.ui.checkLinkData.isChecked():
            self.ui.sliderDataRound.setValue(self.ui.sliderFinderRound.value())
        self.update_labels()
        self.create_qr()

    def on_finderstyle_changed(self):
        value = self.ui.comboFinderStyle.currentText()
        if value == "Superellipse":
            val_f = self.ui.sliderFinderRound.value()
            nf = get_superellipse_n(val_f)
            self.ui.spinFinderRound.setDecimals(2)
            self.ui.spinFinderRound.setRange(0.8, 8)
            self.ui.spinFinderRound.setSingleStep(0.01)
            self.ui.spinFinderRound.setValue(nf)
        else:
            val = self.ui.sliderFinderRound.value()
            self.ui.spinFinderRound.setDecimals(0)
            self.ui.spinFinderRound.setRange(0, 100)
            self.ui.spinFinderRound.setSingleStep(1)
            self.ui.spinFinderRound.setValue(val)

        if value in ["Square", "Circle", "Diamond"]:
            self.ui.sliderFinderRound.setEnabled(False)
            self.ui.sliderDataRound.setEnabled(False)
            self.ui.spinFinderRound.setEnabled(False)
            self.ui.spinDataRound.setEnabled(False)
        else:
            self.ui.sliderFinderRound.setEnabled(True)
            self.ui.sliderDataRound.setEnabled(True)
            self.ui.spinFinderRound.setEnabled(True)
            self.ui.spinDataRound.setEnabled(True)

    def update_labels(self):
        val_f = self.ui.sliderFinderRound.value()
        if "Superellipse" in self.ui.comboFinderStyle.currentText():
            nf = get_superellipse_n(val_f)
            self.ui.labelFinderRound.setText(f"Finder Roundness (n={nf:.2f})")
        else:
            self.ui.labelFinderRound.setText(f"Finder Roundness: {val_f}%")
        val_d = self.ui.sliderDataRound.value()
        if "Superellipse" in self.ui.comboDataStyle.currentText():
            nd = get_superellipse_n(val_d)
            self.ui.labelDataRound.setText(f"Data Roundness (n={nd:.2f})")
        else: 
            self.ui.labelDataRound.setText(f"Data Roundness: {val_d}%")
        self.ui.labelNoiseSeed.setText(f"Noise Seed: {self.ui.sliderNoiseSeed.value()}")
    

    def create_qr(self):
        try:
            rend = QRRenderer(self.ui.lineEdit.text())
            logo_w=0
            if self.logo_path:
                try: 
                    with Image.open(self.logo_path) as i:
                        w,h=i.size
                        logo_w=self.ui.spinSizeQr.value()*(self.ui.sliderSizeLogo.value()/100.0)
                except: pass
            
            d_style = self.ui.comboFinderStyle.currentText() if self.ui.checkLinkData.isChecked() else self.ui.comboDataStyle.currentText()
            
            # Receive Overlay info
            polys, ms, overlay = rend.render(
                self.ui.spinSizeQr.value(),
                d_style,
                self.ui.comboFinderStyle.currentText(), 
                self.ui.sliderFinderRound.value(),
                self.ui.sliderDataRound.value(), 
                self.ui.sliderModuleSize.value()/100.0,
                self.ui.comboGlobalShape.currentText(),
                self.ui.sliderNoiseSeed.value()
            )
            final = []
            if logo_w > 0:
                cut = box(-logo_w/2-0.2, -logo_w/2-0.2, logo_w/2+0.2, logo_w/2+0.2)
                for p in polys:
                    if not ShapelyPoly(p).intersects(cut):
                        final.append(p)
                final.extend(vectorize_logo(
                    self.logo_path,
                    logo_w, self.ui.sliderThreshLogo.value(),
                    self.ui.checkInvertLogo.isChecked(),
                    0.002)
                )
            else:
                final = polys
            self.polys = final
            # Pass overlay to view
            self.canvas.update_data(final, overlay)
        except Exception as e: print(e)

    def button_pick_logo_clicked(self):
        f,_=QFileDialog.getOpenFileName(self,"Img","","Img (*.png *.jpg)"); 
        if f:
            self.logo_path=f
            self.need_fit_logo = True
            self.update_preview()
            self.create_qr()
    
    # Update Preview with Zoom
    def update_preview(self):
        if not self.logo_path: return
        try:
            im = Image.open(self.logo_path).convert("RGBA")
            bg = Image.new("RGBA", im.size, (255, 255, 255))
            im = Image.alpha_composite(bg, im).convert("L")
            if self.ui.checkInvertLogo.isChecked(): 
                im = ImageOps.invert(im)
            im = im.point(lambda p: 255 if p > self.ui.sliderThreshLogo.value() else 0)
            
            # Logic Auto-Fit
            if self.need_fit_logo:
                # Lấy kích thước hiện tại của khung nhìn (Viewport)
                view_w = self.ui.scrollLogo.viewport().width()
                view_h = self.ui.scrollLogo.viewport().height()
                
                img_w, img_h = im.size
                
                # Tránh chia cho 0
                if img_w > 0 and img_h > 0 and view_w > 0 and view_h > 0:
                    # Tính tỷ lệ scale để ảnh vừa khít khung (trừ đi 10px padding cho đẹp)
                    scale_w = (view_w - 20) / img_w
                    scale_h = (view_h - 20) / img_h
                    
                    # Chọn tỷ lệ nhỏ hơn để đảm bảo ảnh lọt lòng hoàn toàn
                    self.logo_scale = min(scale_w, scale_h)
                else:
                    self.logo_scale = 1.0

                # Tắt cờ đi để lần sau zoom chuột không bị reset lại
                self.need_fit_logo = False

            # 3. Tính kích thước hiển thị dựa trên scale thực tế
            w_new = int(im.size[0] * self.logo_scale)
            h_new = int(im.size[1] * self.logo_scale)
            
            # Đảm bảo kích thước tối thiểu là 1px
            w_new = max(1, w_new)
            h_new = max(1, h_new)

            # 4. Hiển thị ảnh
            self.preLogo.setPixmap(pil2pixmap(im.resize((w_new, h_new), Image.NEAREST)))
            self.preLogo.adjustSize() 
            
        except Exception as e: print(f"Error updating preview: {e}")

    def button_copy_clicked(self):
        QApplication.clipboard().setText(export_kicad(self.polys, "QR", self.ui.comboLayer.currentText()))
        QMessageBox.information(self,"OK","Copied!")

    def button_save_clicked(self):
        f,_=QFileDialog.getSaveFileName(self,"Save","QR.kicad_mod","KiCad (*.kicad_mod)")
        if f:
            open(f,"w").write(export_kicad(self.polys, "QR", self.ui.comboLayer.currentText()))
            QMessageBox.information(self,"OK","Saved!")

    def button_remove_logo_clicked(self):
        self.logo_path = None
        self.preLogo.clear()
        self.preLogo.setText("Logo\nPreview")
        self.create_qr()

    def button_close_clicked(self):
        self.close()
    
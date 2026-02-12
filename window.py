from PySide6.QtWidgets import (
    QApplication, QMainWindow,
    QMessageBox, QFileDialog, QVBoxLayout
)
from PySide6.QtCore import QTimer, QEvent
from gui import Ui_MainWindow
from preview_widget import PreviewWidget
from zoom_label import ZoomableLabel
from version import version
from qr_render import QRRenderer

from utils import (
    pil2pixmap,
    vectorize_logo, export_kicad
)

from PIL import Image, ImageOps
from shapely.geometry import box, Point, Polygon as ShapelyPoly, MultiPolygon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f"Artistic QR Code Generator v{version}")

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

        self.ui.scrollLogo.installEventFilter(self)
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.apply_auto_fit)
       
        #self.ui.lineEdit.setText("Artistic QR Code Generator")
        self.ui.comboLayer.addItems(["F.SilkS", "B.SilkS", "F.Cu", "B.Cu"])
        self.ui.comboGlobalShape.addItems(["Square", "Circle", "Heart"])
        self.ui.comboFinderStyle.addItems(["Square", "Circle", "Diamond", "Rounded", "Superellipse"])
        self.ui.comboDataStyle.addItems(["Square", "Circle", "Diamond", "Liquid", "Rounded", "Superellipse"])

        self.ui.sliderNoiseSeed.setEnabled(False)
        self.ui.spinNoiseSeed.setEnabled(False)
        self.ui.sliderFinderRound.setEnabled(False)
        self.ui.spinFinderRound.setEnabled(False)
        self.ui.sliderDataRound.setEnabled(False)
        self.ui.spinDataRound.setEnabled(False)
        self.ui.checkLinkData.setEnabled(False)

        self.ui.lineEdit.textChanged.connect(self.update_preview_qr)
        self.ui.spinSizeQr.valueChanged.connect(self.update_preview_qr)

        self.ui.comboLayer.currentIndexChanged.connect(self.on_layer_changed)
        self.ui.comboGlobalShape.currentIndexChanged.connect(self.on_global_changed)
        self.ui.checkLinkData.toggled.connect(self.on_linkdata_toggle)
        self.ui.comboFinderStyle.currentIndexChanged.connect(self.on_finderstyle_changed)
        self.ui.comboDataStyle.currentIndexChanged.connect(self.on_datastyle_changed)

        self.ui.sliderFinderRound.valueChanged.connect(self.slider_finderround_changed)
        self.ui.spinFinderRound.valueChanged.connect(self.spin_finderround_changed)

        self.ui.sliderDataRound.valueChanged.connect(self.slider_dataround_changed)
        self.ui.spinDataRound.valueChanged.connect(self.spin_dataround_changed)

        self.ui.sliderModuleSize.valueChanged.connect(self.slider_modulesize_changed)
        self.ui.spinModuleSize.valueChanged.connect(self.spin_modulesize_changed)

        self.ui.sliderNoiseSeed.valueChanged.connect(self.slider_noiseseed_changed)
        self.ui.spinNoiseSeed.valueChanged.connect(self.spin_noiseseed_changed)

        self.ui.sliderSizeLogo.valueChanged.connect(self.slider_sizelogo_changed)
        self.ui.spinSizeLogo.valueChanged.connect(self.spin_sizelogo_changed)

        self.ui.sliderThreshLogo.valueChanged.connect(self.slider_threshlogo_changed)
        self.ui.spinThreshLogo.valueChanged.connect(self.spin_threshlogo_changed)

        self.ui.checkInvertLogo.toggled.connect(self.on_invert_toggle)

        self.ui.buttonSelectLogo.clicked.connect(self.button_select_logo_clicked)
        self.ui.buttonRemoveLogo.clicked.connect(self.button_remove_logo_clicked)
        self.ui.buttonClose.clicked.connect(self.button_close_clicked)
        self.ui.buttonSave.clicked.connect(self.button_save_clicked)
        self.ui.buttonCopy.clicked.connect(self.button_copy_clicked)

        self.on_layer_changed()
        QTimer.singleShot(100, self.update_preview_qr)

    #### slot
    def eventFilter(self, source, event):
        if source == self.ui.scrollLogo and event.type() == QEvent.Resize:
            if self.logo_path:
                self.resize_timer.start(100)
        return super().eventFilter(source, event)

    def apply_auto_fit(self):
        self.need_fit_logo = True
        self.update_preview_logo()

    def on_layer_changed(self):
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
    
    def on_global_changed(self):
        value = self.ui.comboGlobalShape.currentText()
        if value == "Square":
            self.ui.sliderNoiseSeed.setEnabled(False)
            self.ui.spinNoiseSeed.setEnabled(False)
        else:
            self.ui.sliderNoiseSeed.setEnabled(True)
            self.ui.spinNoiseSeed.setEnabled(True)
        self.update_preview_qr()

    def on_linkdata_toggle(self):
        linked = self.ui.checkLinkData.isChecked()
        if linked:
            style = self.ui.comboFinderStyle.currentText()
            slider = self.ui.sliderFinderRound.value()
            spin = self.ui.spinFinderRound.value()
            self.ui.sliderFinderRound.blockSignals(True)
            self.ui.comboDataStyle.setCurrentText(style)
            self.ui.sliderFinderRound.blockSignals(False)
            if style == "Superellipse":
                self.ui.labelDataRound.setText(f"Data Roundness: n=0.8")
                self.set_data_round_superellipse()
                self.ui.sliderDataRound.setValue(slider)
                self.ui.spinDataRound.setValue(spin)
            elif style == "Rounded":
                self.ui.labelDataRound.setText(f"Data Roundness: 0%")
                self.set_data_round_rounded()
                self.ui.sliderDataRound.setValue(slider)
                self.ui.spinDataRound.setValue(spin)
        self.ui.comboDataStyle.setEnabled(not linked)
        self.ui.sliderDataRound.setEnabled(not linked)
        self.ui.spinDataRound.setEnabled(not linked)
        self.update_preview_qr()
    
    def on_finderstyle_changed(self):
        value = self.ui.comboFinderStyle.currentText()
        linked = self.ui.checkLinkData.isChecked()
        if linked:
            self.ui.checkLinkData.setChecked(False)
        if value == "Superellipse":
            self.set_finder_round_superellipse()
            self.ui.sliderFinderRound.blockSignals(True)
            self.ui.spinFinderRound.blockSignals(True)
            self.ui.sliderFinderRound.setValue(8)
            self.ui.spinFinderRound.setValue(0.8)
            self.ui.labelFinderRound.setText(f"Finder Roundness: n=0.8")
            self.ui.sliderFinderRound.blockSignals(False)
            self.ui.spinFinderRound.blockSignals(False)
        elif value == "Rounded":
            self.set_finder_round_rounded()
            self.ui.sliderFinderRound.blockSignals(True)
            self.ui.spinFinderRound.blockSignals(True)
            self.ui.sliderFinderRound.setValue(0)
            self.ui.spinFinderRound.setValue(0)
            self.ui.labelFinderRound.setText(f"Finder Roundness: 0%")
            self.ui.sliderFinderRound.blockSignals(False)
            self.ui.spinFinderRound.blockSignals(False)
        else:
            self.ui.labelFinderRound.setText(f"Finder Roundness: Disable")

        check = value in ["Square", "Circle", "Diamond"]
        self.ui.sliderFinderRound.setEnabled(not check)
        self.ui.spinFinderRound.setEnabled(not check)
        self.ui.sliderDataRound.setEnabled(not check)
        self.ui.spinDataRound.setEnabled(not check)
        self.ui.checkLinkData.setEnabled(not check)
        self.update_preview_qr()
    
    def on_datastyle_changed(self):
        value = self.ui.comboDataStyle.currentText()
        if value == "Superellipse":
            self.set_data_round_superellipse()
            self.ui.sliderDataRound.blockSignals(True)
            self.ui.spinDataRound.blockSignals(True)
            self.ui.sliderDataRound.setValue(8)
            self.ui.spinDataRound.setValue(0.8)
            self.ui.labelDataRound.setText(f"Data Roundness: n=0.8")
            self.ui.sliderDataRound.blockSignals(False)
            self.ui.spinDataRound.blockSignals(False)
        elif value == "Rounded":
            self.set_data_round_rounded()
            self.ui.sliderDataRound.blockSignals(True)
            self.ui.spinDataRound.blockSignals(True)
            self.ui.sliderDataRound.setValue(0)
            self.ui.spinDataRound.setValue(0)
            self.ui.labelDataRound.setText(f"Data Roundness: 0%")
            self.ui.sliderDataRound.blockSignals(False)
            self.ui.spinDataRound.blockSignals(False)
        else:
            self.ui.labelDataRound.setText(f"Data Roundness: Disable")
        check = value in ["Square", "Circle", "Diamond", "Liquid"]
        self.ui.sliderDataRound.setEnabled(not check)
        self.ui.spinDataRound.setEnabled(not check)
        self.update_preview_qr()

    def slider_finderround_changed(self):
        style = self.ui.comboFinderStyle.currentText()
        value = self.ui.sliderFinderRound.value()
        linked = self.ui.checkLinkData.isChecked()
        
        if style == "Superellipse":
            target_val = value/10.0
            self.ui.labelFinderRound.setText(f"Finder Roundness: n={target_val:.1f}")
            if linked:
                self.ui.labelDataRound.setText(f"Data Roundness: n={target_val:.1f}")
        elif style == "Rounded":
            target_val = value
            self.ui.labelFinderRound.setText(f"Finder Roundness: {value}%")
            if linked:
                self.ui.labelDataRound.setText(f"Data Roundness: {value}%")
        self.ui.spinFinderRound.blockSignals(True)
        self.ui.spinFinderRound.setValue(target_val)
        self.ui.spinFinderRound.blockSignals(False)
        if linked:
            self.ui.sliderDataRound.blockSignals(True)
            self.ui.spinDataRound.blockSignals(True)
            self.ui.sliderDataRound.setValue(value)
            self.ui.spinDataRound.setValue(target_val)
            self.ui.sliderDataRound.blockSignals(False)
            self.ui.spinDataRound.blockSignals(False)
        self.update_preview_qr()
    
    def spin_finderround_changed(self):
        style = self.ui.comboFinderStyle.currentText()
        value = self.ui.spinFinderRound.value()
        linked = self.ui.checkLinkData.isChecked()
        
        target_val = 0
        if style == "Superellipse":
            target_val = int(10*value)
            self.ui.labelFinderRound.setText(f"Finder Roundness: n={value:.1f}")
            if linked:
                self.ui.labelDataRound.setText(f"Data Roundness: n={value:.1f}")
        else:
            target_val = int(value)
            self.ui.labelFinderRound.setText(f"Finder Roundness: {target_val}%")
            if linked:
                self.ui.labelDataRound.setText(f"Data Roundness: {target_val}%")
        self.ui.sliderFinderRound.blockSignals(True)
        self.ui.sliderFinderRound.setValue(target_val)
        self.ui.sliderFinderRound.blockSignals(False)
        if linked:
            self.ui.sliderDataRound.blockSignals(True)
            self.ui.spinDataRound.blockSignals(True)
            self.ui.sliderDataRound.setValue(target_val)
            self.ui.spinDataRound.setValue(value)
            self.ui.sliderDataRound.blockSignals(False)
            self.ui.spinDataRound.blockSignals(False)
        self.update_preview_qr()
    
    def slider_dataround_changed(self):
        style = self.ui.comboDataStyle.currentText()
        value = self.ui.sliderDataRound.value()
        
        if style == "Superellipse":
            target_val = value/10.0
            self.ui.labelDataRound.setText(f"Data Roundness: n={target_val:.1f}")
        else:
            target_val = value
            self.ui.labelDataRound.setText(f"Data Roundness: {value}%")
            
        self.ui.spinDataRound.blockSignals(True)
        self.ui.spinDataRound.setValue(target_val)
        self.ui.spinDataRound.blockSignals(False)
        self.update_preview_qr()
    
    def spin_dataround_changed(self):
        style = self.ui.comboDataStyle.currentText()
        value = self.ui.spinDataRound.value()
        
        target_val = 0
        if style == "Superellipse":
            target_val = int(10*value)
            self.ui.labelDataRound.setText(f"Data Roundness (n={value:.1f})")
        else:
            target_val = int(value)
            self.ui.labelDataRound.setText(f"Data Roundness: {target_val}%")
        
        self.ui.sliderDataRound.blockSignals(True)
        self.ui.sliderDataRound.setValue(target_val)
        self.ui.sliderDataRound.blockSignals(False)
        self.update_preview_qr()

    def slider_modulesize_changed(self):
        value = self.ui.sliderModuleSize.value()
        self.ui.spinModuleSize.blockSignals(True)
        self.ui.spinModuleSize.setValue(value)
        self.ui.spinModuleSize.blockSignals(False)
        self.update_preview_qr()
    
    def spin_modulesize_changed(self):
        value = self.ui.spinModuleSize.value()
        self.ui.sliderModuleSize.blockSignals(True)
        self.ui.sliderModuleSize.setValue(value)
        self.ui.sliderModuleSize.blockSignals(False)
        self.update_preview_qr()

    def slider_noiseseed_changed(self):
        value = self.ui.sliderNoiseSeed.value()
        self.ui.spinNoiseSeed.blockSignals(True)
        self.ui.spinNoiseSeed.setValue(value)
        self.ui.spinNoiseSeed.blockSignals(False)
        self.update_preview_qr()
    
    def spin_noiseseed_changed(self):
        value = self.ui.spinNoiseSeed.value()
        self.ui.sliderNoiseSeed.blockSignals(True)
        self.ui.sliderNoiseSeed.setValue(value)
        self.ui.sliderNoiseSeed.blockSignals(False)
        self.update_preview_qr()
    
    def slider_sizelogo_changed(self):
        value = self.ui.sliderSizeLogo.value()
        self.ui.spinSizeLogo.blockSignals(True)
        self.ui.spinSizeLogo.setValue(value)
        self.ui.spinSizeLogo.blockSignals(False)
        self.update_preview_qr()

    def spin_sizelogo_changed(self):
        value = self.ui.spinSizeLogo.value()
        self.ui.sliderSizeLogo.blockSignals(True)
        self.ui.sliderSizeLogo.setValue(value)
        self.ui.sliderSizeLogo.blockSignals(False)
        self.update_preview_qr()
    
    def slider_threshlogo_changed(self):
        value = self.ui.sliderThreshLogo.value()
        self.ui.spinThreshLogo.blockSignals(True)
        self.ui.spinThreshLogo.setValue(value)
        self.ui.spinThreshLogo.blockSignals(False)
        self.update_preview_logo()
        self.update_preview_qr()
    
    def spin_threshlogo_changed(self):
        value = self.ui.spinThreshLogo.value()
        self.ui.sliderThreshLogo.blockSignals(True)
        self.ui.sliderThreshLogo.setValue(value)
        self.ui.sliderThreshLogo.blockSignals(False)
        self.update_preview_logo()
        self.update_preview_qr()

    def on_invert_toggle(self):
        self.update_preview_logo()
        self.update_preview_qr()

    def button_select_logo_clicked(self):
        f,_=QFileDialog.getOpenFileName(self,"Img","","Img (*.png *.jpg)"); 
        if f:
            self.logo_path=f
            self.need_fit_logo = True
            self.update_preview_logo()
            self.update_preview_qr()
    
    def button_remove_logo_clicked(self):
        self.logo_path = None
        self.preLogo.clear()
        self.preLogo.setText("Logo\nPreview")
        self.update_preview_qr()
    
    def button_close_clicked(self):
        self.close()

    def button_save_clicked(self):
        f,_=QFileDialog.getSaveFileName(self,"Save","QR.kicad_mod","KiCad (*.kicad_mod)")
        if f:
            open(f,"w").write(export_kicad(self.polys, "QR", self.ui.comboLayer.currentText()))
            QMessageBox.information(self,"OK","Saved!")

    def button_copy_clicked(self):
        QApplication.clipboard().setText(export_kicad(self.polys, "QR", self.ui.comboLayer.currentText()))
        QMessageBox.information(self,"OK","Copied!")

    ########

    def set_finder_round_superellipse(self):
        self.ui.sliderFinderRound.setRange(8, 80)
        self.ui.spinFinderRound.setRange(0.8, 8.0)
        self.ui.spinFinderRound.setDecimals(1)
        self.ui.spinFinderRound.setSingleStep(0.1)
    
    def set_finder_round_rounded(self):
        self.ui.sliderFinderRound.setRange(0, 100)
        self.ui.spinFinderRound.setRange(0, 100)
        self.ui.spinFinderRound.setDecimals(0)
        self.ui.spinFinderRound.setSingleStep(1)

    def set_data_round_superellipse(self):
        self.ui.sliderDataRound.setRange(8, 80)
        self.ui.spinDataRound.setRange(0.8, 8.0)
        self.ui.spinDataRound.setDecimals(1)
        self.ui.spinDataRound.setSingleStep(0.1)
    
    def set_data_round_rounded(self):
        self.ui.sliderDataRound.setRange(0, 100)
        self.ui.spinDataRound.setRange(0, 100)
        self.ui.spinDataRound.setDecimals(0)
        self.ui.spinDataRound.setSingleStep(1)
    
    def change_logo_zoom(self, delta):
        self.logo_scale += delta
        if self.logo_scale < 0.1: self.logo_scale = 0.1
        if self.logo_scale > 10.0: self.logo_scale = 10.0
        self.update_preview_logo()

    def update_preview_qr(self):
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

    # Update Preview with Zoom
    def update_preview_logo(self):
        if not self.logo_path: return
        try:
            im = Image.open(self.logo_path).convert("RGBA")
            bg = Image.new("RGBA", im.size, (255, 255, 255))
            im = Image.alpha_composite(bg, im).convert("L")
            if self.ui.checkInvertLogo.isChecked(): 
                im = ImageOps.invert(im)
            im = im.point(lambda p: 255 if p > self.ui.sliderThreshLogo.value() else 0)
            
            # Auto-Fit Logic
            if self.need_fit_logo:
                # Get current viewport dimensions
                view_w = self.ui.scrollLogo.viewport().width()
                view_h = self.ui.scrollLogo.viewport().height()
                
                img_w, img_h = im.size
                
                # Avoid division by zero
                if img_w > 0 and img_h > 0 and view_w > 0 and view_h > 0:
                    # Calculate scale ratio to fit image within frame (subtract 10px padding for aesthetics)
                    scale_w = (view_w - 20) / img_w
                    scale_h = (view_h - 20) / img_h
                    
                    # Select the smaller ratio to ensure the image fits entirely
                    self.logo_scale = min(scale_w, scale_h)
                else:
                    self.logo_scale = 1.0

                # Disable flag so subsequent mouse zooms don't reset it
                self.need_fit_logo = False

            # 3. Calculate display dimensions based on actual scale
            w_new = int(im.size[0] * self.logo_scale)
            h_new = int(im.size[1] * self.logo_scale)
            
            # Ensure minimum size is 1px
            w_new = max(1, w_new)
            h_new = max(1, h_new)

            # 4. Display image
            self.preLogo.setPixmap(pil2pixmap(im.resize((w_new, h_new), Image.NEAREST)))
            self.preLogo.adjustSize() 
            
        except Exception as e: print(f"Error updating preview: {e}")

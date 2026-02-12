# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QSlider,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.labelContent = QLabel(self.centralwidget)
        self.labelContent.setObjectName(u"labelContent")

        self.horizontalLayout_4.addWidget(self.labelContent)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_4.addWidget(self.lineEdit)

        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.spinSizeQr = QDoubleSpinBox(self.centralwidget)
        self.spinSizeQr.setObjectName(u"spinSizeQr")
        self.spinSizeQr.setDecimals(1)
        self.spinSizeQr.setSingleStep(0.100000000000000)
        self.spinSizeQr.setValue(10.000000000000000)

        self.gridLayout_2.addWidget(self.spinSizeQr, 0, 1, 1, 1)

        self.comboGlobalShape = QComboBox(self.centralwidget)
        self.comboGlobalShape.setObjectName(u"comboGlobalShape")

        self.gridLayout_2.addWidget(self.comboGlobalShape, 1, 1, 1, 1)

        self.comboLayer = QComboBox(self.centralwidget)
        self.comboLayer.setObjectName(u"comboLayer")

        self.gridLayout_2.addWidget(self.comboLayer, 0, 3, 1, 1)

        self.labelGlobalShape = QLabel(self.centralwidget)
        self.labelGlobalShape.setObjectName(u"labelGlobalShape")

        self.gridLayout_2.addWidget(self.labelGlobalShape, 1, 0, 1, 1)

        self.labelDataStyle = QLabel(self.centralwidget)
        self.labelDataStyle.setObjectName(u"labelDataStyle")

        self.gridLayout_2.addWidget(self.labelDataStyle, 2, 2, 1, 1)

        self.comboDataStyle = QComboBox(self.centralwidget)
        self.comboDataStyle.setObjectName(u"comboDataStyle")

        self.gridLayout_2.addWidget(self.comboDataStyle, 2, 3, 1, 1)

        self.labelFinderStyle = QLabel(self.centralwidget)
        self.labelFinderStyle.setObjectName(u"labelFinderStyle")

        self.gridLayout_2.addWidget(self.labelFinderStyle, 2, 0, 1, 1)

        self.comboFinderStyle = QComboBox(self.centralwidget)
        self.comboFinderStyle.setObjectName(u"comboFinderStyle")

        self.gridLayout_2.addWidget(self.comboFinderStyle, 2, 1, 1, 1)

        self.labelSizeQr = QLabel(self.centralwidget)
        self.labelSizeQr.setObjectName(u"labelSizeQr")

        self.gridLayout_2.addWidget(self.labelSizeQr, 0, 0, 1, 1)

        self.labelLayer = QLabel(self.centralwidget)
        self.labelLayer.setObjectName(u"labelLayer")

        self.gridLayout_2.addWidget(self.labelLayer, 0, 2, 1, 1)

        self.checkLinkData = QCheckBox(self.centralwidget)
        self.checkLinkData.setObjectName(u"checkLinkData")

        self.gridLayout_2.addWidget(self.checkLinkData, 1, 2, 1, 2)

        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(3, 1)

        self.verticalLayout.addLayout(self.gridLayout_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelDataRound = QLabel(self.centralwidget)
        self.labelDataRound.setObjectName(u"labelDataRound")

        self.gridLayout.addWidget(self.labelDataRound, 1, 0, 1, 1)

        self.labelFinderRound = QLabel(self.centralwidget)
        self.labelFinderRound.setObjectName(u"labelFinderRound")

        self.gridLayout.addWidget(self.labelFinderRound, 0, 0, 1, 1)

        self.labelModuleSize = QLabel(self.centralwidget)
        self.labelModuleSize.setObjectName(u"labelModuleSize")

        self.gridLayout.addWidget(self.labelModuleSize, 2, 0, 1, 1)

        self.sliderFinderRound = QSlider(self.centralwidget)
        self.sliderFinderRound.setObjectName(u"sliderFinderRound")
        self.sliderFinderRound.setMaximum(100)
        self.sliderFinderRound.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout.addWidget(self.sliderFinderRound, 0, 1, 1, 1)

        self.spinFinderRound = QDoubleSpinBox(self.centralwidget)
        self.spinFinderRound.setObjectName(u"spinFinderRound")
        self.spinFinderRound.setDecimals(0)
        self.spinFinderRound.setSingleStep(1.000000000000000)

        self.gridLayout.addWidget(self.spinFinderRound, 0, 2, 1, 1)

        self.labelNoiseSeed = QLabel(self.centralwidget)
        self.labelNoiseSeed.setObjectName(u"labelNoiseSeed")

        self.gridLayout.addWidget(self.labelNoiseSeed, 3, 0, 1, 1)

        self.sliderDataRound = QSlider(self.centralwidget)
        self.sliderDataRound.setObjectName(u"sliderDataRound")
        self.sliderDataRound.setMaximum(100)
        self.sliderDataRound.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout.addWidget(self.sliderDataRound, 1, 1, 1, 1)

        self.sliderModuleSize = QSlider(self.centralwidget)
        self.sliderModuleSize.setObjectName(u"sliderModuleSize")
        self.sliderModuleSize.setMinimum(10)
        self.sliderModuleSize.setMaximum(100)
        self.sliderModuleSize.setValue(85)
        self.sliderModuleSize.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout.addWidget(self.sliderModuleSize, 2, 1, 1, 1)

        self.sliderNoiseSeed = QSlider(self.centralwidget)
        self.sliderNoiseSeed.setObjectName(u"sliderNoiseSeed")
        self.sliderNoiseSeed.setMaximum(500)
        self.sliderNoiseSeed.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout.addWidget(self.sliderNoiseSeed, 3, 1, 1, 1)

        self.spinDataRound = QDoubleSpinBox(self.centralwidget)
        self.spinDataRound.setObjectName(u"spinDataRound")
        self.spinDataRound.setDecimals(0)
        self.spinDataRound.setSingleStep(1.000000000000000)

        self.gridLayout.addWidget(self.spinDataRound, 1, 2, 1, 1)

        self.spinModuleSize = QDoubleSpinBox(self.centralwidget)
        self.spinModuleSize.setObjectName(u"spinModuleSize")
        self.spinModuleSize.setDecimals(0)
        self.spinModuleSize.setMinimum(10.000000000000000)
        self.spinModuleSize.setSingleStep(1.000000000000000)
        self.spinModuleSize.setValue(85.000000000000000)

        self.gridLayout.addWidget(self.spinModuleSize, 2, 2, 1, 1)

        self.spinNoiseSeed = QDoubleSpinBox(self.centralwidget)
        self.spinNoiseSeed.setObjectName(u"spinNoiseSeed")
        self.spinNoiseSeed.setDecimals(0)
        self.spinNoiseSeed.setMaximum(500.000000000000000)
        self.spinNoiseSeed.setSingleStep(1.000000000000000)

        self.gridLayout.addWidget(self.spinNoiseSeed, 3, 2, 1, 1)

        self.gridLayout.setColumnStretch(1, 3)
        self.gridLayout.setColumnStretch(2, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonSelectLogo = QPushButton(self.centralwidget)
        self.buttonSelectLogo.setObjectName(u"buttonSelectLogo")

        self.horizontalLayout.addWidget(self.buttonSelectLogo)

        self.buttonRemoveLogo = QPushButton(self.centralwidget)
        self.buttonRemoveLogo.setObjectName(u"buttonRemoveLogo")

        self.horizontalLayout.addWidget(self.buttonRemoveLogo)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.scrollLogo = QScrollArea(self.centralwidget)
        self.scrollLogo.setObjectName(u"scrollLogo")
        self.scrollLogo.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 360, 296))
        self.scrollLogo.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollLogo)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkInvertLogo = QCheckBox(self.centralwidget)
        self.checkInvertLogo.setObjectName(u"checkInvertLogo")

        self.horizontalLayout_2.addWidget(self.checkInvertLogo)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.labelScrollZoom = QLabel(self.centralwidget)
        self.labelScrollZoom.setObjectName(u"labelScrollZoom")

        self.horizontalLayout_2.addWidget(self.labelScrollZoom)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.labelSizeLogo = QLabel(self.centralwidget)
        self.labelSizeLogo.setObjectName(u"labelSizeLogo")

        self.gridLayout_4.addWidget(self.labelSizeLogo, 0, 0, 1, 1)

        self.sliderThreshLogo = QSlider(self.centralwidget)
        self.sliderThreshLogo.setObjectName(u"sliderThreshLogo")
        self.sliderThreshLogo.setMaximum(255)
        self.sliderThreshLogo.setValue(127)
        self.sliderThreshLogo.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_4.addWidget(self.sliderThreshLogo, 1, 1, 1, 1)

        self.spinThreshLogo = QDoubleSpinBox(self.centralwidget)
        self.spinThreshLogo.setObjectName(u"spinThreshLogo")
        self.spinThreshLogo.setDecimals(0)
        self.spinThreshLogo.setMaximum(255.000000000000000)
        self.spinThreshLogo.setValue(127.000000000000000)

        self.gridLayout_4.addWidget(self.spinThreshLogo, 1, 2, 1, 1)

        self.spinSizeLogo = QDoubleSpinBox(self.centralwidget)
        self.spinSizeLogo.setObjectName(u"spinSizeLogo")
        self.spinSizeLogo.setDecimals(0)
        self.spinSizeLogo.setMinimum(10.000000000000000)
        self.spinSizeLogo.setMaximum(45.000000000000000)
        self.spinSizeLogo.setValue(20.000000000000000)

        self.gridLayout_4.addWidget(self.spinSizeLogo, 0, 2, 1, 1)

        self.sliderSizeLogo = QSlider(self.centralwidget)
        self.sliderSizeLogo.setObjectName(u"sliderSizeLogo")
        self.sliderSizeLogo.setMinimum(10)
        self.sliderSizeLogo.setMaximum(45)
        self.sliderSizeLogo.setValue(20)
        self.sliderSizeLogo.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_4.addWidget(self.sliderSizeLogo, 0, 1, 1, 1)

        self.labelThreshLogo = QLabel(self.centralwidget)
        self.labelThreshLogo.setObjectName(u"labelThreshLogo")

        self.gridLayout_4.addWidget(self.labelThreshLogo, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_4)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.buttonClose = QPushButton(self.centralwidget)
        self.buttonClose.setObjectName(u"buttonClose")

        self.horizontalLayout_9.addWidget(self.buttonClose)

        self.buttonSave = QPushButton(self.centralwidget)
        self.buttonSave.setObjectName(u"buttonSave")

        self.horizontalLayout_9.addWidget(self.buttonSave)

        self.buttonCopy = QPushButton(self.centralwidget)
        self.buttonCopy.setObjectName(u"buttonCopy")

        self.horizontalLayout_9.addWidget(self.buttonCopy)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.verticalLayout.setStretch(4, 1)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.groupBoxPreview = QGroupBox(self.centralwidget)
        self.groupBoxPreview.setObjectName(u"groupBoxPreview")

        self.horizontalLayout_3.addWidget(self.groupBoxPreview)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)

        self.gridLayout_3.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 900, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.labelContent.setText(QCoreApplication.translate("MainWindow", u"Content:", None))
        self.labelGlobalShape.setText(QCoreApplication.translate("MainWindow", u"Global Shape:", None))
        self.labelDataStyle.setText(QCoreApplication.translate("MainWindow", u"Data Style:", None))
        self.labelFinderStyle.setText(QCoreApplication.translate("MainWindow", u"Finder Style:", None))
        self.labelSizeQr.setText(QCoreApplication.translate("MainWindow", u"Size (mm):", None))
        self.labelLayer.setText(QCoreApplication.translate("MainWindow", u"Layer:", None))
        self.checkLinkData.setText(QCoreApplication.translate("MainWindow", u"\U0001f517 Link Data to Finder", None))
        self.labelDataRound.setText(QCoreApplication.translate("MainWindow", u"Data Roundness: Disable", None))
        self.labelFinderRound.setText(QCoreApplication.translate("MainWindow", u"Finder Roundness: Disable", None))
        self.labelModuleSize.setText(QCoreApplication.translate("MainWindow", u"Module Size (10% - 100%):", None))
        self.labelNoiseSeed.setText(QCoreApplication.translate("MainWindow", u"Noise Seed (0 - 500):", None))
        self.buttonSelectLogo.setText(QCoreApplication.translate("MainWindow", u"Select Logo", None))
        self.buttonRemoveLogo.setText(QCoreApplication.translate("MainWindow", u"Remove Logo", None))
        self.checkInvertLogo.setText(QCoreApplication.translate("MainWindow", u"Invert", None))
        self.labelScrollZoom.setText(QCoreApplication.translate("MainWindow", u"Scroll mouse over image to Zoom", None))
        self.labelSizeLogo.setText(QCoreApplication.translate("MainWindow", u"Size  (10% - 45%):", None))
        self.labelThreshLogo.setText(QCoreApplication.translate("MainWindow", u"Thresh (0 - 255):", None))
        self.buttonClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.buttonSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.buttonCopy.setText(QCoreApplication.translate("MainWindow", u"Copy Clipboard", None))
        self.groupBoxPreview.setTitle(QCoreApplication.translate("MainWindow", u"Preview", None))
    # retranslateUi


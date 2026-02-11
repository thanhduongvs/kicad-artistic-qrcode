# QR Generator

# KiCad Artistic QR Code Generator

A powerful Python-based tool designed to generate artistic, vector-based QR codes specifically for **KiCad PCB designs**. 

Unlike standard QR generators that output raster images (PNG/JPG), this tool uses computational geometry (`Shapely`) to create precise **polygons** and exports them directly as **KiCad Footprint files (`.kicad_mod`)**. This allows you to place aesthetic, functional QR codes on your PCB's Silkscreen or Copper layers without quality loss.

![Preview Screenshot](https://via.placeholder.com/800x400?text=Insert+Application+Screenshot+Here)

## 🚀 Key Features

* **Vector-Based Generation**: Generates true geometry, not bitmaps. Perfect for manufacturing.
* **Artistic Styles**:
    * **Data Styles**: Liquid (blobby), Rounded, Superellipse, Circle, Square, Diamond.
    * **Finder Patterns**: Customize the 3 corner markers independently (e.g., Rounded, Diamond, Superellipse).
* **Global Shapes**:
    * **Square**: Standard QR code.
    * **Circle**: Crops the QR code into a circle (great for round PCBs).
    * **Heart**: Generates a heart-shaped QR code layout.
* **PCB Layer Support**:
    * Front/Back Silkscreen (`F.SilkS`, `B.SilkS`).
    * Front/Back Copper (`F.Cu`, `B.Cu`).
* **Logo Embedding**:
    * Import images (PNG/JPG).
    * **Auto-Vectorization**: Converts bitmap logos to vectors using OpenCV contours.
    * **Auto-Fit**: Automatically scales logos to fit the center.
    * **Smart Removal**: Clears data modules behind the logo to ensure readability.
* **Live Preview**: Real-time rendering with Zoom/Pan capabilities (powered by Qt).

## 🛠️ Installation

### Prerequisites
* Python 3.8+
* Pip

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/kicad-qr-generator.git](https://github.com/yourusername/kicad-qr-generator.git)
cd kicad-qr-generator
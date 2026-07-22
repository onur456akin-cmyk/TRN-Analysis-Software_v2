# TARGET RADIATED NOISE (TRN) ANALYSIS SOFTWARE

Professional acoustic analysis software for analyzing underwater ship noise recordings using hydrophone systems.

## 📋 Project Overview

This application is designed for:
- Military applications
- Academic research
- Scientific investigations
- Laboratory analysis processes

**Target Users**: Non-technical users who need professional TRN analysis without programming knowledge

## 🎯 Key Features

- **Multi-Format Support**: WAV, BIN, TXT file formats
- **Advanced Spectrum Analysis**: FFT, PSD, Peak Detection
- **TRN Calculation**: ANSI, ISO, Welch, FFT Average, RMS methods
- **Interactive Graphics**: Zoom, pan, sync, spectrum cursors
- **Integrated Audio Player**: Play, pause, speed control
- **Batch Processing**: Analyze multiple files simultaneously
- **Comparison Module**: Compare different recordings
- **Comprehensive Reporting**: PDF, Excel, CSV export
- **Multi-Language**: Turkish, English (expandable)
- **Dark/Light/High Contrast Themes**
- **Plugin Architecture**: Extensible framework for new algorithms

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

```bash
git clone https://github.com/onur456akin-cmyk/TRN-Analysis-Software_v2.git
cd TRN-Analysis-Software_v2
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

## 📦 Dependencies

- **PySide6** - GUI framework
- **NumPy** - Numerical computing
- **SciPy** - Scientific computing
- **Pandas** - Data processing
- **PyQtGraph** - Interactive plotting
- **Matplotlib** - Graphics
- **Sounddevice** - Audio playback
- **ReportLab** - PDF generation
- **openpyxl** - Excel export

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Module Specifications](docs/MODULES.md)
- [Mathematical Models](docs/MATHEMATICAL_MODELS.md)
- [API Documentation](docs/API.md)
- [User Guide](docs/USER_GUIDE.md)

## 🔧 Building Executable

```bash
python scripts/build_executable.py
```

## 📄 License

MIT License - see LICENSE file for details

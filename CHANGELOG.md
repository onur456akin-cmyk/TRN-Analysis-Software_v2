# CHANGELOG

## [0.1.0] - 2026-07-22

### Added
- Initial project structure and architecture
- Core modules:
  - FFT module for frequency domain analysis
  - PSD (Power Spectral Density) calculations
  - File Manager for WAV/BIN/TXT file I/O
  - Signal Processing utilities
  - Calibration module for hydrophone and amplifier compensation
  - Transmission Loss models (Spherical, Cylindrical, Practical)

- TRN Calculation Algorithms:
  - ANSI S1.4 method
  - ISO 20998 method
  - Welch PSD method
  - FFT Average method
  - RMS method

- Analysis Features:
  - Spectrum Analyzer with peak detection
  - Advanced peak detection capabilities
  - Batch processing for multiple files
  - Comparison module for multi-recording analysis

- GUI Application:
  - Main window with 3-panel layout
  - Parameter input panel
  - Analysis results display
  - Audio player integration

- Reporting & Export:
  - Report generator (HTML, TXT)
  - Export manager (CSV, TXT, Excel)
  - Result summarization

- Utilities:
  - Logging system
  - Data validation
  - Unit converters
  - Application constants

- Documentation:
  - README with quick start guide
  - Usage guide with examples
  - Project structure documentation

### Planned Features
- LOFAR Analysis
- DEMON Analysis (Detection of Envelope Modulation on Noise)
- Cepstrum Analysis
- Spectrogram/STFT Analysis
- Wavelet Analysis
- Beamforming
- Machine Learning Classification
- Real-time hydrophone streaming
- Database integration
- Advanced GUI improvements
- Multi-language support (German, French, Spanish, Japanese)
- Plugin system enhancements
- Automatic update system

### Known Limitations
- Audio playback requires sounddevice library
- Excel export requires openpyxl
- Large file processing may require optimization
- GUI still in development phase

## Future Versions

### [0.2.0] - Planned
- Enhanced GUI with matplotlib integration
- Spectrogram and STFT analysis
- Improved peak detection
- Database support

### [1.0.0] - Planned
- All core features complete
- Full documentation
- LOFAR and DEMON analysis
- Machine learning classification
- Production-ready executable

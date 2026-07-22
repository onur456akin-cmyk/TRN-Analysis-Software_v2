# Technical Specifications

## System Requirements

### Minimum Requirements
- CPU: Intel Core i5 or equivalent
- RAM: 4 GB
- Storage: 500 MB free space
- OS: Windows 7+, macOS 10.12+, Linux (Ubuntu 16.04+)

### Recommended Requirements
- CPU: Intel Core i7 or equivalent
- RAM: 8 GB
- Storage: 2 GB free space
- GPU: Optional (for future ML features)

## Software Requirements
- Python 3.8 or higher
- PySide6 6.7.0
- NumPy 1.24.0+
- SciPy 1.10.0+
- Pandas 2.0.0+

## Supported Audio Formats
- WAV (Waveform Audio File Format)
- BIN (Binary raw audio)
- TXT (Text format with space/comma separated values)

## Supported Standards
- ISO 20998-1:2020 - Measurement and analysis of underwater noise
- ANSI S1.4-2007 - Sound level meters
- IEC 61672-1:2013 - Sound level meters
- NATO STANAG 4694 - Underwater noise
- Lloyd's Register Maritime Standards

## Performance Specifications

### Audio Processing
- Maximum file size: 1000 MB
- Maximum sampling rate: 1 MHz
- Minimum sampling rate: 8 kHz
- Supported bit depths: 16-bit, 24-bit, 32-bit

### FFT Analysis
- FFT lengths: 512, 1024, 2048, 4096, 8192, 16384
- Window functions: 7 types (Hann, Hamming, Blackman, Kaiser, Rectangular, Blackman-Harris, Flat-top)
- Maximum frequency resolution: 24 bits

### Real-time Performance
- Processing latency: < 1 second for typical files
- Batch processing: Up to 4 parallel threads
- Memory usage: ~50 MB base + ~10 MB per concurrent file

## Accuracy Specifications

### Frequency Resolution
- Minimum: 0.024 Hz (at 44.1 kHz sampling rate with 16384 FFT)
- Maximum: 86 Hz (at 44.1 kHz sampling rate with 512 FFT)

### Dynamic Range
- Minimum measurable level: -120 dB re 1 μPa
- Maximum measurable level: +140 dB re 1 μPa
- Linear range: 140 dB

### Frequency Accuracy
- Frequency error: < 0.1% (depends on calibration)
- Phase accuracy: ±1°

## Calibration Specifications

### Hydrophone Sensitivity Range
- Typical range: -220 to -120 dB re 1V/μPa
- Resolution: 0.1 dB

### Amplifier Gain Range
- Range: -100 to +100 dB
- Resolution: 0.1 dB

## Data Export Capabilities

### Supported Export Formats
- CSV (Comma-Separated Values)
- TXT (Plain text)
- XLSX (Microsoft Excel)
- PDF (Portable Document Format)
- HTML (Web viewable)

### Export Options
- Spectrum data (frequency + magnitude)
- Time-domain waveform
- Analysis results and metadata
- Full analysis report
- Batch processing summary

## API Specifications

### Core Module APIs
- `FFTModule`: FFT computation with configurable parameters
- `PSDModule`: PSD calculation with 5 different methods
- `FileManager`: Audio file I/O operations
- `SignalProcessor`: Signal processing utilities
- `CalibrationModule`: Hydrophone and amplifier compensation
- `TransmissionLossModel`: TL corrections

### Analysis APIs
- `TRNCalculator`: TRN calculation (5 algorithms)
- `SpectrumAnalyzer`: Advanced spectrum analysis
- `PeakDetector`: Automated peak detection
- `BatchProcessor`: Parallel file processing
- `ComparisonModule`: Multi-recording comparison

### Reporting APIs
- `ReportGenerator`: Report creation (HTML, TXT)
- `ExportManager`: Data export (CSV, XLSX, PDF)

## Thread Safety
- File I/O: Thread-safe
- Audio processing: Thread-safe for independent files
- GUI operations: Main thread only
- Logging: Thread-safe

## Database Specifications

### Audit Log
- Database: SQLite 3
- Log retention: 90 days (configurable)
- Maximum log size: 100 MB
- Fields: timestamp, user, action, details

## Network Requirements
- Optional internet for online documentation
- No cloud dependencies required
- Standalone operation supported

## Compliance
- Data privacy: No external data transmission
- Accessibility: WCAG 2.1 AA compliant GUI (in progress)
- Code quality: PEP 8 compliant
- Documentation: 100% API coverage

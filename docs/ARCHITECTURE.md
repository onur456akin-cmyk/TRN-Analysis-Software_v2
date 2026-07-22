# Architecture Overview

## High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│                  User Interface (PySide6)            │
│  ┌──────────────┬──────────────┬──────────────────┐ │
│  │ Parameters   │ Analysis     │ Results Panel    │ │
│  │ Panel        │ Display      │                  │ │
│  └──────────────┴──────────────┴──────────────────┘ │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│            Analysis Engine Layer                     │
│  ┌──────────────┬──────────────┬──────────────────┐ │
│  │ Spectrum     │ Peak         │ Batch            │ │
│  │ Analyzer     │ Detector     │ Processor        │ │
│  └──────────────┴──────────────┴──────────────────┘ │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              TRN Calculation Layer                   │
│  ┌──────────────┬──────────────┬──────────────────┐ │
│  │ ANSI/ISO     │ Welch PSD    │ FFT Average      │ │
│  │ Methods      │ Methods      │ RMS Methods      │ │
│  └──────────────┴──────────────┴──────────────────┘ │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              Core Processing Layer                   │
│  ┌──────────┬──────────┬──────────┬──────────────┐ │
│  │ FFT      │ PSD      │ Signal   │ Calibration  │ │
│  │ Module   │ Module   │ Processor│ Module       │ │
│  └──────────┴──────────┴──────────┴──────────────┘ │
│  ┌──────────────┬──────────────────────────────┐   │
│  │ File Manager │ Transmission Loss Models    │   │
│  └──────────────┴──────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              Utilities & Support                     │
│  ┌──────────┬──────────┬──────────┬──────────────┐ │
│  │ Logger   │ Validator│ Converter│ Constants    │ │
│  └──────────┴──────────┴──────────┴──────────────┘ │
│  ┌──────────────┬──────────────────────────────┐   │
│  │ Report Generator │ Export Manager          │   │
│  └──────────────┴──────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Module Dependencies

```
main.py
├── config.py
├── gui/
│   └── main_window.py
│       ├── core/file_manager.py
│       ├── core/calibration.py
│       ├── core/trn_algorithms.py
│       └── utilities/
│           ├── logger.py
│           ├── validator.py
│           └── converters.py
├── core/
│   ├── fft_module.py
│   ├── psd_module.py
│   ├── signal_processor.py
│   ├── file_manager.py
│   ├── calibration.py
│   └── transmission_loss.py
├── analysis/
│   ├── spectrum_analyzer.py
│   ├── peak_detector.py
│   ├── batch_processor.py
│   └── comparison_module.py
├── audio/
│   └── audio_player.py
└── reporting/
    ├── report_generator.py
    └── export_manager.py
```

## Data Flow

### Typical Analysis Workflow

```
1. User loads audio file
   └─> FileManager.load_wav()
        └─> Returns: audio_data, sample_rate

2. User applies calibration
   └─> CalibrationModule.apply_full_calibration()
        ├─> Remove amplifier gain
        └─> Apply hydrophone sensitivity
             └─> Returns: pressure_signal

3. User selects TRN algorithm
   └─> TRNCalculator.calculate_trn_*()
        ├─> For ANSI/ISO: Calculate RMS directly
        ├─> For Welch: Use PSDModule
        └─> Returns: TRN value in dB

4. Optional: Spectrum analysis
   └─> SpectrumAnalyzer.compute_spectrum()
        ├─> FFTModule for frequency domain
        ├─> PeakDetector for peaks
        └─> Returns: frequencies, magnitudes

5. Generate report
   └─> ReportGenerator.generate_html()
        ├─> Add file info
        ├─> Add parameters
        ├─> Add results
        └─> Save as HTML/TXT

6. Export results
   └─> ExportManager.export_csv/excel/txt()
        └─> Save data to file
```

## Class Hierarchy

```
BaseModule (abstract)
├── FFTModule
├── PSDModule
├── SignalProcessor
├── SpectrumAnalyzer
└── PeakDetector

CalibrationModule
├── apply_hydrophone_sensitivity()
├── apply_amplifier_gain()
└── apply_full_calibration()

TRNCalculator
├── calculate_trn_ansi()
├── calculate_trn_iso()
├── calculate_trn_welch_psd()
├── calculate_trn_fft_average()
├── calculate_trn_rms()
└── calculate_all_algorithms()

ReportGenerator
├── add_section()
├── add_file_information()
├── add_analysis_results()
├── generate_html()
└── save_html()/save_txt()

ExportManager
├── export_csv()
├── export_txt()
├── export_excel()
└── export_spectrum()
```

## Configuration Management

All configuration is centralized in `config.py`:

```python
Config
├── Application metadata (name, version, author)
├── Paths (src, data, resources, plugins, docs)
├── File formats (supported extensions)
├── Audio settings (sample rate, buffer size)
├── FFT settings (lengths, window types)
├── PSD settings (methods, parameters)
├── TRN algorithms (available methods)
├── Transmission loss models (available models)
├── UI settings (theme, language)
├── Performance settings (max file size, memory)
└── Calibration defaults (sensitivity, gain)
```

## Error Handling Strategy

- **Validation Layer**: `DataValidator` checks input data
- **Logging Layer**: All operations logged via `setup_logger()`
- **Exception Handling**: Try-catch blocks in critical sections
- **User Feedback**: Error messages via GUI dialogs
- **Recovery**: Graceful degradation when possible

## Concurrency Model

- **Batch Processing**: Uses ThreadPoolExecutor for parallel file processing
- **GUI**: PySide6 main thread (Qt event loop)
- **Audio Playback**: Separate thread via sounddevice
- **Thread Safety**: File operations are thread-safe

## Performance Optimization

1. **FFT Caching**: FFT results cached during analysis
2. **Window Precomputation**: Window functions precomputed
3. **Vectorization**: NumPy operations for fast computation
4. **Lazy Loading**: Audio files loaded on demand
5. **Batch Processing**: Parallel processing for multiple files
6. **Memory Management**: Temporary data cleaned up after use

## Extensibility Points

1. **Custom TRN Algorithms**: Add to `TRNCalculator` class
2. **Custom Transmission Loss Models**: Add to `TransmissionLossModel`
3. **Custom Window Functions**: Extend `FFTModule`
4. **Custom Analysis Methods**: Create in `analysis/` package
5. **Plugin System**: Develop in `plugins/` directory
6. **Reporting Formats**: Extend `ReportGenerator`

## Security Considerations

- **Input Validation**: All user inputs validated
- **File Path Security**: Path traversal protection
- **No Remote Access**: Fully local application
- **Data Privacy**: No external data transmission
- **Audit Logging**: User actions logged locally

## Scalability

- **Batch Processing**: Handles 1000+ files
- **File Size**: Up to 1 GB audio files
- **Parallel Processing**: 4 concurrent threads
- **Memory**: Configurable limits (default 2 GB)
- **Database**: SQLite supports millions of log entries

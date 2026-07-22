"""Documentation and examples"""

# GETTING STARTED GUIDE

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

### 1. Load Audio File

```python
from src.core.file_manager import FileManager
from pathlib import Path

file_path = Path("path/to/audio.wav")
audio_data, sample_rate = FileManager.load_wav(file_path)
```

### 2. Apply Calibration

```python
from src.core.calibration import CalibrationModule

sensitivity_db = -170  # dB re 1V/µPa
amplifier_gain_db = 20  # dB

pressure_signal = CalibrationModule.apply_full_calibration(
    audio_data, sensitivity_db, amplifier_gain_db
)
```

### 3. Calculate TRN

```python
from src.core.trn_algorithms import TRNCalculator

# Method 1: ANSI
trn_ansi = TRNCalculator.calculate_trn_ansi(pressure_signal, sample_rate)

# Method 2: Welch PSD
trn_welch, frequencies, psd = TRNCalculator.calculate_trn_welch_psd(
    pressure_signal, sample_rate
)

# Method 3: All algorithms
all_results = TRNCalculator.calculate_all_algorithms(
    pressure_signal, sample_rate
)
for algo, value in all_results.items():
    print(f"{algo}: {value:.2f} dB")
```

### 4. Spectrum Analysis

```python
from src.analysis.spectrum_analyzer import SpectrumAnalyzer

analyzer = SpectrumAnalyzer(fft_length=2048, window="hann")
frequencies, magnitude_db = analyzer.compute_spectrum(pressure_signal, sample_rate)

# Find dominant frequency
dom_freq, dom_mag = analyzer.find_dominant_frequency(magnitude_db, frequencies)
print(f"Dominant frequency: {dom_freq:.2f} Hz at {dom_mag:.2f} dB")
```

### 5. Peak Detection

```python
from src.analysis.peak_detector import PeakDetector

detector = PeakDetector()
peaks = detector.detect(
    magnitude_db, frequencies,
    min_height=-40,
    min_distance=10,
    min_prominence=3.0
)

top_peaks = detector.get_top_peaks(peaks, count=10)
for peak in top_peaks:
    print(f"Frequency: {peak['frequency']:.2f} Hz, Magnitude: {peak['magnitude_db']:.2f} dB")
```

### 6. Batch Processing

```python
from src.analysis.batch_processor import BatchProcessor
from pathlib import Path

batch = BatchProcessor(max_workers=4)

def process_file(file_path):
    # Load and analyze file
    audio_data, sr = FileManager.load_wav(file_path)
    pressure = CalibrationModule.apply_full_calibration(audio_data, -170, 0)
    return TRNCalculator.calculate_trn_ansi(pressure, sr)

results = batch.process_directory(
    Path("./audio_files"),
    file_pattern="*.wav",
    process_func=process_file,
    recursive=True
)

print(f"Processed {results['successful']} files successfully")
print(f"Failed: {results['failed']}")
```

### 7. Generate Report

```python
from src.reporting.report_generator import ReportGenerator
from pathlib import Path

report = ReportGenerator("TRN Analysis Report")

report.add_file_information(
    str(file_path),
    sample_rate=sample_rate,
    duration=len(audio_data) / sample_rate,
    file_size_mb=file_path.stat().st_size / (1024**2)
)

report.add_parameters({
    'Hydrophone Sensitivity': f"{sensitivity_db} dB",
    'Amplifier Gain': f"{amplifier_gain_db} dB",
    'Algorithm': 'ANSI S1.4'
})

report.add_analysis_results({
    'TRN': f"{trn_ansi:.2f} dB",
    'Dominant Frequency': f"{dom_freq:.2f} Hz",
    'Number of Peaks': len(peaks)
})

report.save_html(Path("report.html"))
report.save_txt(Path("report.txt"))
```

### 8. Export Results

```python
from src.reporting.export_manager import ExportManager

# Export spectrum
ExportManager.export_spectrum(
    Path("spectrum.csv"),
    frequencies, magnitude_db,
    format="csv"
)

# Export custom data
data = {
    'frequencies': frequencies,
    'magnitude': magnitude_db
}
metadata = {
    'File': 'audio.wav',
    'Algorithm': 'ANSI',
    'TRN': f"{trn_ansi:.2f} dB"
}

ExportManager.export_csv(Path("results.csv"), data, metadata)
ExportManager.export_excel(Path("results.xlsx"), data, metadata)
```

## Running the GUI Application

```bash
python src/main.py
```

## Command Line Usage

```bash
# Process single file
python -m src.main path/to/audio.wav --algorithm ANSI --sensitivity -170

# Batch processing
python -m src.main --batch /path/to/audio/directory --recursive
```

## Advanced Topics

### Custom TRN Algorithm

Create a custom TRN calculation method:

```python
class MyCustomTRN:
    @staticmethod
    def calculate(pressure_signal, fs):
        # Your custom implementation
        rms = np.sqrt(np.mean(pressure_signal**2))
        return 20 * np.log10(rms / 1e-6)

# Add to TRN Calculator
TRNCalculator.calculate_trn_custom = MyCustomTRN.calculate
```

### Custom Transmission Loss Model

```python
from src.core.transmission_loss import TransmissionLossModel

# Define custom model
def custom_tl_model(distance, **kwargs):
    # Your custom TL calculation
    return 20 * np.log10(distance) + 0.01 * distance

# Use in analysis
tl = custom_tl_model(1000)
```

### Extending with Plugins

Create a plugin in `plugins/my_plugin/`:

```python
# plugins/my_plugin/__init__.py
from src.plugins.base_plugin import BasePlugin

class MyPlugin(BasePlugin):
    name = "My Analysis Plugin"
    version = "1.0.0"
    
    def execute(self, signal_data, fs):
        # Your analysis code
        return results
```

## Troubleshooting

### Audio playback not working
- Install sounddevice: `pip install sounddevice`
- Check audio device: `python -c "import sounddevice; print(sounddevice.query_devices())"`

### Import errors
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python version (3.8+)

### Memory issues with large files
- Use batch processing with smaller chunk sizes
- Enable memory optimization in config

## Performance Tips

1. Use appropriate FFT length (2048-4096 for most cases)
2. Enable zero padding for better frequency resolution
3. Use Welch method for noisy data
4. Process files in batch for efficiency
5. Reduce overlap for faster analysis

## More Information

- [GitHub Repository](https://github.com/onur456akin-cmyk/TRN-Analysis-Software_v2)
- [Technical Documentation](../docs/TECHNICAL_SPECS.md)
- [API Reference](../docs/API.md)
- [Mathematical Models](../docs/MATHEMATICAL_MODELS.md)

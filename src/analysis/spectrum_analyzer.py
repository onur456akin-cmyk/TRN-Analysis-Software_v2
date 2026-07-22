"""Spectrum Analyzer Module"""

import numpy as np
from typing import Tuple, Dict, List
import logging
from scipy import signal as scipy_signal

logger = logging.getLogger(__name__)


class SpectrumAnalyzer:
    """Advanced spectrum analysis capabilities"""
    
    def __init__(self, fft_length: int = 2048, window: str = "hann"):
        """
        Initialize spectrum analyzer
        
        Args:
            fft_length: FFT length
            window: Window type
        """
        self.fft_length = fft_length
        self.window = window
    
    def compute_spectrum(self, signal_data: np.ndarray, fs: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute frequency spectrum
        
        Args:
            signal_data: Input signal
            fs: Sampling frequency
            
        Returns:
            frequencies: Frequency axis
            magnitude_db: Magnitude spectrum in dB
        """
        # Pad signal
        if len(signal_data) < self.fft_length:
            signal_data = np.pad(signal_data, (0, self.fft_length - len(signal_data)))
        else:
            signal_data = signal_data[:self.fft_length]
        
        # Apply window
        window_func = scipy_signal.get_window(self.window, self.fft_length)
        windowed = signal_data * window_func
        
        # Compute FFT
        fft_result = np.fft.fft(windowed, self.fft_length)
        magnitude = np.abs(fft_result[:self.fft_length // 2])
        
        # Normalize
        magnitude = magnitude / (self.fft_length / 2)
        magnitude[0] = magnitude[0] / 2
        
        # Convert to dB
        magnitude_db = 20 * np.log10(magnitude + 1e-10)
        
        # Frequency axis
        frequencies = np.fft.fftfreq(self.fft_length, 1/fs)[:self.fft_length // 2]
        
        return frequencies, magnitude_db
    
    def detect_peaks(self, magnitude_db: np.ndarray, frequencies: np.ndarray,
                    height: float = -40, distance: int = 10,
                    prominence: float = 3.0) -> Dict:
        """
        Detect peaks in spectrum
        
        Args:
            magnitude_db: Magnitude spectrum in dB
            frequencies: Frequency axis
            height: Minimum peak height (dB)
            distance: Minimum distance between peaks (samples)
            prominence: Minimum peak prominence (dB)
            
        Returns:
            Dictionary with peak information
        """
        peaks, properties = scipy_signal.find_peaks(
            magnitude_db,
            height=height,
            distance=distance,
            prominence=prominence
        )
        
        peak_info = {
            'indices': peaks,
            'frequencies': frequencies[peaks],
            'magnitudes': magnitude_db[peaks],
            'prominences': properties['prominences'],
            'count': len(peaks)
        }
        
        logger.info(f"Detected {len(peaks)} peaks")
        return peak_info
    
    def find_dominant_frequency(self, magnitude_db: np.ndarray, 
                               frequencies: np.ndarray) -> Tuple[float, float]:
        """
        Find dominant frequency in spectrum
        
        Args:
            magnitude_db: Magnitude spectrum in dB
            frequencies: Frequency axis
            
        Returns:
            frequency: Dominant frequency
            magnitude: Magnitude at dominant frequency
        """
        max_idx = np.argmax(magnitude_db)
        return frequencies[max_idx], magnitude_db[max_idx]
    
    def compute_bandwidth(self, magnitude_db: np.ndarray, frequencies: np.ndarray,
                         peak_frequency: float) -> float:
        """
        Compute -3dB bandwidth around a frequency
        
        Args:
            magnitude_db: Magnitude spectrum in dB
            frequencies: Frequency axis
            peak_frequency: Center frequency
            
        Returns:
            Bandwidth in Hz
        """
        # Find peak index
        peak_idx = np.argmin(np.abs(frequencies - peak_frequency))
        peak_magnitude = magnitude_db[peak_idx]
        threshold = peak_magnitude - 3
        
        # Find -3dB points
        above_threshold = np.where(magnitude_db >= threshold)[0]
        
        if len(above_threshold) == 0:
            return 0.0
        
        lower_idx = above_threshold[0]
        upper_idx = above_threshold[-1]
        
        bandwidth = frequencies[upper_idx] - frequencies[lower_idx]
        return bandwidth
    
    def compute_spectral_centroid(self, magnitude: np.ndarray, 
                                 frequencies: np.ndarray) -> float:
        """
        Compute spectral centroid
        
        Args:
            magnitude: Magnitude spectrum (linear)
            frequencies: Frequency axis
            
        Returns:
            Spectral centroid frequency
        """
        if np.sum(magnitude) == 0:
            return 0.0
        return np.sum(frequencies * magnitude) / np.sum(magnitude)
    
    def compute_spectral_spread(self, magnitude: np.ndarray,
                               frequencies: np.ndarray) -> float:
        """
        Compute spectral spread (standard deviation)
        
        Args:
            magnitude: Magnitude spectrum (linear)
            frequencies: Frequency axis
            
        Returns:
            Spectral spread
        """
        centroid = self.compute_spectral_centroid(magnitude, frequencies)
        if np.sum(magnitude) == 0:
            return 0.0
        return np.sqrt(np.sum((frequencies - centroid) ** 2 * magnitude) / np.sum(magnitude))


if __name__ == "__main__":
    print("Spectrum Analyzer module loaded")

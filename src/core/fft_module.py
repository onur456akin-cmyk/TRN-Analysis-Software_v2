"""FFT Module for frequency domain analysis"""

import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import get_window
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class FFTModule:
    """Fast Fourier Transform calculations"""
    
    def __init__(self, fft_length: int = 2048, window: str = "hann", overlap: float = 0.5):
        """
        Initialize FFT module
        
        Args:
            fft_length: Length of FFT (power of 2 for efficiency)
            window: Window function type
            overlap: Overlap ratio (0.0 to 0.95)
        """
        self.fft_length = fft_length
        self.window_type = window
        self.overlap = overlap
        self.window = self._create_window()
        logger.info(f"FFT Module initialized: length={fft_length}, window={window}, overlap={overlap}")
    
    def _create_window(self) -> np.ndarray:
        """Create window function"""
        return get_window(self.window_type, self.fft_length)
    
    def set_window(self, window_type: str) -> None:
        """Change window type"""
        valid_windows = ["hann", "hamming", "blackman", "kaiser", "rectangular", "blackman-harris", "flat-top"]
        if window_type not in valid_windows:
            raise ValueError(f"Invalid window type. Must be one of {valid_windows}")
        self.window_type = window_type
        self.window = self._create_window()
        logger.info(f"Window changed to {window_type}")
    
    def set_fft_length(self, length: int) -> None:
        """Change FFT length"""
        if length <= 0 or (length & (length - 1)) != 0:
            raise ValueError("FFT length must be a positive power of 2")
        self.fft_length = length
        self.window = self._create_window()
        logger.info(f"FFT length changed to {length}")
    
    def compute_fft(self, signal: np.ndarray, fs: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute FFT of input signal
        
        Args:
            signal: Input signal
            fs: Sampling frequency
            
        Returns:
            frequencies: Frequency axis
            magnitude: FFT magnitude spectrum
        """
        # Pad signal if necessary
        if len(signal) < self.fft_length:
            signal = np.pad(signal, (0, self.fft_length - len(signal)), mode='constant')
        else:
            signal = signal[:self.fft_length]
        
        # Apply window
        windowed_signal = signal * self.window
        
        # Compute FFT
        fft_result = fft(windowed_signal, self.fft_length)
        magnitude = np.abs(fft_result[:self.fft_length // 2])
        
        # Compute frequency axis
        frequencies = fftfreq(self.fft_length, 1/fs)[:self.fft_length // 2]
        
        return frequencies, magnitude
    
    def compute_fft_segments(self, signal: np.ndarray, fs: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute FFT with overlapping segments (for Welch-like analysis)
        
        Args:
            signal: Input signal
            fs: Sampling frequency
            
        Returns:
            frequencies: Frequency axis
            time_segments: Time points for each segment
            fft_matrix: FFT results for each segment (segments x frequencies)
        """
        hop_length = int(self.fft_length * (1 - self.overlap))
        num_segments = (len(signal) - self.fft_length) // hop_length + 1
        
        if num_segments <= 0:
            num_segments = 1
            hop_length = len(signal) - self.fft_length
        
        fft_matrix = np.zeros((num_segments, self.fft_length // 2))
        time_segments = np.zeros(num_segments)
        
        for i in range(num_segments):
            start = i * hop_length
            end = start + self.fft_length
            
            if end > len(signal):
                segment = np.pad(signal[start:], (0, end - len(signal)), mode='constant')
            else:
                segment = signal[start:end]
            
            # Apply window and compute FFT
            windowed = segment * self.window
            fft_result = fft(windowed, self.fft_length)
            fft_matrix[i] = np.abs(fft_result[:self.fft_length // 2])
            time_segments[i] = start / fs
        
        frequencies = fftfreq(self.fft_length, 1/fs)[:self.fft_length // 2]
        
        return frequencies, time_segments, fft_matrix
    
    def get_frequency_resolution(self, fs: float) -> float:
        """Get frequency resolution in Hz"""
        return fs / self.fft_length
    
    def get_nyquist_frequency(self, fs: float) -> float:
        """Get Nyquist frequency"""
        return fs / 2


if __name__ == "__main__":
    # Test FFT module
    fft_module = FFTModule(fft_length=2048, window="hann", overlap=0.5)
    
    # Create test signal
    fs = 44100
    t = np.linspace(0, 1, fs)
    test_signal = np.sin(2 * np.pi * 440 * t) + 0.5 * np.sin(2 * np.pi * 880 * t)
    
    # Compute FFT
    frequencies, magnitude = fft_module.compute_fft(test_signal, fs)
    
    print(f"Frequency resolution: {fft_module.get_frequency_resolution(fs):.2f} Hz")
    print(f"Nyquist frequency: {fft_module.get_nyquist_frequency(fs):.2f} Hz")
    print(f"FFT shape: {magnitude.shape}")

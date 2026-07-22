"""Power Spectral Density (PSD) Module"""

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class PSDModule:
    """Power Spectral Density calculations using various methods"""
    
    def __init__(self, method: str = "welch", fs: float = 44100):
        """
        Initialize PSD module
        
        Args:
            method: PSD calculation method (welch, periodogram, multitaper, bartlett, blackman-tukey)
            fs: Sampling frequency
        """
        self.method = method
        self.fs = fs
        valid_methods = ["welch", "periodogram", "multitaper", "bartlett", "blackman-tukey"]
        if method not in valid_methods:
            raise ValueError(f"Invalid method. Must be one of {valid_methods}")
        logger.info(f"PSD Module initialized: method={method}, fs={fs} Hz")
    
    def compute_welch(self, signal_data: np.ndarray, nperseg: Optional[int] = None, 
                     noverlap: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute PSD using Welch's method
        
        Args:
            signal_data: Input signal
            nperseg: Length of segments (default: None, uses 256)
            noverlap: Overlap length (default: nperseg//2)
            
        Returns:
            frequencies: Frequency axis
            psd: Power Spectral Density
        """
        if nperseg is None:
            nperseg = min(256, len(signal_data))
        if noverlap is None:
            noverlap = nperseg // 2
        
        frequencies, psd = signal.welch(signal_data, self.fs, nperseg=nperseg, 
                                       noverlap=noverlap, window='hann')
        return frequencies, psd
    
    def compute_periodogram(self, signal_data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute PSD using Periodogram method
        
        Args:
            signal_data: Input signal
            
        Returns:
            frequencies: Frequency axis
            psd: Power Spectral Density
        """
        frequencies, psd = signal.periodogram(signal_data, self.fs)
        return frequencies, psd
    
    def compute_multitaper(self, signal_data: np.ndarray, NW: float = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute PSD using Multitaper method
        
        Args:
            signal_data: Input signal
            NW: Time-bandwidth product (default: 4)
            
        Returns:
            frequencies: Frequency axis
            psd: Power Spectral Density
        """
        frequencies, psd = signal.welch(signal_data, self.fs, window='dpss', 
                                       nperseg=len(signal_data))
        return frequencies, psd
    
    def compute_bartlett(self, signal_data: np.ndarray, nperseg: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute PSD using Bartlett method (non-overlapping Hann windows)
        
        Args:
            signal_data: Input signal
            nperseg: Length of segments
            
        Returns:
            frequencies: Frequency axis
            psd: Power Spectral Density
        """
        if nperseg is None:
            nperseg = min(256, len(signal_data))
        
        frequencies, psd = signal.welch(signal_data, self.fs, nperseg=nperseg, 
                                       noverlap=0, window='hann')
        return frequencies, psd
    
    def compute_blackman_tukey(self, signal_data: np.ndarray, nlags: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute PSD using Blackman-Tukey method (autocorrelation)
        
        Args:
            signal_data: Input signal
            nlags: Number of lags
            
        Returns:
            frequencies: Frequency axis
            psd: Power Spectral Density
        """
        if nlags is None:
            nlags = len(signal_data) // 2
        
        # Compute autocorrelation
        auto_corr = np.correlate(signal_data - np.mean(signal_data), 
                                signal_data - np.mean(signal_data), mode='full')
        auto_corr = auto_corr[len(auto_corr)//2:]
        auto_corr = auto_corr[:nlags]
        
        # Apply Blackman window
        window_vals = np.blackman(len(auto_corr))
        auto_corr = auto_corr * window_vals
        
        # Compute FFT
        psd = np.abs(fft(auto_corr, len(auto_corr) * 2))
        frequencies = fftfreq(len(psd), 1/self.fs)
        
        # Return positive frequencies only
        positive_idx = frequencies >= 0
        return frequencies[positive_idx], psd[positive_idx]
    
    def compute_psd(self, signal_data: np.ndarray, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute PSD using the configured method
        
        Args:
            signal_data: Input signal
            **kwargs: Method-specific parameters
            
        Returns:
            frequencies: Frequency axis
            psd: Power Spectral Density
        """
        if self.method == "welch":
            return self.compute_welch(signal_data, **kwargs)
        elif self.method == "periodogram":
            return self.compute_periodogram(signal_data)
        elif self.method == "multitaper":
            return self.compute_multitaper(signal_data, **kwargs)
        elif self.method == "bartlett":
            return self.compute_bartlett(signal_data, **kwargs)
        elif self.method == "blackman-tukey":
            return self.compute_blackman_tukey(signal_data, **kwargs)
        else:
            raise ValueError(f"Unknown method: {self.method}")
    
    def db_per_hz(self, psd: np.ndarray, reference: float = 1e-6) -> np.ndarray:
        """Convert PSD to dB/Hz"""
        return 10 * np.log10(psd / (reference ** 2) + 1e-20)
    
    def db_re_uPa2_per_hz(self, psd: np.ndarray) -> np.ndarray:
        """Convert PSD to dB re 1 µPa²/Hz"""
        return 10 * np.log10(psd + 1e-20)


if __name__ == "__main__":
    # Test PSD module
    fs = 44100
    t = np.linspace(0, 1, fs)
    test_signal = np.sin(2 * np.pi * 440 * t) + 0.5 * np.sin(2 * np.pi * 880 * t)
    
    psd_module = PSDModule(method="welch", fs=fs)
    frequencies, psd = psd_module.compute_psd(test_signal)
    
    print(f"PSD shape: {psd.shape}")
    print(f"PSD range: {psd.min():.2e} to {psd.max():.2e}")

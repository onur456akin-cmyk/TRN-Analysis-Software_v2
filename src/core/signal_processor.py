"""Signal Processing Module"""

import numpy as np
from scipy import signal
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class SignalProcessor:
    """Signal processing utilities"""
    
    @staticmethod
    def remove_dc_offset(signal_data: np.ndarray) -> np.ndarray:
        """Remove DC offset from signal"""
        return signal_data - np.mean(signal_data)
    
    @staticmethod
    def normalize(signal_data: np.ndarray) -> np.ndarray:
        """Normalize signal to [-1, 1] range"""
        max_val = np.max(np.abs(signal_data))
        if max_val > 0:
            return signal_data / max_val
        return signal_data
    
    @staticmethod
    def bandpass_filter(signal_data: np.ndarray, fs: float, lowcut: float, 
                       highcut: float, order: int = 5) -> np.ndarray:
        """
        Apply bandpass filter
        
        Args:
            signal_data: Input signal
            fs: Sampling frequency
            lowcut: Low cutoff frequency
            highcut: High cutoff frequency
            order: Filter order
            
        Returns:
            Filtered signal
        """
        nyquist = fs / 2
        low = lowcut / nyquist
        high = highcut / nyquist
        
        # Ensure valid range
        low = np.clip(low, 0.001, 0.999)
        high = np.clip(high, 0.001, 0.999)
        
        if low >= high:
            logger.warning("Invalid bandpass filter range")
            return signal_data
        
        b, a = signal.butter(order, [low, high], btype='band')
        filtered = signal.filtfilt(b, a, signal_data)
        return filtered
    
    @staticmethod
    def highpass_filter(signal_data: np.ndarray, fs: float, cutoff: float, 
                       order: int = 5) -> np.ndarray:
        """Apply highpass filter"""
        nyquist = fs / 2
        normalized_cutoff = np.clip(cutoff / nyquist, 0.001, 0.999)
        b, a = signal.butter(order, normalized_cutoff, btype='high')
        return signal.filtfilt(b, a, signal_data)
    
    @staticmethod
    def lowpass_filter(signal_data: np.ndarray, fs: float, cutoff: float, 
                      order: int = 5) -> np.ndarray:
        """Apply lowpass filter"""
        nyquist = fs / 2
        normalized_cutoff = np.clip(cutoff / nyquist, 0.001, 0.999)
        b, a = signal.butter(order, normalized_cutoff, btype='low')
        return signal.filtfilt(b, a, signal_data)
    
    @staticmethod
    def compute_rms(signal_data: np.ndarray) -> float:
        """Compute RMS value"""
        return np.sqrt(np.mean(signal_data ** 2))
    
    @staticmethod
    def compute_peak(signal_data: np.ndarray) -> float:
        """Compute peak value"""
        return np.max(np.abs(signal_data))
    
    @staticmethod
    def compute_crest_factor(signal_data: np.ndarray) -> float:
        """Compute crest factor (peak/RMS)"""
        rms = SignalProcessor.compute_rms(signal_data)
        if rms == 0:
            return 0
        return SignalProcessor.compute_peak(signal_data) / rms
    
    @staticmethod
    def extract_segment(signal_data: np.ndarray, fs: float, start_time: float, 
                       end_time: float) -> np.ndarray:
        """Extract time segment from signal"""
        start_idx = int(start_time * fs)
        end_idx = int(end_time * fs)
        return signal_data[start_idx:end_idx]


if __name__ == "__main__":
    print("Signal Processing module loaded")

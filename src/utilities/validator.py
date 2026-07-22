"""Data validation utilities"""

from pathlib import Path
from typing import Tuple, Optional
import numpy as np


class DataValidator:
    """Data validation helper class"""
    
    SUPPORTED_FORMATS = [".wav", ".bin", ".txt"]
    
    @staticmethod
    def validate_file(file_path: Path) -> Tuple[bool, str]:
        """Validate if file exists and is supported format"""
        if not file_path.exists():
            return False, "File does not exist"
        
        if not file_path.is_file():
            return False, "Path is not a file"
        
        if file_path.suffix.lower() not in DataValidator.SUPPORTED_FORMATS:
            return False, f"Unsupported format: {file_path.suffix}"
        
        if file_path.stat().st_size == 0:
            return False, "File is empty"
        
        return True, "File is valid"
    
    @staticmethod
    def validate_audio_data(data: np.ndarray) -> Tuple[bool, str]:
        """Validate audio data array"""
        if not isinstance(data, np.ndarray):
            return False, "Data must be numpy array"
        
        if len(data) == 0:
            return False, "Data array is empty"
        
        if np.all(np.isnan(data)):
            return False, "Data contains only NaN values"
        
        if np.all(np.isinf(data)):
            return False, "Data contains infinite values"
        
        return True, "Audio data is valid"
    
    @staticmethod
    def validate_sampling_frequency(fs: float) -> Tuple[bool, str]:
        """Validate sampling frequency"""
        if fs <= 0:
            return False, "Sampling frequency must be positive"
        
        if fs < 8000:
            return False, "Sampling frequency too low (minimum 8000 Hz)"
        
        if fs > 1000000:
            return False, "Sampling frequency too high (maximum 1 MHz)"
        
        return True, "Sampling frequency is valid"
    
    @staticmethod
    def validate_time_range(start: float, end: float, max_duration: float) -> Tuple[bool, str]:
        """Validate time range selection"""
        if start < 0:
            return False, "Start time cannot be negative"
        
        if end < 0:
            return False, "End time cannot be negative"
        
        if start >= end:
            return False, "Start time must be less than end time"
        
        if end > max_duration:
            return False, f"End time exceeds recording duration ({max_duration}s)"
        
        return True, "Time range is valid"
    
    @staticmethod
    def validate_sensitivity(sensitivity: float) -> Tuple[bool, str]:
        """Validate hydrophone sensitivity"""
        if sensitivity > 0:
            return False, "Sensitivity should be negative (dB re 1V/µPa)"
        
        if sensitivity < -300:
            return False, "Sensitivity value seems unrealistic"
        
        return True, "Sensitivity is valid"
    
    @staticmethod
    def validate_gain(gain: float) -> Tuple[bool, str]:
        """Validate amplifier gain"""
        if gain < -100 or gain > 100:
            return False, "Gain should be between -100 and 100 dB"
        
        return True, "Gain is valid"

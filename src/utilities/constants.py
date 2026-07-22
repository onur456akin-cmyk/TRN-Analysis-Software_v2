"""Application Constants"""

import numpy as np

# Physical constants
SPEED_OF_SOUND_WATER = 1500  # m/s
REFERENCE_PRESSURE = 1e-6  # 1 µPa
REFERENCE_INTENSITY = 1e-12  # W/m²

# Window functions info
WINDOW_INFO = {
    "hann": {"name": "Hann", "spectral_leakage": -32},
    "hamming": {"name": "Hamming", "spectral_leakage": -43},
    "blackman": {"name": "Blackman", "spectral_leakage": -58},
    "kaiser": {"name": "Kaiser", "spectral_leakage": -50},
    "rectangular": {"name": "Rectangular", "spectral_leakage": -13},
    "blackman-harris": {"name": "Blackman-Harris", "spectral_leakage": -92},
    "flat-top": {"name": "Flat-top", "spectral_leakage": -93},
}

# PSD Methods info
PSD_METHOD_INFO = {
    "welch": {"name": "Welch PSD", "description": "Welch method using Hann window and 50% overlap"},
    "periodogram": {"name": "Periodogram", "description": "Simple FFT-based PSD"},
    "multitaper": {"name": "Multitaper", "description": "Uses multiple tapers for better estimates"},
    "bartlett": {"name": "Bartlett", "description": "Averaged periodograms"},
    "blackman-tukey": {"name": "Blackman-Tukey", "description": "Autocorrelation method"},
}

# TRN Algorithm info
TRN_ALGORITHM_INFO = {
    "ANSI": {"name": "ANSI S1.4", "reference": "ANSI S1.4-2007"},
    "ISO": {"name": "ISO 20998", "reference": "ISO 20998-1:2020"},
    "Welch PSD": {"name": "Welch PSD Method", "reference": "Custom"},
    "FFT Average": {"name": "FFT Average", "reference": "Custom"},
    "RMS": {"name": "RMS Method", "reference": "Custom"},
}

# Transmission Loss Models info
TL_MODEL_INFO = {
    "Spherical": {"name": "Spherical Spreading", "formula": "TL = 20*log10(r)"},
    "Cylindrical": {"name": "Cylindrical Spreading", "formula": "TL = 10*log10(r)"},
    "Practical": {"name": "Practical Spreading", "formula": "TL = 10*log10(r) + k*r"},
    "User Defined": {"name": "User Defined", "formula": "Custom"},
}

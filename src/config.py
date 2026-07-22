"""Application Configuration Management"""

from pathlib import Path
from typing import Optional
import json


class Config:
    """Application configuration management"""
    
    # Application metadata
    app_name = "TRN Analysis Software"
    version = "0.1.0"
    author = "Onur Akin"
    description = "Professional acoustic analysis software for Target Radiated Noise calculation"
    
    # Paths
    base_path = Path(__file__).parent.parent
    src_path = base_path / "src"
    data_path = base_path / "data"
    resources_path = base_path / "resources"
    plugins_path = base_path / "plugins"
    docs_path = base_path / "docs"
    
    # Create directories if they don't exist
    data_path.mkdir(exist_ok=True)
    (data_path / "cache").mkdir(exist_ok=True)
    (data_path / "logs").mkdir(exist_ok=True)
    plugins_path.mkdir(exist_ok=True)
    
    # File formats
    supported_formats = [".wav", ".bin", ".txt"]
    supported_export_formats = ["csv", "txt", "excel", "pdf"]
    
    # Audio settings
    default_sample_rate = 44100  # Hz
    audio_buffer_size = 4096
    
    # FFT settings
    default_fft_length = 2048
    fft_lengths = [512, 1024, 2048, 4096, 8192, 16384]
    window_types = ["hann", "hamming", "blackman", "kaiser", "rectangular", "blackman-harris", "flat-top"]
    
    # PSD settings
    psd_methods = ["welch", "periodogram", "multitaper", "bartlett", "blackman-tukey"]
    default_psd_method = "welch"
    
    # TRN algorithms
    trn_algorithms = ["ANSI", "ISO", "Welch PSD", "FFT Average", "RMS", "Custom"]
    default_trn_algorithm = "ANSI"
    
    # Transmission loss models
    transmission_loss_models = ["Spherical", "Cylindrical", "Practical", "User Defined"]
    default_transmission_loss_model = "Spherical"
    
    # UI settings
    theme = "dark"  # "dark" or "light" or "high_contrast"
    language = "en_US"  # "tr_TR" or "en_US"
    
    # Standards
    supported_standards = ["ISO", "ANSI", "IEC", "NATO", "STANAG", "MIL-STD", "DNV", "Lloyd's Register"]
    default_standard = "ISO"
    
    # Performance
    max_file_size_mb = 1000
    max_memory_mb = 2048
    
    # Hydrophone reference
    hydrophone_reference_pressure = 1e-6  # 1 µPa
    reference_distance = 1.0  # 1 meter
    
    # Default parameter values
    default_hydrophone_sensitivity = -170  # dB re 1V/µPa
    default_amplifier_gain = 0  # dB
    default_max_cpa_distance = 1000  # meters
    
    # User settings file
    user_settings_file = data_path / "user_settings.json"
    
    # Audit log
    audit_log_db = data_path / "audit_log.db"

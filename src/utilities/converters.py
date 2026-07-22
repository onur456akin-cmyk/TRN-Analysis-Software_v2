"""Unit and data conversion utilities"""

import numpy as np
from typing import Union


class UnitConverter:
    """Unit conversion helper class"""
    
    @staticmethod
    def hz_to_khz(frequency_hz: float) -> float:
        """Convert Hz to kHz"""
        return frequency_hz / 1000
    
    @staticmethod
    def khz_to_hz(frequency_khz: float) -> float:
        """Convert kHz to Hz"""
        return frequency_khz * 1000
    
    @staticmethod
    def db_to_linear(db_value: float) -> float:
        """Convert dB to linear scale"""
        return 10 ** (db_value / 10)
    
    @staticmethod
    def linear_to_db(linear_value: float, reference: float = 1.0) -> float:
        """Convert linear value to dB"""
        if linear_value <= 0:
            return float('-inf')
        return 10 * np.log10(linear_value / reference)
    
    @staticmethod
    def pressure_to_db(pressure: float, reference_pressure: float = 1e-6) -> float:
        """Convert pressure to dB re 1 µPa"""
        if pressure <= 0:
            return float('-inf')
        return 20 * np.log10(pressure / reference_pressure)
    
    @staticmethod
    def db_to_pressure(db_value: float, reference_pressure: float = 1e-6) -> float:
        """Convert dB to pressure"""
        return reference_pressure * (10 ** (db_value / 20))
    
    @staticmethod
    def voltage_to_pressure(voltage: float, sensitivity_db: float, reference_pressure: float = 1e-6) -> float:
        """Convert voltage to pressure using hydrophone sensitivity"""
        sensitivity_linear = 10 ** (sensitivity_db / 20)  # V/µPa
        pressure_uPa = voltage / sensitivity_linear
        pressure_pa = pressure_uPa * reference_pressure
        return pressure_pa
    
    @staticmethod
    def apply_gain(signal: np.ndarray, gain_db: float) -> np.ndarray:
        """Apply gain to signal"""
        gain_linear = 10 ** (gain_db / 20)
        return signal * gain_linear
    
    @staticmethod
    def apply_transmission_loss_spherical(level_db: float, distance: float, reference_distance: float = 1.0) -> float:
        """Apply spherical transmission loss correction (20*log10(r/r0))"""
        if distance <= 0 or reference_distance <= 0:
            return level_db
        transmission_loss = 20 * np.log10(distance / reference_distance)
        return level_db + transmission_loss
    
    @staticmethod
    def apply_transmission_loss_cylindrical(level_db: float, distance: float, reference_distance: float = 1.0) -> float:
        """Apply cylindrical transmission loss correction (10*log10(r/r0))"""
        if distance <= 0 or reference_distance <= 0:
            return level_db
        transmission_loss = 10 * np.log10(distance / reference_distance)
        return level_db + transmission_loss


class DataConverter:
    """Data format conversion utilities"""
    
    @staticmethod
    def normalize_signal(signal: np.ndarray) -> np.ndarray:
        """Normalize signal to [-1, 1] range"""
        max_val = np.max(np.abs(signal))
        if max_val > 0:
            return signal / max_val
        return signal
    
    @staticmethod
    def remove_dc_offset(signal: np.ndarray) -> np.ndarray:
        """Remove DC offset (mean) from signal"""
        return signal - np.mean(signal)

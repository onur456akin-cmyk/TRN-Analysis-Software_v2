"""Calibration Module for hydrophone and amplifier compensation"""

import numpy as np
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class CalibrationModule:
    """Handle calibration and compensation operations"""
    
    @staticmethod
    def apply_hydrophone_sensitivity(signal_voltage: np.ndarray, 
                                    sensitivity_db: float,
                                    reference_pressure: float = 1e-6) -> np.ndarray:
        """
        Apply hydrophone sensitivity compensation
        Convert voltage to pressure
        
        Args:
            signal_voltage: Voltage signal
            sensitivity_db: Hydrophone sensitivity (dB re 1V/µPa)
            reference_pressure: Reference pressure (default 1 µPa)
            
        Returns:
            Pressure signal in Pa
        """
        # Convert sensitivity from dB to linear (V/µPa)
        sensitivity_linear = 10 ** (sensitivity_db / 20)
        
        # Convert voltage to pressure in µPa
        pressure_uPa = signal_voltage / sensitivity_linear
        
        # Convert to Pa
        pressure_pa = pressure_uPa * reference_pressure
        
        logger.info(f"Applied hydrophone sensitivity: {sensitivity_db} dB re 1V/µPa")
        return pressure_pa
    
    @staticmethod
    def apply_amplifier_gain(signal: np.ndarray, gain_db: float) -> np.ndarray:
        """
        Apply amplifier gain compensation
        
        Args:
            signal: Input signal
            gain_db: Gain in dB
            
        Returns:
            Signal with gain removed
        """
        gain_linear = 10 ** (gain_db / 20)
        corrected_signal = signal / gain_linear
        logger.info(f"Applied amplifier gain correction: {gain_db} dB")
        return corrected_signal
    
    @staticmethod
    def apply_full_calibration(signal_voltage: np.ndarray,
                              sensitivity_db: float,
                              amplifier_gain_db: float,
                              reference_pressure: float = 1e-6) -> np.ndarray:
        """
        Apply full calibration chain
        
        Args:
            signal_voltage: Raw voltage signal
            sensitivity_db: Hydrophone sensitivity
            amplifier_gain_db: Amplifier gain
            reference_pressure: Reference pressure
            
        Returns:
            Calibrated pressure signal
        """
        # First remove amplifier gain
        signal_no_gain = CalibrationModule.apply_amplifier_gain(signal_voltage, amplifier_gain_db)
        
        # Then apply hydrophone sensitivity
        pressure_signal = CalibrationModule.apply_hydrophone_sensitivity(
            signal_no_gain, sensitivity_db, reference_pressure
        )
        
        logger.info(f"Full calibration applied: sensitivity={sensitivity_db} dB, gain={amplifier_gain_db} dB")
        return pressure_signal
    
    @staticmethod
    def get_pressure_level_db(pressure: np.ndarray, reference_pressure: float = 1e-6) -> float:
        """
        Calculate pressure level in dB
        
        Args:
            pressure: Pressure signal in Pa
            reference_pressure: Reference pressure (default 1 µPa = 1e-6 Pa)
            
        Returns:
            Pressure level in dB re 1 µPa
        """
        rms_pressure = np.sqrt(np.mean(pressure ** 2))
        if rms_pressure <= 0:
            return float('-inf')
        level_db = 20 * np.log10(rms_pressure / reference_pressure)
        return level_db


if __name__ == "__main__":
    print("Calibration Module loaded")

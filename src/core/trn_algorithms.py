"""TRN Calculation Algorithms"""

import numpy as np
from scipy import signal
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class TRNCalculator:
    """Target Radiated Noise (TRN) calculation methods"""
    
    @staticmethod
    def calculate_trn_ansi(pressure_signal: np.ndarray, fs: float, 
                          reference_pressure: float = 1e-6) -> float:
        """
        Calculate TRN using ANSI S1.4 method
        
        Args:
            pressure_signal: Calibrated pressure signal in Pa
            fs: Sampling frequency
            reference_pressure: Reference pressure (1 µPa)
            
        Returns:
            TRN level in dB re 1 µPa
        """
        # Compute RMS pressure
        rms_pressure = np.sqrt(np.mean(pressure_signal ** 2))
        
        # Convert to dB
        if rms_pressure <= 0:
            return float('-inf')
        
        trn_db = 20 * np.log10(rms_pressure / reference_pressure)
        logger.info(f"ANSI TRN: {trn_db:.2f} dB re 1 µPa")
        return trn_db
    
    @staticmethod
    def calculate_trn_iso(pressure_signal: np.ndarray, fs: float, 
                         reference_pressure: float = 1e-6) -> float:
        """
        Calculate TRN using ISO 20998 method
        Similar to ANSI but with ISO-specific parameters
        
        Args:
            pressure_signal: Calibrated pressure signal in Pa
            fs: Sampling frequency
            reference_pressure: Reference pressure (1 µPa)
            
        Returns:
            TRN level in dB re 1 µPa
        """
        # Compute RMS pressure
        rms_pressure = np.sqrt(np.mean(pressure_signal ** 2))
        
        if rms_pressure <= 0:
            return float('-inf')
        
        trn_db = 20 * np.log10(rms_pressure / reference_pressure)
        logger.info(f"ISO TRN: {trn_db:.2f} dB re 1 µPa")
        return trn_db
    
    @staticmethod
    def calculate_trn_welch_psd(pressure_signal: np.ndarray, fs: float,
                               reference_pressure: float = 1e-6,
                               nperseg: int = 2048) -> Tuple[float, np.ndarray, np.ndarray]:
        """
        Calculate TRN using Welch PSD method
        
        Args:
            pressure_signal: Calibrated pressure signal in Pa
            fs: Sampling frequency
            reference_pressure: Reference pressure
            nperseg: Segment length for Welch method
            
        Returns:
            trn_db: TRN level in dB
            frequencies: Frequency axis
            psd: Power spectral density
        """
        # Compute Welch PSD
        frequencies, psd = signal.welch(pressure_signal, fs, nperseg=nperseg, 
                                       window='hann', scaling='density')
        
        # Integrate PSD to get total power
        total_power = np.trapz(psd, frequencies)
        
        # Convert to dB
        rms_pressure = np.sqrt(total_power)
        if rms_pressure <= 0:
            trn_db = float('-inf')
        else:
            trn_db = 20 * np.log10(rms_pressure / reference_pressure)
        
        logger.info(f"Welch PSD TRN: {trn_db:.2f} dB re 1 µPa")
        return trn_db, frequencies, psd
    
    @staticmethod
    def calculate_trn_fft_average(pressure_signal: np.ndarray, fs: float,
                                 reference_pressure: float = 1e-6,
                                 nfft: int = 2048) -> Tuple[float, np.ndarray, np.ndarray]:
        """
        Calculate TRN using FFT averaging method
        
        Args:
            pressure_signal: Calibrated pressure signal in Pa
            fs: Sampling frequency
            reference_pressure: Reference pressure
            nfft: FFT length
            
        Returns:
            trn_db: TRN level in dB
            frequencies: Frequency axis
            magnitude: FFT magnitude spectrum
        """
        # Pad to FFT length
        if len(pressure_signal) < nfft:
            pressure_signal = np.pad(pressure_signal, (0, nfft - len(pressure_signal)))
        else:
            pressure_signal = pressure_signal[:nfft]
        
        # Apply Hann window
        window = signal.get_window('hann', nfft)
        windowed = pressure_signal * window
        
        # Compute FFT
        fft_result = np.fft.fft(windowed, nfft)
        magnitude = np.abs(fft_result[:nfft // 2])
        frequencies = np.fft.fftfreq(nfft, 1/fs)[:nfft // 2]
        
        # Convert magnitude to pressure RMS
        magnitude_db = 20 * np.log10(magnitude / reference_pressure + 1e-10)
        
        # TRN is the mean of the magnitude spectrum
        trn_db = np.mean(magnitude_db)
        
        logger.info(f"FFT Average TRN: {trn_db:.2f} dB re 1 µPa")
        return trn_db, frequencies, magnitude_db
    
    @staticmethod
    def calculate_trn_rms(pressure_signal: np.ndarray, 
                         reference_pressure: float = 1e-6) -> float:
        """
        Calculate TRN using simple RMS method
        
        Args:
            pressure_signal: Calibrated pressure signal in Pa
            reference_pressure: Reference pressure
            
        Returns:
            TRN level in dB re 1 µPa
        """
        rms_pressure = np.sqrt(np.mean(pressure_signal ** 2))
        
        if rms_pressure <= 0:
            return float('-inf')
        
        trn_db = 20 * np.log10(rms_pressure / reference_pressure)
        logger.info(f"RMS TRN: {trn_db:.2f} dB re 1 µPa")
        return trn_db
    
    @staticmethod
    def calculate_all_algorithms(pressure_signal: np.ndarray, fs: float,
                                reference_pressure: float = 1e-6) -> Dict[str, float]:
        """
        Calculate TRN using all available methods for comparison
        
        Args:
            pressure_signal: Calibrated pressure signal
            fs: Sampling frequency
            reference_pressure: Reference pressure
            
        Returns:
            Dictionary with all TRN values
        """
        results = {}
        
        try:
            results['ANSI'] = TRNCalculator.calculate_trn_ansi(pressure_signal, fs, reference_pressure)
        except Exception as e:
            logger.error(f"ANSI calculation error: {e}")
            results['ANSI'] = None
        
        try:
            results['ISO'] = TRNCalculator.calculate_trn_iso(pressure_signal, fs, reference_pressure)
        except Exception as e:
            logger.error(f"ISO calculation error: {e}")
            results['ISO'] = None
        
        try:
            results['Welch PSD'], _, _ = TRNCalculator.calculate_trn_welch_psd(
                pressure_signal, fs, reference_pressure
            )
        except Exception as e:
            logger.error(f"Welch PSD calculation error: {e}")
            results['Welch PSD'] = None
        
        try:
            results['FFT Average'], _, _ = TRNCalculator.calculate_trn_fft_average(
                pressure_signal, fs, reference_pressure
            )
        except Exception as e:
            logger.error(f"FFT Average calculation error: {e}")
            results['FFT Average'] = None
        
        try:
            results['RMS'] = TRNCalculator.calculate_trn_rms(pressure_signal, reference_pressure)
        except Exception as e:
            logger.error(f"RMS calculation error: {e}")
            results['RMS'] = None
        
        return results


if __name__ == "__main__":
    print("TRN Calculator module loaded")

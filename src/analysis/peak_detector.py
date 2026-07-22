"""Peak Detection Module"""

import numpy as np
from typing import Dict, List, Tuple
from scipy import signal
import logging

logger = logging.getLogger(__name__)


class PeakDetector:
    """Automated peak detection in spectral data"""
    
    def __init__(self):
        self.peaks = None
        self.properties = None
    
    def detect(self, spectrum: np.ndarray, frequencies: np.ndarray,
              min_height: float = -40, min_distance: int = 10,
              min_prominence: float = 3.0) -> List[Dict]:
        """
        Detect peaks in spectrum
        
        Args:
            spectrum: Magnitude spectrum in dB
            frequencies: Frequency axis
            min_height: Minimum peak height in dB
            min_distance: Minimum distance between peaks (samples)
            min_prominence: Minimum peak prominence in dB
            
        Returns:
            List of peak dictionaries
        """
        # Find peaks
        self.peaks, self.properties = signal.find_peaks(
            spectrum,
            height=min_height,
            distance=min_distance,
            prominence=min_prominence
        )
        
        # Build peak list
        peaks_list = []
        for i, peak_idx in enumerate(self.peaks):
            peak_dict = {
                'index': i + 1,
                'frequency': frequencies[peak_idx],
                'magnitude_db': spectrum[peak_idx],
                'prominence': self.properties['prominences'][i],
                'left_edge': frequencies[peak_idx],
                'right_edge': frequencies[peak_idx],
            }
            peaks_list.append(peak_dict)
        
        logger.info(f"Detected {len(peaks_list)} peaks")
        return peaks_list
    
    def filter_peaks(self, peaks_list: List[Dict], 
                    frequency_range: Tuple[float, float] = None,
                    magnitude_threshold: float = None) -> List[Dict]:
        """
        Filter peaks based on criteria
        
        Args:
            peaks_list: List of peak dictionaries
            frequency_range: (min_freq, max_freq) tuple
            magnitude_threshold: Minimum magnitude in dB
            
        Returns:
            Filtered peak list
        """
        filtered = peaks_list
        
        if frequency_range:
            min_freq, max_freq = frequency_range
            filtered = [p for p in filtered if min_freq <= p['frequency'] <= max_freq]
        
        if magnitude_threshold:
            filtered = [p for p in filtered if p['magnitude_db'] >= magnitude_threshold]
        
        logger.info(f"After filtering: {len(filtered)} peaks")
        return filtered
    
    def get_top_peaks(self, peaks_list: List[Dict], count: int = 10) -> List[Dict]:
        """
        Get top N peaks by magnitude
        
        Args:
            peaks_list: List of peak dictionaries
            count: Number of peaks to return
            
        Returns:
            Top peaks sorted by magnitude
        """
        sorted_peaks = sorted(peaks_list, key=lambda x: x['magnitude_db'], reverse=True)
        return sorted_peaks[:count]
    
    def get_harmonics(self, fundamental_frequency: float, peaks_list: List[Dict],
                     tolerance: float = 0.05) -> List[Dict]:
        """
        Identify harmonics of a fundamental frequency
        
        Args:
            fundamental_frequency: Fundamental frequency in Hz
            peaks_list: List of peak dictionaries
            tolerance: Frequency tolerance as fraction of fundamental
            
        Returns:
            List of harmonic peaks
        """
        harmonics = []
        
        for harmonic_number in range(1, 10):
            expected_freq = fundamental_frequency * harmonic_number
            freq_tolerance = fundamental_frequency * tolerance
            
            # Find peak near expected frequency
            matching_peaks = [
                p for p in peaks_list
                if abs(p['frequency'] - expected_freq) <= freq_tolerance
            ]
            
            if matching_peaks:
                harmonic = matching_peaks[0]
                harmonic['harmonic_number'] = harmonic_number
                harmonics.append(harmonic)
        
        logger.info(f"Found {len(harmonics)} harmonics")
        return harmonics


if __name__ == "__main__":
    print("Peak Detector module loaded")

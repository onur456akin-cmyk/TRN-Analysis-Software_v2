"""Comparison Module for analyzing multiple recordings"""

import numpy as np
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ComparisonModule:
    """Compare multiple audio recordings or analysis results"""
    
    def __init__(self):
        self.comparison_data = []
        self.labels = []
    
    def add_spectrum(self, frequencies: np.ndarray, magnitude: np.ndarray,
                    label: str) -> None:
        """
        Add spectrum for comparison
        
        Args:
            frequencies: Frequency axis
            magnitude: Magnitude spectrum
            label: Label for this spectrum
        """
        self.comparison_data.append({
            'frequencies': frequencies,
            'magnitude': magnitude,
            'label': label
        })
        self.labels.append(label)
        logger.info(f"Added spectrum for comparison: {label}")
    
    def add_signal(self, signal: np.ndarray, fs: float, label: str) -> None:
        """
        Add time-domain signal for comparison
        
        Args:
            signal: Audio signal
            fs: Sampling frequency
            label: Label for this signal
        """
        self.comparison_data.append({
            'signal': signal,
            'fs': fs,
            'label': label
        })
        self.labels.append(label)
        logger.info(f"Added signal for comparison: {label}")
    
    def compute_difference(self, index1: int, index2: int) -> Dict:
        """
        Compute difference between two spectra
        
        Args:
            index1: Index of first spectrum
            index2: Index of second spectrum
            
        Returns:
            Difference metrics
        """
        if index1 >= len(self.comparison_data) or index2 >= len(self.comparison_data):
            raise IndexError("Invalid spectrum index")
        
        data1 = self.comparison_data[index1]
        data2 = self.comparison_data[index2]
        
        if 'magnitude' not in data1 or 'magnitude' not in data2:
            raise ValueError("Both entries must contain magnitude spectra")
        
        # Ensure same frequency resolution
        mag1 = data1['magnitude']
        mag2 = data2['magnitude']
        
        # Interpolate to same length if needed
        if len(mag1) != len(mag2):
            min_len = min(len(mag1), len(mag2))
            mag1 = mag1[:min_len]
            mag2 = mag2[:min_len]
        
        # Compute differences
        difference_db = mag1 - mag2
        mean_difference = np.mean(difference_db)
        max_difference = np.max(np.abs(difference_db))
        rms_difference = np.sqrt(np.mean(difference_db ** 2))
        
        return {
            'label1': self.labels[index1],
            'label2': self.labels[index2],
            'difference_db': difference_db,
            'mean_difference': mean_difference,
            'max_difference': max_difference,
            'rms_difference': rms_difference
        }
    
    def compute_correlation(self, index1: int, index2: int) -> float:
        """
        Compute correlation between two spectra
        
        Args:
            index1: Index of first spectrum
            index2: Index of second spectrum
            
        Returns:
            Correlation coefficient
        """
        data1 = self.comparison_data[index1]
        data2 = self.comparison_data[index2]
        
        if 'magnitude' not in data1 or 'magnitude' not in data2:
            raise ValueError("Both entries must contain magnitude spectra")
        
        mag1 = data1['magnitude']
        mag2 = data2['magnitude']
        
        # Ensure same length
        min_len = min(len(mag1), len(mag2))
        mag1 = mag1[:min_len]
        mag2 = mag2[:min_len]
        
        # Compute correlation
        correlation = np.corrcoef(mag1, mag2)[0, 1]
        return correlation
    
    def clear(self) -> None:
        """Clear comparison data"""
        self.comparison_data = []
        self.labels = []
        logger.info("Comparison data cleared")
    
    def get_summary(self) -> Dict:
        """Get summary of comparison data"""
        return {
            'num_items': len(self.comparison_data),
            'labels': self.labels,
            'items': self.comparison_data
        }


if __name__ == "__main__":
    print("Comparison Module loaded")

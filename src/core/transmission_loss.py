"""Transmission Loss Models"""

import numpy as np
from typing import Callable, Dict
import logging

logger = logging.getLogger(__name__)


class TransmissionLossModel:
    """Transmission Loss (TL) model implementations"""
    
    @staticmethod
    def spherical_spreading(distance: float, reference_distance: float = 1.0) -> float:
        """
        Spherical spreading model: TL = 20*log10(r/r0)
        
        Args:
            distance: Distance in meters
            reference_distance: Reference distance (default 1 m)
            
        Returns:
            Transmission loss in dB
        """
        if distance <= 0 or reference_distance <= 0:
            return 0.0
        return 20 * np.log10(distance / reference_distance)
    
    @staticmethod
    def cylindrical_spreading(distance: float, reference_distance: float = 1.0) -> float:
        """
        Cylindrical spreading model: TL = 10*log10(r/r0)
        
        Args:
            distance: Distance in meters
            reference_distance: Reference distance (default 1 m)
            
        Returns:
            Transmission loss in dB
        """
        if distance <= 0 or reference_distance <= 0:
            return 0.0
        return 10 * np.log10(distance / reference_distance)
    
    @staticmethod
    def practical_spreading(distance: float, absorption_coeff: float = 0.01, 
                           reference_distance: float = 1.0) -> float:
        """
        Practical spreading model: TL = 10*log10(r/r0) + a*r
        Combines cylindrical spreading with absorption
        
        Args:
            distance: Distance in meters
            absorption_coeff: Absorption coefficient (default 0.01 dB/m)
            reference_distance: Reference distance (default 1 m)
            
        Returns:
            Transmission loss in dB
        """
        if distance <= 0 or reference_distance <= 0:
            return 0.0
        
        cylindrical = 10 * np.log10(distance / reference_distance)
        absorption = absorption_coeff * distance
        return cylindrical + absorption
    
    @staticmethod
    def spreading_loss(distance: float, spread_factor: float, 
                      reference_distance: float = 1.0) -> float:
        """
        General spreading loss model: TL = spread_factor*log10(r/r0)
        
        Args:
            distance: Distance in meters
            spread_factor: Spreading factor (20 for spherical, 10 for cylindrical)
            reference_distance: Reference distance (default 1 m)
            
        Returns:
            Transmission loss in dB
        """
        if distance <= 0 or reference_distance <= 0:
            return 0.0
        return spread_factor * np.log10(distance / reference_distance)
    
    @staticmethod
    def correct_for_transmission_loss(level_db: float, model: str, distance: float, 
                                     reference_distance: float = 1.0, **kwargs) -> float:
        """
        Apply transmission loss correction to acoustic level
        
        Args:
            level_db: Original level in dB
            model: TL model ("spherical", "cylindrical", "practical")
            distance: Distance in meters
            reference_distance: Reference distance
            **kwargs: Additional model parameters
            
        Returns:
            Corrected level in dB
        """
        if model == "spherical":
            tl = TransmissionLossModel.spherical_spreading(distance, reference_distance)
        elif model == "cylindrical":
            tl = TransmissionLossModel.cylindrical_spreading(distance, reference_distance)
        elif model == "practical":
            absorption = kwargs.get('absorption_coeff', 0.01)
            tl = TransmissionLossModel.practical_spreading(distance, absorption, reference_distance)
        else:
            logger.warning(f"Unknown TL model: {model}. Using spherical.")
            tl = TransmissionLossModel.spherical_spreading(distance, reference_distance)
        
        return level_db + tl


if __name__ == "__main__":
    print("Transmission Loss Model module loaded")

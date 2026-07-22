"""File Manager for audio file handling"""

import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import logging
import soundfile as sf

logger = logging.getLogger(__name__)


class FileManager:
    """Manage audio file I/O operations"""
    
    SUPPORTED_FORMATS = [".wav", ".bin", ".txt"]
    
    @staticmethod
    def load_wav(file_path: Path) -> Tuple[np.ndarray, float]:
        """
        Load WAV file
        
        Args:
            file_path: Path to WAV file
            
        Returns:
            audio_data: Audio samples
            sample_rate: Sampling frequency
        """
        try:
            audio_data, sample_rate = sf.read(str(file_path))
            logger.info(f"Loaded WAV file: {file_path.name}, {len(audio_data)} samples at {sample_rate} Hz")
            return audio_data, sample_rate
        except Exception as e:
            logger.error(f"Error loading WAV file: {e}")
            raise
    
    @staticmethod
    def load_bin(file_path: Path, dtype: str = 'float32') -> np.ndarray:
        """
        Load binary file
        
        Args:
            file_path: Path to binary file
            dtype: Data type
            
        Returns:
            audio_data: Audio samples
        """
        try:
            audio_data = np.fromfile(str(file_path), dtype=dtype)
            logger.info(f"Loaded BIN file: {file_path.name}, {len(audio_data)} samples")
            return audio_data
        except Exception as e:
            logger.error(f"Error loading BIN file: {e}")
            raise
    
    @staticmethod
    def load_txt(file_path: Path, delimiter: str = None) -> np.ndarray:
        """
        Load text file
        
        Args:
            file_path: Path to text file
            delimiter: Column delimiter
            
        Returns:
            audio_data: Audio samples
        """
        try:
            audio_data = np.loadtxt(str(file_path), delimiter=delimiter)
            logger.info(f"Loaded TXT file: {file_path.name}, {len(audio_data)} samples")
            return audio_data
        except Exception as e:
            logger.error(f"Error loading TXT file: {e}")
            raise
    
    @staticmethod
    def load_audio(file_path: Path, **kwargs) -> Tuple[np.ndarray, Optional[float]]:
        """
        Load audio file (auto-detects format)
        
        Args:
            file_path: Path to audio file
            **kwargs: Additional arguments for specific formats
            
        Returns:
            audio_data: Audio samples
            sample_rate: Sampling frequency (None for BIN/TXT)
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        suffix = file_path.suffix.lower()
        
        if suffix == ".wav":
            return FileManager.load_wav(file_path), None
        elif suffix == ".bin":
            return FileManager.load_bin(file_path, **kwargs), None
        elif suffix == ".txt":
            return FileManager.load_txt(file_path, **kwargs), None
        else:
            raise ValueError(f"Unsupported format: {suffix}")
    
    @staticmethod
    def save_wav(file_path: Path, audio_data: np.ndarray, sample_rate: float) -> None:
        """
        Save audio to WAV file
        
        Args:
            file_path: Output file path
            audio_data: Audio samples
            sample_rate: Sampling frequency
        """
        try:
            sf.write(str(file_path), audio_data, int(sample_rate))
            logger.info(f"Saved WAV file: {file_path.name}")
        except Exception as e:
            logger.error(f"Error saving WAV file: {e}")
            raise
    
    @staticmethod
    def save_csv(file_path: Path, data: np.ndarray, header: str = "") -> None:
        """
        Save data to CSV file
        
        Args:
            file_path: Output file path
            data: Data to save
            header: CSV header
        """
        try:
            np.savetxt(str(file_path), data, delimiter=',', header=header)
            logger.info(f"Saved CSV file: {file_path.name}")
        except Exception as e:
            logger.error(f"Error saving CSV file: {e}")
            raise
    
    @staticmethod
    def get_file_info(file_path: Path) -> dict:
        """
        Get file information
        
        Args:
            file_path: Path to file
            
        Returns:
            File info dictionary
        """
        file_path = Path(file_path)
        return {
            "name": file_path.name,
            "size_mb": file_path.stat().st_size / (1024 * 1024),
            "format": file_path.suffix.lower(),
            "exists": file_path.exists(),
        }


if __name__ == "__main__":
    # Test file manager
    print("File Manager module loaded")

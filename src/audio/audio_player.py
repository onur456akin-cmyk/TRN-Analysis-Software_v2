"""Audio Player Module"""

import numpy as np
from pathlib import Path
from typing import Optional
import logging

try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False

logger = logging.getLogger(__name__)


class AudioPlayer:
    """Audio playback functionality"""
    
    def __init__(self, sample_rate: float = 44100):
        """
        Initialize audio player
        
        Args:
            sample_rate: Sampling frequency
        """
        self.sample_rate = sample_rate
        self.is_playing = False
        self.current_position = 0
        self.audio_data = None
        self.stream = None
        self.playback_speed = 1.0
        
        if not SOUNDDEVICE_AVAILABLE:
            logger.warning("sounddevice not available. Audio playback disabled.")
    
    def load_audio(self, audio_data: np.ndarray, sample_rate: float):
        """
        Load audio data for playback
        
        Args:
            audio_data: Audio samples
            sample_rate: Sampling frequency
        """
        self.audio_data = audio_data
        self.sample_rate = sample_rate
        self.current_position = 0
        logger.info(f"Audio loaded: {len(audio_data)} samples at {sample_rate} Hz")
    
    def play(self, start: float = 0.0):
        """
        Start audio playback
        
        Args:
            start: Start time in seconds
        """
        if not SOUNDDEVICE_AVAILABLE:
            logger.warning("Cannot play: sounddevice not available")
            return
        
        if self.audio_data is None:
            logger.warning("No audio data loaded")
            return
        
        try:
            start_idx = int(start * self.sample_rate)
            audio_segment = self.audio_data[start_idx:]
            
            # Adjust for playback speed
            if self.playback_speed != 1.0:
                # Resample audio for speed adjustment
                new_length = int(len(audio_segment) / self.playback_speed)
                audio_segment = np.interp(
                    np.linspace(0, len(audio_segment) - 1, new_length),
                    np.arange(len(audio_segment)),
                    audio_segment
                )
                fs = int(self.sample_rate * self.playback_speed)
            else:
                fs = self.sample_rate
            
            self.is_playing = True
            sd.play(audio_segment, fs)
            logger.info(f"Playback started at {start}s, speed {self.playback_speed}x")
        except Exception as e:
            logger.error(f"Playback error: {e}")
    
    def pause(self):
        """Pause audio playback"""
        if not SOUNDDEVICE_AVAILABLE:
            return
        
        try:
            sd.stop()
            self.is_playing = False
            logger.info("Playback paused")
        except Exception as e:
            logger.error(f"Pause error: {e}")
    
    def stop(self):
        """Stop audio playback"""
        if not SOUNDDEVICE_AVAILABLE:
            return
        
        try:
            sd.stop()
            self.is_playing = False
            self.current_position = 0
            logger.info("Playback stopped")
        except Exception as e:
            logger.error(f"Stop error: {e}")
    
    def set_playback_speed(self, speed: float):
        """
        Set playback speed
        
        Args:
            speed: Speed factor (0.5 = half speed, 2.0 = double speed)
        """
        if speed <= 0:
            raise ValueError("Playback speed must be positive")
        self.playback_speed = speed
        logger.info(f"Playback speed set to {speed}x")
    
    def get_duration(self) -> float:
        """Get audio duration in seconds"""
        if self.audio_data is None:
            return 0.0
        return len(self.audio_data) / self.sample_rate
    
    def is_playing_now(self) -> bool:
        """Check if audio is currently playing"""
        if not SOUNDDEVICE_AVAILABLE:
            return False
        return sd.is_playing() if SOUNDDEVICE_AVAILABLE else False


if __name__ == "__main__":
    print("Audio Player module loaded")

"""Real-time audio level monitoring for Speech2Text application."""

import numpy as np
import pyaudio
import threading
import time
from typing import Callable, Optional
from collections import deque


class AudioLevelMonitor:
    """Real-time audio level monitoring with amplitude detection."""
    
    def __init__(self, 
                 sample_rate: int = 44100,
                 chunk_size: int = 1024,
                 channels: int = 1,
                 update_callback: Optional[Callable] = None):
        """Initialize audio level monitor.
        
        Args:
            sample_rate: Audio sample rate in Hz
            chunk_size: Audio buffer size
            channels: Number of audio channels
            update_callback: Callback function for level updates
        """
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.channels = channels
        self.update_callback = update_callback
        
        # Audio processing
        self.audio = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Level calculation
        self.level_history = deque(maxlen=10)  # Keep last 10 readings for smoothing
        self.current_level = 0.0
        self.peak_level = 0.0
        self.noise_floor = 0.001  # Minimum threshold to ignore background noise
        
        # Voice activity detection
        self.voice_threshold = 0.02  # Threshold for voice activity
        self.is_voice_detected = False
        self.voice_start_time = None
        self.min_voice_duration = 0.1  # Minimum duration to consider as voice
        
    def start_monitoring(self) -> bool:
        """Start real-time audio level monitoring.
        
        Returns:
            True if monitoring started successfully, False otherwise
        """
        if self.monitoring:
            return True
            
        try:
            self.stream = self.audio.open(
                format=pyaudio.paFloat32,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=None
            )
            
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            
            return True
            
        except Exception as e:
            print(f"Failed to start audio monitoring: {e}")
            return False
    
    def stop_monitoring(self) -> None:
        """Stop audio level monitoring."""
        self.monitoring = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
            self.monitor_thread = None
            
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop running in separate thread."""
        while self.monitoring and self.stream:
            try:
                # Read audio data
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.float32)
                
                # Calculate RMS (Root Mean Square) level
                rms_level = np.sqrt(np.mean(audio_data ** 2))
                
                # Apply noise floor
                if rms_level < self.noise_floor:
                    rms_level = 0.0
                
                # Smooth the level using history
                self.level_history.append(rms_level)
                smoothed_level = np.mean(self.level_history)
                
                # Normalize to 0-1 range (adjust multiplier as needed)
                normalized_level = min(1.0, smoothed_level * 50)  # Amplify for visibility
                
                # Update current level
                self.current_level = normalized_level
                
                # Update peak level (with decay)
                if normalized_level > self.peak_level:
                    self.peak_level = normalized_level
                else:
                    self.peak_level *= 0.95  # Peak decay
                
                # Voice activity detection
                self._detect_voice_activity(normalized_level)
                
                # Call update callback
                if self.update_callback:
                    self.update_callback(normalized_level, self.is_voice_detected)
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.01)  # 100 FPS update rate
                
            except Exception as e:
                if self.monitoring:  # Only log if we're supposed to be monitoring
                    print(f"Audio monitoring error: {e}")
                break
    
    def _detect_voice_activity(self, level: float) -> None:
        """Detect voice activity based on audio level.
        
        Args:
            level: Current normalized audio level (0-1)
        """
        current_time = time.time()
        
        if level > self.voice_threshold:
            if not self.is_voice_detected:
                self.voice_start_time = current_time
            self.is_voice_detected = True
        else:
            if self.is_voice_detected:
                # Check if voice was detected for minimum duration
                if (self.voice_start_time and 
                    current_time - self.voice_start_time < self.min_voice_duration):
                    # Too short to be considered voice
                    pass
                else:
                    self.is_voice_detected = False
                    self.voice_start_time = None
    
    def get_current_level(self) -> float:
        """Get current audio level (0-1)."""
        return self.current_level
    
    def get_peak_level(self) -> float:
        """Get peak audio level (0-1)."""
        return self.peak_level
    
    def is_voice_active(self) -> bool:
        """Check if voice activity is detected."""
        return self.is_voice_detected
    
    def set_voice_threshold(self, threshold: float) -> None:
        """Set voice activity detection threshold (0-1).
        
        Args:
            threshold: New threshold value
        """
        self.voice_threshold = max(0.0, min(1.0, threshold))
    
    def set_noise_floor(self, noise_floor: float) -> None:
        """Set noise floor threshold (0-1).
        
        Args:
            noise_floor: New noise floor value
        """
        self.noise_floor = max(0.0, min(1.0, noise_floor))
    
    def calibrate_noise_floor(self, duration: float = 2.0) -> float:
        """Calibrate noise floor by measuring ambient noise.
        
        Args:
            duration: Calibration duration in seconds
            
        Returns:
            Calculated noise floor level
        """
        if not self.monitoring:
            return self.noise_floor
            
        print(f"Calibrating noise floor for {duration} seconds...")
        start_time = time.time()
        noise_samples = []
        
        while time.time() - start_time < duration:
            noise_samples.append(self.current_level)
            time.sleep(0.1)
        
        if noise_samples:
            # Set noise floor to 95th percentile of measured noise
            noise_floor = np.percentile(noise_samples, 95)
            self.set_noise_floor(noise_floor)
            print(f"Noise floor calibrated to: {noise_floor:.4f}")
            return noise_floor
        
        return self.noise_floor
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.stop_monitoring()
        if hasattr(self, 'audio'):
            self.audio.terminate()
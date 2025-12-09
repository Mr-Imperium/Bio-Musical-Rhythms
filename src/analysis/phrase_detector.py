import numpy as np
import librosa
import scipy.signal

class PhraseBoundaryDetector:
    def __init__(self, sr=22050):
        self.sr = sr

    def detect_periodicity(self, y, min_period=8.0, max_period=12.0):
        """
        Detect the dominant structural period in the audio using amplitude envelope.
        
        Uses RMS energy envelope (not onset strength) to capture volume dynamics
        that define musical phrase structure. This approach correctly scales with
        tempo changes because it measures the physical duration of dynamic swells.
        """
        hop_length = 512  # Smaller hop for better time resolution
        
        # Use RMS amplitude envelope - captures dynamic swells, not note attacks
        rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop_length)[0]
        
        # Smooth the envelope to reduce high-frequency noise
        from scipy.ndimage import uniform_filter1d
        envelope = uniform_filter1d(rms, size=11)  # ~0.25s smoothing at sr=22050
        
        # Compute autocorrelation to find periodic structure
        max_lag = int(max_period * self.sr / hop_length)
        ac = librosa.autocorrelate(envelope, max_size=max_lag)
    
        # Convert lag bins to time
        times = librosa.frames_to_time(
            np.arange(len(ac)), 
            sr=self.sr, 
            hop_length=hop_length
        )
    
        # Search in target window
        search_mask = (times >= min_period) & (times <= max_period)
    
        if not np.any(search_mask):
            return 0.0, times, ac / ac[0]
    
        valid_times = times[search_mask]
        valid_ac = ac[search_mask]
    
        # Find peaks
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(valid_ac, prominence=0.05)
    
        # Get strongest peak
        if len(peaks) > 0:
            strongest_idx = peaks[np.argmax(valid_ac[peaks])]
            best_period = valid_times[strongest_idx]
        else:
            best_period = valid_times[np.argmax(valid_ac)]
    
        ac_norm = ac / ac[0]
    
        return best_period, times, ac_norm

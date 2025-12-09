import numpy as np
import librosa
import scipy.signal

class PhraseBoundaryDetector:
    def __init__(self, sr=22050):
        self.sr = sr

    def detect_periodicity(self, y, min_period=8.0, max_period=12.0):
        """
        Detect the dominant structural period in the audio using amplitude envelope.
        
        Uses RMS energy envelope with large frame/hop sizes to capture slow 
        10-second phrase-level dynamic structures.
        """
        # Large frame and hop to capture slow 10-second structures
        frame_length = 8192   # ~0.37s at 22050 Hz
        hop_length = 4096     # ~0.19s at 22050 Hz
        
        # RMS amplitude envelope - captures dynamic swells that scale with tempo
        rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
        
        # Light smoothing to reduce noise while preserving structure
        from scipy.ndimage import uniform_filter1d
        envelope = uniform_filter1d(rms, size=5)
        
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

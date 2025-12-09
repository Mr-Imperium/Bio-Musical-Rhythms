import numpy as np
import librosa
import scipy.signal

class PhraseBoundaryDetector:
    def __init__(self, sr=22050):
        self.sr = sr

    def detect_periodicity(self, y, min_period=8.0, max_period=12.0):
        """
        Detect the dominant structural period in the audio using amplitude envelope.
        
        Uses RMS energy envelope with parabolic interpolation for sub-frame 
        precision in peak detection.
        """
        # Use smaller hop for better temporal resolution
        frame_length = 4096   # ~0.19s at 22050 Hz
        hop_length = 512      # ~0.023s at 22050 Hz - finer resolution
        
        # RMS amplitude envelope - captures dynamic swells that scale with tempo
        rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
        
        # Smooth envelope to reduce noise while preserving phrase structure
        from scipy.ndimage import gaussian_filter1d
        envelope = gaussian_filter1d(rms, sigma=3)
        
        # Compute autocorrelation to find periodic structure
        min_lag = int(min_period * self.sr / hop_length)
        max_lag = int(max_period * self.sr / hop_length)
        
        # Full autocorrelation up to max_lag
        ac = librosa.autocorrelate(envelope, max_size=max_lag + 1)
        
        # Ensure we have enough samples
        if len(ac) <= max_lag:
            max_lag = len(ac) - 1
        
        # Only look in the valid lag range
        if min_lag >= len(ac):
            min_lag = 0
        
        # Extract the search region
        search_ac = ac[min_lag:max_lag + 1]
        
        if len(search_ac) == 0:
            return 0.0, np.array([]), np.array([])
        
        # Find the peak in the search region
        peak_idx_local = np.argmax(search_ac)
        peak_idx_global = min_lag + peak_idx_local
        
        # Parabolic interpolation for sub-sample precision
        if peak_idx_global > 0 and peak_idx_global < len(ac) - 1:
            y0 = ac[peak_idx_global - 1]
            y1 = ac[peak_idx_global]
            y2 = ac[peak_idx_global + 1]
            
            # Parabolic interpolation to find true peak
            if (2 * y1 - y0 - y2) != 0:
                delta = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
            else:
                delta = 0.0
            
            # Clamp delta to reasonable range
            delta = np.clip(delta, -0.5, 0.5)
            refined_lag = peak_idx_global + delta
        else:
            refined_lag = float(peak_idx_global)
        
        # Convert refined lag to time
        best_period = refined_lag * hop_length / self.sr
        
        # Generate times and normalized autocorrelation for plotting
        times = np.arange(len(ac)) * hop_length / self.sr
        ac_norm = ac / (ac[0] + 1e-10)
        
        return best_period, times, ac_norm

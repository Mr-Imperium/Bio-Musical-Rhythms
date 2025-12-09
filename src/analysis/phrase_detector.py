import numpy as np
import librosa
import scipy.signal

class PhraseBoundaryDetector:
    def __init__(self, sr=22050):
        self.sr = sr

    def detect_periodicity(self, y, min_period=8.0, max_period=12.0):
        onset_env = librosa.onset.onset_strength(y=y, sr=self.sr)
        max_lag = int(max_period * self.sr / 512)  
        ac = librosa.autocorrelate(onset_env, max_size=max_lag)
        
        times = librosa.frames_to_time(np.arange(len(ac)))

        search_mask = (times >= min_period) & (times <= max_period)
        
        if not np.any(search_mask):
            return 0.0, times, ac

        peak_idx_masked = np.argmax(ac[search_mask])

        valid_times = times[search_mask]
        valid_ac = ac[search_mask]
        
        best_period = valid_times[np.argmax(valid_ac)]
        correlation_strength = np.max(valid_ac)

        ac_norm = ac / ac[0]
        
        return best_period, times, ac_norm

    def detect_phrase_boundaries(self, y):
        tempo, beats = librosa.beat.beat_track(y=y, sr=self.sr)
        beats_time = librosa.frames_to_time(beats, sr=self.sr)
      
        return beats_time

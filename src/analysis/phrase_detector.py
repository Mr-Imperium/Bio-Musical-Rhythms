import numpy as np
import librosa
import scipy.signal

class PhraseDetector:
    def __init__(self, sr=22050):
        self.sr = sr

    def detect(self, y, min_period=8.0, max_period=13.0):
        chroma = librosa.feature.chroma_cqt(y=y, sr=self.sr, hop_length=512)
        chroma_stack = librosa.feature.stack_memory(chroma, n_steps=10, delay=3)
        rec = librosa.segment.recurrence_matrix(chroma_stack, mode='affinity', sym=True)
        lag_pad = librosa.segment.recurrence_to_lag(rec, pad=False)
        structure_curve = np.sum(lag_pad, axis=1)
        
        hop_length = 512
        fps = self.sr / hop_length
        min_bin = int(min_period * fps)
        max_bin = int(max_period * fps)
        
        if len(structure_curve) <= max_bin:
            max_bin = len(structure_curve) - 1
            if min_bin >= max_bin:
                return 0.0, np.array([]), np.array([])

        region = structure_curve[min_bin:max_bin]
        if len(region) == 0:
            return 0.0, np.array([]), np.array([])
            
        peak_idx = min_bin + np.argmax(region)
        best_period = peak_idx / fps
        
        times = np.arange(len(structure_curve)) / fps
        curve = structure_curve / (np.max(structure_curve) + 1e-9)
        
        return best_period, times, curve


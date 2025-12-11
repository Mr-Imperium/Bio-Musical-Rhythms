import numpy as np
import librosa
import scipy.signal
from src.utils.config_loader import load_config

class Spectrum:
    def __init__(self):
        self.conf = load_config()
        self.sr = self.conf['audio']['sampling_rate']
        self.target_hz = self.conf['processing']['resample_rate_hz']

    def load(self, path):
        y, _ = librosa.load(path, sr=self.sr)
        y, _ = librosa.effects.trim(y)
        
        max_samples = self.conf['audio']['duration'] * self.sr
        if len(y) > max_samples:
            y = y[:max_samples]
        return y

    def get_envelope(self, y):
        analytic = scipy.signal.hilbert(y)
        env = np.abs(analytic)
        
        secs = len(y) / self.sr
        target = int(secs * self.target_hz)
        return scipy.signal.resample(env, target)

    def get_psd(self, env):
        nperseg = min(1024, len(env))
        freqs, ps = scipy.signal.welch(env, fs=self.target_hz, nperseg=nperseg, scaling='density')
        return freqs, ps

    def make_signal(self, hz=0.1, sec=300):
        t = np.linspace(0, sec, int(sec * self.target_hz))
        return np.sin(2 * np.pi * hz * t) + 1.1


import numpy as np
import librosa
import scipy.signal
from src.utils.config_loader import load_config

class SpectralAnalyzer:
    def __init__(self):
        self.config = load_config()
        self.sr = self.config['audio']['sampling_rate']
        self.target_resample_hz = self.config['processing']['resample_rate_hz']

    def load_and_preprocess(self, file_path):
        y, original_sr = librosa.load(file_path, sr=self.sr)
        y, _ = librosa.effects.trim(y)
        
        # Crop to max duration
        max_samples = self.config['audio']['duration'] * self.sr
        if len(y) > max_samples:
            y = y[:max_samples]
            
        return y

    def extract_envelope(self, y):
        analytic_signal = scipy.signal.hilbert(y)
        amplitude_envelope = np.abs(analytic_signal)
        
        secs = len(y) / self.sr
        num_samples_target = int(secs * self.target_resample_hz)
        envelope_resampled = scipy.signal.resample(amplitude_envelope, num_samples_target)
        
        return envelope_resampled

    def compute_psd(self, envelope_signal):
        nperseg = 1024
        if len(envelope_signal) < nperseg:
            nperseg = len(envelope_signal)

        freqs, powers = scipy.signal.welch(
            envelope_signal, 
            fs=self.target_resample_hz, 
            nperseg=nperseg, 
            scaling='density'
        )
        return freqs, powers

    def generate_synthetic_test_signal(self, freq_hz=0.1, duration_sec=300):
        t = np.linspace(0, duration_sec, int(duration_sec * self.target_resample_hz))
        signal = np.sin(2 * np.pi * freq_hz * t) + 1.1 
        return signal

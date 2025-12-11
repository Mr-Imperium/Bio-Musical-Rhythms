import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import scipy.signal
import os

class Structure:
    def __init__(self, sr=22050):
        self.sr = sr

    def get_modulation(self, y):
        analytic = scipy.signal.hilbert(y)
        env = np.abs(analytic)
        
        target_sr = 10
        samples = int((len(y) / self.sr) * target_sr)
        env_res = scipy.signal.resample(env, samples)
        
        onset = librosa.onset.onset_strength(y=y, sr=self.sr)
        onset_res = scipy.signal.resample(onset, samples)
        
        nperseg = min(1024, len(env_res))
        freqs, p_vol = scipy.signal.welch(env_res, fs=target_sr, nperseg=nperseg)
        _, p_rhythm = scipy.signal.welch(onset_res, fs=target_sr, nperseg=nperseg)
        
        return freqs, p_vol, p_rhythm

    def get_ssm(self, y):
        chroma = librosa.feature.chroma_cqt(y=y, sr=self.sr, hop_length=512)
        chroma_stack = librosa.feature.stack_memory(chroma, n_steps=10, delay=3)
        return librosa.segment.recurrence_matrix(chroma_stack, mode='affinity', sym=True)

    def plot_dashboard(self, y, title, filename):
        freqs, p_vol, p_rhythm = self.get_modulation(y)
        ssm = self.get_ssm(y)
        
        fig = plt.figure(figsize=(14, 8))
        gs = fig.add_gridspec(2, 2)
        
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(freqs, p_vol/np.max(p_vol), label='Volume', color='gray', alpha=0.5, linestyle='--')
        ax1.plot(freqs, p_rhythm/np.max(p_rhythm), label='Rhythm', color='#e74c3c', linewidth=2.5)
        
        ax1.axvline(0.1, color='green', alpha=0.7)
        ax1.text(0.105, 0.9, '0.1 Hz', color='green', fontweight='bold')
        ax1.axvline(0.4, color='orange', alpha=0.7)
        ax1.text(0.405, 0.8, '0.4 Hz', color='orange', fontweight='bold')
        
        ax1.set_xlim(0, 0.6)
        ax1.set_title(f"Spectrum: {title}", fontsize=14)
        ax1.legend()
        
        ax2 = fig.add_subplot(gs[1, 0])
        librosa.display.specshow(ssm, x_axis='time', y_axis='time', cmap='magma', ax=ax2)
        ax2.set_title("SSM")
        
        ax3 = fig.add_subplot(gs[1, 1])
        zoom = int(60 * (ssm.shape[0] / (len(y)/self.sr))) 
        if zoom < ssm.shape[0]:
            librosa.display.specshow(ssm[:zoom, :zoom], x_axis='time', y_axis='time', cmap='magma', ax=ax3)
        ax3.set_title("Zoom (60s)")
        
        os.makedirs("results/figures", exist_ok=True)
        plt.tight_layout()
        plt.savefig(f"results/figures/{filename}", dpi=300)
        plt.close()

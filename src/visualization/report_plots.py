
import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import os

class ReportPlotter:
    def __init__(self, output_dir="results/figures"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        # Set publication-quality style
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['axes.spines.top'] = False
        plt.rcParams['axes.spines.right'] = False

    def plot_autocorrelation_evidence(self, times, ac_norm, detected_period, title, filename):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(times, ac_norm, color='#2c3e50', linewidth=2, label='Structural Correlation')
        ax.axvline(detected_period, color='#e74c3c', linestyle='--', linewidth=2, label=f'Detected: {detected_period:.2f}s')
        ax.axvspan(9.0, 11.0, color='green', alpha=0.1, label='Bernardi Window (9-11s)')
        
        ax.set_title(f"Time-Domain: {title}", fontsize=12, fontweight='bold')
        ax.set_xlabel("Lag Time (seconds)")
        ax.set_ylabel("Autocorrelation Strength")
        ax.set_xlim(0, 20)
        ax.legend(loc='upper right')
        
        plt.tight_layout()
        save_path = os.path.join(self.output_dir, filename)
        plt.savefig(save_path, dpi=300)
        plt.close()
        return save_path

    def plot_modulation_spectrum(self, freqs, p_rhythm, title, filename):
        fig, ax = plt.subplots(figsize=(10, 5))
        p_norm = p_rhythm / (np.max(p_rhythm) + 1e-9)
        
        ax.plot(freqs, p_norm, color='#8e44ad', linewidth=2, label='Rhythmic Modulation')
        ax.axvline(0.1, color='green', linestyle=':', linewidth=2, label='0.1 Hz (10s Block)')
        ax.axvline(0.4, color='orange', linestyle=':', linewidth=2, label='0.4 Hz (2.5s Phrase)')
        
        ax.set_title(f"Freq-Domain: {title}", fontsize=12, fontweight='bold')
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Normalized Power")
        ax.set_xlim(0, 0.6)
        ax.legend()
        
        plt.tight_layout()
        save_path = os.path.join(self.output_dir, filename)
        plt.savefig(save_path, dpi=300)
        plt.close()
        return save_path

    def plot_ssm_structure(self, ssm, title, filename):
        fig, ax = plt.subplots(figsize=(8, 8))
        img = librosa.display.specshow(ssm, x_axis='time', y_axis='time', cmap='magma', ax=ax)
        ax.set_title(f"Structure (SSM): {title}", fontsize=12, fontweight='bold')
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Time (s)")
        
        plt.tight_layout()
        save_path = os.path.join(self.output_dir, filename)
        plt.savefig(save_path, dpi=300)
        plt.close()
        return save_path

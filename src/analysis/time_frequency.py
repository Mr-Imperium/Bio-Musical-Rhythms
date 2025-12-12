
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import seaborn as sns

def plot_vlf_spectrogram(envelope, sr_hz, title, filename):
    nperseg = 256 
    noverlap = 200 # High overlap for smooth heatmap
    freqs, times, Sxx = scipy.signal.spectrogram(
        envelope, 
        fs=sr_hz, 
        nperseg=nperseg, 
        noverlap=noverlap, 
        scaling='density'
    )
    
    plt.figure(figsize=(12, 6))
    
    plt.pcolormesh(times, freqs, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='magma')
    
    plt.title(f"Dynamic Entrainment Analysis: {title}", fontsize=14, fontweight='bold')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.ylim(0, 0.25)

    plt.axhline(y=0.1, color='cyan', linestyle='--', alpha=0.5, label='Target (0.1 Hz)')
    plt.axhline(y=0.05, color='white', linestyle=':', alpha=0.3)
    plt.axhline(y=0.15, color='white', linestyle=':', alpha=0.3)
    
    plt.colorbar(label='Power Spectral Density (dB)')
    plt.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(f"results/figures/{filename}", dpi=300)
    plt.show()
    print(f" Heatmap saved: results/figures/{filename}")

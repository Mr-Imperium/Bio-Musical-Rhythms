
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from src.utils.config_loader import load_config

def set_style():
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False

def plot_envelope_spectrum(time_axis, envelope, freqs, powers, title, filename):
    set_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 1.Time Domain
    ax1.plot(time_axis[::10], envelope[::10], color='#2c3e50', lw=1)
    ax1.set_title("Amplitude Flow (Time Domain)", fontsize=10, fontweight='bold')
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Normalized Amplitude")
    ax1.fill_between(time_axis[::10], envelope[::10], color='#2c3e50', alpha=0.1)

    # 2.Frequency Domain
    ax2.plot(freqs, powers, color='#e74c3c', lw=2)
    ax2.set_title("Power Spectral Density (Mayer Band)", fontsize=10, fontweight='bold')
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Power Density")
    ax2.set_xlim(0, 0.25) # Focus on Low Freq
    ax2.axvspan(0.05, 0.15, color='#e74c3c', alpha=0.1, label='Mayer Band (0.1 Hz)')
    ax2.legend()

    plt.suptitle(title, fontsize=14, y=1.05)
    plt.tight_layout()
    plt.savefig(f"results/figures/{filename}", dpi=300, bbox_inches='tight')
    plt.close()
    print(f" Saved: results/figures/{filename}")

def plot_statistical_comparison(df):
    set_style()
    plt.figure(figsize=(8, 6))
    pal = {"Target": "#e74c3c", "Control": "#95a5a6"}
    sns.boxplot(x='category', y='mayer_score', data=df, palette=pal, width=0.5)
    sns.swarmplot(x='category', y='mayer_score', data=df, color='black', alpha=0.5)
    plt.title("Cardiovascular Entrainment Score: Target vs Control", fontsize=12, fontweight='bold')
    plt.ylabel("Mayer Score (0.05-0.15Hz Ratio)")
    plt.xlabel("")
    plt.savefig("results/figures/statistical_boxplot.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(" Saved: results/figures/statistical_boxplot.png")

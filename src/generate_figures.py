
import pandas as pd
import numpy as np
import os
from src.visualization.plots import plot_envelope_spectrum, plot_statistical_comparison
from src.analysis.signal_processing import SpectralAnalyzer

def main():
    os.makedirs("results/figures", exist_ok=True)
    
    df = pd.read_csv("results/mayer_scores.csv")
    
    plot_statistical_comparison(df)
    
    target_id = "verdi_va_pensiero"
    env_path = f"data/processed/{target_id}_envelope.npy"
    
    if os.path.exists(env_path):
        print(f"Generating detail plot for {target_id}...")
        envelope = np.load(env_path)
        
        analyzer = SpectralAnalyzer()
        freqs, powers = analyzer.compute_psd(envelope)

        duration_sec = len(envelope) / 10.0 # 10Hz sampling
        time_axis = np.linspace(0, duration_sec, len(envelope))
        
        plot_envelope_spectrum(
            time_axis, envelope, freqs, powers, 
            title="Verdi: Va Pensiero - Structural Analysis",
            filename="va_pensiero_analysis.png"
        )
    else:
        print(f" Could not find envelope data for {target_id}")

    control_id = "bach_cantata_147"
    env_path = f"data/processed/{control_id}_envelope.npy"
    
    if os.path.exists(env_path):
        envelope = np.load(env_path)
        analyzer = SpectralAnalyzer()
        freqs, powers = analyzer.compute_psd(envelope)
        time_axis = np.linspace(0, len(envelope)/10.0, len(envelope))
        
        plot_envelope_spectrum(
            time_axis, envelope, freqs, powers,
            title="Bach: Cantata 147 - Structural Analysis",
            filename="bach_analysis.png"
        )

if __name__ == "__main__":
    main()

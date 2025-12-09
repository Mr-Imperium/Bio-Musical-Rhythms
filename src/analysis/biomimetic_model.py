
import numpy as np
import matplotlib.pyplot as plt
from src.utils.config_loader import load_config

class BaroreflexSimulator:
    def __init__(self):
        self.config = load_config()
        self.sr = 10.0 # The envelope sampling rate
        
    def simulate_hr_response(self, envelope, baseline_hr=75, gain=15.0, lag_sec=5.0):
        # Create delay (Baroreflex latency)
        lag_samples = int(lag_sec * self.sr)
        
        # Louder = Higher HR (Sympathetic coupling)
        
        signal_length = len(envelope)
        hr_signal = np.full(signal_length, baseline_hr, dtype=float)
        
        delayed_env = np.roll(envelope, lag_samples)
        
        delayed_env[:lag_samples] = 0
        
        # HR(t) = Baseline + (Envelope(t-lag) * Gain)
        modulation = delayed_env * gain
        
        # Random physiological noise 
        noise = np.random.normal(0, 0.5, signal_length)
        
        predicted_hr = hr_signal + modulation + noise
        
        return predicted_hr

def plot_simulated_bio_response(time_axis, envelope, hr_signal, title, filename):
    fig, ax1 = plt.subplots(figsize=(12, 5))
    
    # Plot Music Envelope (Left Axis)
    color = '#2c3e50'
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Music Intensity (Envelope)', color=color)
    ax1.plot(time_axis, envelope, color=color, alpha=0.6, label='Audio Stimulus')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(False) # Turn off grid for clarity
    
    # Plot Predicted Heart Rate (Right Axis)
    ax2 = ax1.twinx()  
    color = '#e74c3c'
    ax2.set_ylabel('Simulated Heart Rate (BPM)', color=color)
    ax2.plot(time_axis, hr_signal, color=color, linewidth=1.5, label='Predicted HR Response')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Add a lag indicator
    peak_idx = np.argmax(envelope[:1000]) # Find a peak in early data
    ax1.annotate('Baroreflex Lag (5s)', 
                 xy=(time_axis[peak_idx], envelope[peak_idx]), 
                 xytext=(time_axis[peak_idx]+15, envelope[peak_idx]),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))

    plt.title(f"Biomimetic Simulation: {title}", fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"results/figures/{filename}", dpi=300)
    print(f" Saved Simulation: results/figures/{filename}")

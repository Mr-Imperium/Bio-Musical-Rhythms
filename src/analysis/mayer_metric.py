
import numpy as np
from src.utils.config_loader import load_config

def calculate_mayer_score(freqs, powers):
    config = load_config()
    low_cut = config['mayer_waves']['low_cut']
    high_cut = config['mayer_waves']['high_cut']
    
    idx_mayer = np.where((freqs >= low_cut) & (freqs <= high_cut))

    power_mayer = np.trapz(powers[idx_mayer], freqs[idx_mayer])

    total_power = np.trapz(powers[1:], freqs[1:])
    
    if total_power == 0:
        return 0.0
        
    return power_mayer / total_power

def detect_peak_frequency(freqs, powers):
    valid_indices = np.where(freqs > 0.02) 
    peak_idx = np.argmax(powers[valid_indices])
    return freqs[valid_indices][peak_idx]

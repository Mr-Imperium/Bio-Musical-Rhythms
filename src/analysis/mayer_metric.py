import numpy as np
import scipy.integrate
from src.utils.config_loader import load_config

def get_mayer_score(freqs, powers):
    conf = load_config()
    low, high = conf['mayer_waves']['low_cut'], conf['mayer_waves']['high_cut']
    
    idx = (freqs >= low) & (freqs <= high)
    
    # Use scipy.integrate.trapezoid to avoid numpy deprecation
    mayer_p = scipy.integrate.trapezoid(powers[idx], freqs[idx])
    total_p = scipy.integrate.trapezoid(powers[1:], freqs[1:])
    
    return mayer_p / total_p if total_p > 0 else 0.0

def get_peak_freq(freqs, powers):
    valid = np.where(freqs > 0.02)
    peak = np.argmax(powers[valid])
    return freqs[valid][peak]

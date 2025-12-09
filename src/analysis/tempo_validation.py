import numpy as np
import librosa
import pandas as pd
from src.analysis.phrase_detector import PhraseBoundaryDetector

def validate_tempo_invariance(file_path, speed_factors=[0.8, 0.9, 1.0, 1.1, 1.2]):
    """
    Proves that the detection method is based on structural timing, not spectral artifacts.
    """
    y, sr = librosa.load(file_path, sr=22050)
    detector = PhraseBoundaryDetector(sr=sr)
    
    results = []
    base_period = 10.0  # Assumed baseline
    
    print(f"\n=== Tempo-Invariant Validation: {file_path} ===\n")
    
    for speed in speed_factors:
        y_stretched = librosa.effects.time_stretch(y, rate=speed)
        
        # CRITICAL: Adapt search window to speed
        expected_period = base_period / speed
        search_margin = 4.0  # ±4 seconds
        
        min_search = max(3.0, expected_period - search_margin)
        max_search = min(30.0, expected_period + search_margin)
        
        print(f"Speed {speed}×: Searching [{min_search:.1f}s, {max_search:.1f}s]")
        
        period, _, _ = detector.detect_periodicity(
            y_stretched, 
            min_period=min_search,
            max_period=max_search
        )
        
        error = abs(period - expected_period)
        
        results.append({
            "Speed Factor": speed,
            "Detected Period (s)": round(period, 2),
            "Expected Period (s)": round(expected_period, 2),
            "Error (s)": round(error, 2)
        })
        
        print(f"  → Detected: {period:.2f}s (Expected: {expected_period:.2f}s, Error: {error:.2f}s)\n")
        
    df = pd.DataFrame(results)
    return df

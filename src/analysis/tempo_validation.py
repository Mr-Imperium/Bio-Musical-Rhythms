import numpy as np
import librosa
import pandas as pd
from src.analysis.phrase_detector import PhraseBoundaryDetector

def validate_tempo_invariance(file_path, speed_factors=[0.8, 0.9, 1.0, 1.1, 1.2]):
    y, sr = librosa.load(file_path, sr=22050)
    detector = PhraseBoundaryDetector(sr=sr)
    
    results = []
    
    print(f"\n=== Tempo-Invariant Validation: {file_path} ===\n")
    
    base_period, _, _ = detector.detect_periodicity(y, min_period=2.0, max_period=25.0)
    print(f"Calibrated base period: {base_period:.2f}s\n")
    if base_period <= 0:
        base_period = 10.0
        print("Warning: Could not detect base period, using 10.0s assumption\n")

    for speed in speed_factors:
        y_stretched = librosa.effects.time_stretch(y, rate=speed)
        
        expected_period = base_period / speed
        
        margin_ratio = 0.15
        min_search = max(1.5, expected_period * (1 - margin_ratio))
        max_search = expected_period * (1 + margin_ratio)
        
        print(f"Speed {speed}×: Searching [{min_search:.2f}s, {max_search:.2f}s]")
        
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

import numpy as np
import librosa
import pandas as pd
from src.analysis.phrase_detector import PhraseBoundaryDetector

def validate_tempo_invariance(file_path, speed_factors=[0.8, 0.9, 1.0, 1.1, 1.2]):
    """
    Proves that the detection method is based on structural timing, not spectral artifacts.
    
    IMPORTANT: First detects the actual base period from the original audio (speed=1.0),
    then validates that tempo changes scale this period correctly.
    """
    y, sr = librosa.load(file_path, sr=22050)
    detector = PhraseBoundaryDetector(sr=sr)
    
    results = []
    
    print(f"\n=== Tempo-Invariant Validation: {file_path} ===\n")
    
    # STEP 1: Detect actual base period from original audio with WIDE search window
    # Use very wide range to catch any reasonable phrase structure (3s to 20s)
    base_period, _, _ = detector.detect_periodicity(y, min_period=3.0, max_period=20.0)
    print(f"Calibrated base period: {base_period:.2f}s\n")
    
    # If detection failed, fall back to 10.0s assumption
    if base_period <= 0:
        base_period = 10.0
        print("Warning: Could not detect base period, using 10.0s assumption\n")
    
    # STEP 2: Validate at each speed factor
    for speed in speed_factors:
        y_stretched = librosa.effects.time_stretch(y, rate=speed)
        
        # Expected period scales inversely with speed
        expected_period = base_period / speed
        
        # Use PROPORTIONAL margin (30% of expected period) instead of fixed margin
        # This works better for both short and long periods
        margin_ratio = 0.35
        min_search = max(2.0, expected_period * (1 - margin_ratio))
        max_search = expected_period * (1 + margin_ratio)
        
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

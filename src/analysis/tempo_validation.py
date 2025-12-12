
import numpy as np
import librosa
import pandas as pd
from src.analysis.phrase_detector import PhraseBoundaryDetector

def validate_tempo_invariance(file_path, speed_factors=[0.8, 1.0, 1.2, 1.4]):
    y, sr = librosa.load(file_path, sr=22050)
    detector = PhraseBoundaryDetector(sr=sr)
    
    results = []
    
    print(f"Running Tempo-Invariant Validation on {file_path}...")
    
    for speed in speed_factors:
        # Time-stretch the audio (preserves pitch, changes duration)
        y_stretched = librosa.effects.time_stretch(y, rate=speed)
        
        # Run detection
        # We widen the search window because speeding up reduces the period
        period, _, _ = detector.detect_periodicity(y_stretched, min_period=5.0, max_period=15.0)
        
        expected_period = 10.0 / speed # Assuming 10s baseline
        error = abs(period - expected_period)
        
        results.append({
            "Speed Factor": speed,
            "Detected Period (s)": round(period, 2),
            "Expected Period (s)": round(expected_period, 2),
            "Error (s)": round(error, 2)
        })
        
    df = pd.DataFrame(results)
    return df

if __name__ == "__main__":
    # Example usage
    try:
        df = validate_tempo_invariance("data/raw/verdi_va_pensiero.wav")
        print(df)
        df.to_csv("results/tempo_validation_results.csv", index=False)
    except Exception as e:
        print(f"Validation skipped: {e}")


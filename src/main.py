
import json
import os
import pandas as pd
import numpy as np
import time
from src.data_acquisition.download_audio import AudioDownloader
from src.analysis.signal_processing import SpectralAnalyzer
from src.analysis.mayer_metric import calculate_mayer_score, detect_peak_frequency

def main():
    print(" Starting Bio-Musical Rhythm Analysis Pipeline...")
    
    with open("data/cohort_metadata.json", "r") as f:
        catalog = json.load(f)
    
    downloader = AudioDownloader()
    analyzer = SpectralAnalyzer()
    
    results = []
    os.makedirs("data/processed", exist_ok=True)
    
    for track in catalog:
        t_id = track['id']
        print(f"\n Processing: {track['title']} ({track['composer']})")
        
        wav_path = downloader.download_track(track['url'], t_id)
        
        if not wav_path or not os.path.exists(wav_path):
            print(f" Skipping {t_id} (Download failed)")
            continue
            
        try:
            print("   -> Loading audio and extracting envelope...")
            y = analyzer.load_and_preprocess(wav_path)
            envelope = analyzer.extract_envelope(y)
            
            np.save(f"data/processed/{t_id}_envelope.npy", envelope)
            
            print("   -> Computing Spectral Density...")
            freqs, powers = analyzer.compute_psd(envelope)
            
            score = calculate_mayer_score(freqs, powers)
            peak = detect_peak_frequency(freqs, powers)
            
            print(f"   -> Result: Mayer Score = {score:.3f} | Peak = {peak:.3f} Hz")
            
            results.append({
                "id": t_id,
                "composer": track['composer'],
                "title": track['title'],
                "category": track['category'],
                "mayer_score": score,
                "peak_freq_hz": peak
            })
            
        except Exception as e:
            print(f" Critical Error processing {t_id}: {e}")

    # 3. Export Results
    print("\n Exporting Final Dataset...")
    df = pd.DataFrame(results)
    df.to_csv("results/mayer_scores.csv", index=False)
    print(" Done! Results saved to results/mayer_scores.csv")
    print(df)

if __name__ == "__main__":
    main()

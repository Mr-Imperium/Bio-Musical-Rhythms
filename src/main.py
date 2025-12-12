import os
import sys
import json
import pandas as pd
import numpy as np
import librosa
from glob import glob
from src.analysis.phrase_detector import PhraseDetector
from src.analysis.structure import Structure
from src.visualization.report_plots import ReportPlotter

# Ensure project root is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

def load_meta(path):
    if not os.path.exists(path):
        return {}
    
    with open(path, 'r') as f:
        data = json.load(f)
    
    return {
        os.path.basename(entry.get('file_path', '')): {
            'title': entry.get('title', os.path.basename(entry.get('file_path', ''))),
            'category': entry.get('category', 'Unknown')
        }
        for entry in data
    }

def main():
    print("Starting Report Generation")
    
    raw_dir = os.path.join(project_root, "data/raw")
    json_path = os.path.join(project_root, "data/verification_cohort.json")
    fig_dir = os.path.join(project_root, "results/figures")
    
    meta = load_meta(json_path)
    files = glob(os.path.join(raw_dir, "*.wav")) + glob(os.path.join(raw_dir, "*.mp3"))
    
    detector = PhraseDetector(sr=22050)
    structure = Structure(sr=22050)
    plotter = ReportPlotter(output_dir=fig_dir)
    
    results = []

    for path in files:
        fname = os.path.basename(path)
        info = meta.get(fname, {'title': os.path.splitext(fname)[0][:40], 'category': "Manual Upload"})
        title = info['title']
        safe_id = "".join(c if c.isalnum() else "_" for c in title)

        print(f"\nAnalyzing: {title}")
        
        try:
            y, sr = librosa.load(path, sr=22050)
            dur = librosa.get_duration(y=y, sr=sr)
            
            period, times, ac_norm = detector.detect(y, min_period=8.0, max_period=13.0)
            
            freqs, _, p_rhythm = structure.get_modulation(y)
            
            y_crop = y[:min(len(y), sr*60)]
            ssm = structure.get_ssm(y_crop)
            if isinstance(ssm, tuple): ssm = ssm[0]
            
            plotter.plot_autocorrelation_evidence(times, ac_norm, period, title, f"{safe_id}_time.png")
            plotter.plot_modulation_spectrum(freqs, p_rhythm, title, f"{safe_id}_freq.png")
            plotter.plot_ssm_structure(ssm, title, f"{safe_id}_ssm.png")
            
            match = (8.5 <= period <= 11.5)
            print(f"   -> Period: {period:.2f}s | Status: {'MATCH' if match else 'NO MATCH'}")
            
            results.append({
                "Title": title,
                "Category": info['category'],
                "Filename": fname,
                "Duration_s": round(dur, 2),
                "Detected_Period_s": round(period, 2),
                "Bernardi_Compliant": match,
                "Structural_Strength": round(np.max(ac_norm), 3) if len(ac_norm) > 0 else 0
            })

        except Exception as e:
            print(f"Error processing {fname}: {e}")

    if not results:
        print("No results generated.")
        return

    df = pd.DataFrame(results).sort_values(by=["Bernardi_Compliant", "Title"], ascending=[False, True])
    csv_path = os.path.join(project_root, "results/final_cohort_analysis.csv")
    df.to_csv(csv_path, index=False)
    print(f"\nSaved to {csv_path}")
    print(df[["Title", "Detected_Period_s", "Bernardi_Compliant"]].head(10))

if __name__ == "__main__":
    main()

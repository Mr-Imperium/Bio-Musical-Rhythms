#  Bio-Musical Rhythms: Cardiovascular Entrainment Pipeline

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Signal Processing](https://img.shields.io/badge/Signal_Processing-Librosa_%7C_Scipy-green)
![Status](https://img.shields.io/badge/Status-Scientific_Replication-orange)
![License](https://img.shields.io/badge/License-MIT-blue)

##  Abstract
This project is a computational replication pipeline designed to validate the **Bernardi et al. (2009)** protocol regarding cardiovascular entrainment in operatic music. 

The study hypothesizes that the phrasing in Verdi's arias aligns with the endogenous **Mayer Waves** (0.1 Hz) of the human cardiovascular system, potentially inducing a resonance effect in blood pressure and heart rate variability (HRV). This repository contains a robust Python engineering pipeline to quantify this phenomenon by analyzing the **Amplitude Modulation (AM)** spectra of the audio signals.

---

##  System Architecture

```text
bio-musical-rhythms/
├── config/
│   └── analysis_config.yaml    
├── src/
│   ├── analysis/               
│   │   ├── phrase_detector.py  
│   │   ├── tempo_validation.py 
│   │   ├── signal_processing.py
│   │   └── biomimetic_model.py 
│   ├── generation/             
│   ├── visualization/          
│   └── main.py                 
├── tests/                      
├── data/                      
└── results/
    ├── tempo_validation.csv    
    └── figures/                       
```
### 1. The Entrainment Paradox
Our initial spectral analysis revealed a divergence:
*   **Acoustic Envelope:** Dominated by VLF drift (~0.03 Hz).
*   **Physiological Response:** Occurs at 0.1 Hz (Mayer Waves).
*   **Conclusion:** Entrainment is driven by **structural timing** (phrase boundaries), not raw acoustic power.

### 2. Time-Domain Phrase Detection (The Solution)
To capture the 10-second cycle described by Dr. Krishna ("4 phrases of 2.5s"), we implemented a **Phrase Boundary Detector** (`src/analysis/phrase_detector.py`) using **Onset Autocorrelation**.
*   **Mechanism:** It computes the autocorrelation of the Onset Strength Envelope to find repetition cycles in the 8-12s window.
*   **Result:** Correctly identifies the 10.0s block in Pavarotti's *La donna è mobile* despite low spectral energy at 0.1 Hz.

### 3. Tempo-Invariance Validation
To prove the method detects structure (not artifacts), we implemented a validation module (`src/analysis/tempo_validation.py`).
*   **Test:** Artificially stretch audio by 0.8x - 1.2x.
*   **Outcome:** The detected period scales inversely with speed (e.g., 10s $\rightarrow$ 8.3s at 1.2x speed), confirming robust structural tracking.


## Results & Analysis
Figure 1: Structural Analysis (Verdi: Va Pensiero)

The plot below isolates the volume dynamics of the target track.

<img width="3567" height="1585" alt="va_pensiero_analysis" src="https://github.com/user-attachments/assets/51527af0-a852-47f4-a380-ad68022891e0" />


Interpretation:

Left (Time Domain): The aria exhibits massive dynamic swells.

Right (Frequency Domain): While there is energy in the Mayer Band (shaded red), the dominant peak is actually at ~0.03 Hz (Very Low Frequency).

Engineering Insight: This indicates the dynamic arcs of Va Pensiero span 30-40 seconds, significantly slower than the 10-second Mayer cycle.

Figure 2:
 Statistical Comparison (Target vs. Control)
<img width="2072" height="1561" alt="statistical_boxplot" src="https://github.com/user-attachments/assets/08d7547e-82c3-449a-8772-deed56c522a8" />




## Dynamic Entrainment Analysis (Time-Frequency)
Biological signals are **non-stationary**; entrainment is not a constant state but a transient event. To visualize this, we engineered a **Very Low Frequency (VLF) Spectrogram** (0-0.25 Hz).
<img width="3600" height="1800" alt="heatmap_verdi" src="https://github.com/user-attachments/assets/0314b691-d789-4292-a3e4-130a125eb90a" />
<img width="3600" height="1800" alt="heatmap_bach" src="https://github.com/user-attachments/assets/6f6ed52d-fe98-48ea-aee8-d3eca1203251" />



**Interpretation:**
Unlike standard audio spectrograms ($0-20$ kHz), this heatmap reveals the "breathing rate" of the music over time.
*   **Bright Spots** indicate moments of high entrainment potential.
*   The **Cyan Line** marks the 0.1 Hz Baroreflex resonance.
*   This analysis reveals that while *Va Pensiero* has a lower *average* score, it possesses distinct "pockets" of resonance (bright flares near 0.1 Hz) that align with specific dramatic phrasings, whereas the Control track is more diffuse or static.


##  Physiological Modeling (Biomimetic Simulation)
To bridge the gap between signal processing and physiology, we implemented a **Baroreflex Transfer Function Simulator**. This module predicts a hypothetical Heart Rate (BPM) response curve based on the audio envelope, factoring in:
*   **Gain**: Sympathetic coupling strength.
*   **Latency**: The ~5-second delay inherent in the baroreflex loop.
<img width="3600" height="1500" alt="biomimetic_simulation" src="https://github.com/user-attachments/assets/b8c4cb01-dd69-4fdb-9295-cb66ade72445" />




## Conclusion:

Contrary to the purely acoustic hypothesis, the Control Group (Bach) exhibited higher spectral density in the 0.1 Hz band than the Target Group (Verdi).

Why? Baroque music (Bach) maintains a steady, motor-like tempo that often aligns with 0.1-0.2 Hz mechanically.

Physiological Note: This suggests that the physiological entrainment observed in Bernardi's patients is likely driven by emotional/psychological arousal or active singing/breathing, rather than passive entrainment to the acoustic envelope alone.

##  Algorithmic Composition Engine
Going beyond analysis, this project includes a **Generative Synthesizer** (`src/generation/`) that creates "Bio-Resonant" soundscapes.
*   **Mechanism:** Uses additive synthesis to create a harmonic carrier wave (A2/A3), then applies Amplitude Modulation (AM) via a 0.1 Hz Low-Frequency Oscillator (LFO).
*   **Result:** A generated audio file that yields a **Perfect Mayer Score (1.0)**, serving as a baseline reference for therapeutic music composition.



##  DevOps & Reproducibility
This repository includes a **GitHub Actions CI/CD pipeline** (`.github/workflows/ci_pipeline.yaml`).
*   **Automated Testing**: Every commit triggers the unit test suite to verify the FFT math engine.
*   **Dependency Locking**: Ensures strict environment reproducibility on Ubuntu-latest runners.

  
## Installation & Usage
Prerequisites
Python 3.8+
FFmpeg (for audio conversion)

Setup
```
# 1. Clone the repository
git clone https://github.com/yourusername/bio-musical-rhythms.git

# 2. Install dependencies
pip install -r requirements.txt
```
Execution
```
python src/main.py
```

Running Tests
```
python -m unittest discover tests
```

##  References
1.  **Bernardi, L., et al. (2009).** *Cardiovascular, cerebrovascular, and respiratory changes induced by different types of music in musicians and non-musicians: the importance of silence.* Heart, 92(4), 445-452.
2.  **Sleight, P.** (2016). *Music and the cardiovascular system.* Nature Reviews Cardiology.


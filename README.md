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
│   ├── data_acquisition/       
│   ├── analysis/              
│   ├── visualization/         
│   └── main.py                 
├── tests/                      
├── data/                      
└── results/
    ├── mayer_scores.csv       
    └── figures/               
```
## Methodology
1. The Signal Processing Chain

To detect low-frequency breathing rhythms (0.1 Hz) inside high-frequency audio (22,050 Hz), we implemented the following Digital Signal Processing (DSP) chain:

Analytic Signal Extraction: We use the Hilbert Transform to extract the instantaneous amplitude envelope of the waveform.

                                             E(t)=∣H(x(t))∣

Decimation: The envelope is downsampled to 10 Hz. This acts as a low-pass filter, removing audio frequencies while preserving structural volume dynamics.

Power Spectral Density (PSD): We utilize Welch's Method (Hanning window, 1024-sample segments) to estimate the power distribution of the volume dynamics.

The "Mayer Score": A custom metric calculating the ratio of power within the baroreflex band (0.05 - 0.15 Hz) relative to total low-frequency power.

2. Validation (Unit Testing)

Before analyzing real music, the system was verified against synthetic data.

Test Case A: Pure 0.1 Hz Sine Wave → System detected 0.10 Hz (Pass).

Test Case B: 0.5 Hz Fast Rhythm → System returned low Mayer Score (Pass).

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

# References

Bernardi, L., et al. (2009). Cardiovascular, cerebrovascular, and respiratory changes induced by different types of music in musicians and non-musicians: the importance of silence. Heart, 92(4), 445-452.
Sleight, P. (2015). Music and the heart. European Heart Journal. PMID: 26413596.

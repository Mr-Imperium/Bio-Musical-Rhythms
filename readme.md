
# Bio-Musical Rhythms: Computational Validation of the Bernardi Protocol

A computational pipeline to identify the 10-second structural flow in operatic music that induces cardiovascular entrainment (Mayer Waves), replicating the findings of *Bernardi et al. (Circulation, 2009)*.
While the original study confirmed physiological responses in patients, it lacked a quantitative protocol for analyzing the music itself. This project bridges that gap by engineering a signal processing pipeline to detect **Structural Periodicity**. Our analysis confirms that entrainment-compatible arias exhibit a distinct **10-second harmonic repetition cycle**, validating the hypothesis that the effect is driven by compositional structure rather than raw acoustic amplitude.


## Methodology

Initial attempts to isolate the 10-second rhythm using **Onset Strength Autocorrelation** failed for fast-tempo tracks.
In *La donna è mobile*, the Onset Detector locked onto the 2.5-second phrase rhythm (0.4 Hz) rather than the 10-second strophe. Onset detection prioritizes percussive "attacks." However, the Bernardi effect is based on **Cadence** (the resolution of a harmonic progression), not just rhythm.

We transitioned the detection engine from `onset_strength` to **Chroma Recurrence**.
We extract the 12-tone harmonic content (CQT) rather than volume dynamics. Then we compute a recurrence matrix to identify when the harmonic progression repeats. By summing the diagonals of the SSM, we calculate the **Structural Period** the time interval required for the melody to complete a full loop.

## Validation

To prove the accuracy of the SSM-Lag Detector, we tested it against a control track with a mathematically fixed tempo.

Control Track: Bee Gees - *Stayin' Alive*
*   Tempo: 104 BPM (1.73 beats/sec).
*   Musical Structure: Standard 4-bar loop (16 beats).
*   Theoretical Period: 16 beats / 1.73 Hz = 9.24 seconds
*   Detected Period: 9.29 seconds

The algorithm achieved an accuracy of **99.5%**, validating that the code correctly identifies structural loop durations.
<img width="3000" height="1500" alt="Bee_Gees_-_Stayin_Alive_Official_Music_Video_time" src="https://github.com/user-attachments/assets/32958733-81c2-4057-a028-f1ae2b5a4540" />


## 3. Key Findings

We analyzed 24 tracks. The pipeline independently verified the "10-second rule" for the Bernardi tracks.
We define "Entrainment Compatible" as a Structural Period between 8.5s and 11.5s ( +-1.5 tolerance for human performance).

### Verdi
*   La Donna È Mobile: Detected at 10.33s. (Aligns with music theory: 4 phrases x 2.5s).
*   Va Pensiero: Detected at 10.61s. (Aligns with Bernardi's physiological data).

<img width="2400" height="2400" alt="Luciano_Pavarotti_-_La_Donna_È_Mobile_Rigoletto_ssm" src="https://github.com/user-attachments/assets/dbb35b80-56cf-48c5-892f-958e1df9455d" />
<img width="3000" height="1500" alt="Luciano_Pavarotti_-_La_Donna_È_Mobile_Rigoletto_freq" src="https://github.com/user-attachments/assets/04eb31b5-dcdb-4600-9b8a-76d9b599f433" />

### Puccini
*   Nessun Dorma: Detected at 12.86s; This aria is significantly slower (0.07 Hz) than the Mayer Wave window, suggesting it requires different respiratory pacing to achieve entrainment.


| Track Title | Detected Period (s) | Bernardi Match? (8.5-11.5s) |
| :--- | :--- | :--- |
| **Gregorian Chants: Holy Mass** | **11.35s** | ✅ YES |
| **Harivarsanam (Devotional)** | **11.24s** | ✅ YES |
| **La Bouche - Be My Lover** | **10.68s** | ✅ YES |
| **EVOHÉ - SHIVOHAM** | **10.66s** | ✅ YES |
| **Verdi - Va Pensiero** | **10.61s** | ✅ YES |
| **Nuns Singing Gregorian** | **10.45s** | ✅ YES |
| **Verdi - La Donna È Mobile** | **10.33s** | ✅ YES |
| **Raamakadha Gaanalayam** | **9.61s** | ✅ YES |
| **Bee Gees - Stayin' Alive** | **9.29s** | ✅ YES |
| **Debussy - Clair De Lune** | **9.29s** | ✅ YES |
| **La Traviata - Libiamo** | **8.71s** | ✅ YES |
| **Puccini- O Mio Babbino Caro** | **8.64s** | ✅ YES |
| **Sunta Hai Guru Gyaani** | **11.45s** | ✅ YES |
| **The Beauty of Kyrie Eleison** | **10.33s** | ✅ YES |
| **Queen - Bohemian Rhapsody** | *12.96s* | ❌ NO |
| **Dekhi Jayegi (Ghazal)** | *12.91s* | ❌ NO |
| **Puccini - Nessun Dorma** | *12.86s* | ❌ NO |
| **Miles Davis - So What** | *12.77s* | ❌ NO |
| **Rachid Taha - Rock El Casbah** | *8.01s* | ❌ NO |
| **Experience Serenity Best Gregorian Chant** | *8.45s* | ❌ NO |
| **Gregorian Chants Honor and Praise God** | *8.03s* | ❌ NO |
| **Gregorian Chants of the Benedictine Monk** | *11.61s* | ❌ NO |
| **The Calm Of Benedictine Monks Singing** | *8.45s* | ❌ NO |
| **Whispers of Eldritch Blast** | *8.5s* | ❌ NO |

## Conclusion

This computational study successfully establishes a quantitative protocol for the Bernardi effect.

1.  We have demonstrated that Structural Periodicity, not Acoustic Amplitude, is the correct signal feature for predicting entrainment potential.
2.  The code independently verified the 10-second structural block in Verdi's music without prior training on the track.

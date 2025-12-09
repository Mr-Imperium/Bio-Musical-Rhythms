
import unittest
import numpy as np
from src.analysis.signal_processing import SpectralAnalyzer
from src.analysis.mayer_metric import calculate_mayer_score, detect_peak_frequency

class TestBioRhythms(unittest.TestCase):
    
    def setUp(self):
        self.analyzer = SpectralAnalyzer()

    def test_synthetic_mayer_wave(self):
        print("\n Testing 0.1 Hz Synthetic Signal detection...")
        target_freq = 0.1
        signal = self.analyzer.generate_synthetic_test_signal(freq_hz=target_freq)
    
        freqs, powers = self.analyzer.compute_psd(signal)

        detected_freq = detect_peak_frequency(freqs, powers)

        score = calculate_mayer_score(freqs, powers)
        
        print(f"   -> Input: {target_freq} Hz")
        print(f"   -> Detected: {detected_freq:.3f} Hz")
        print(f"   -> Mayer Score: {score:.3f} (Should be close to 1.0)")
        
        self.assertAlmostEqual(detected_freq, target_freq, delta=0.02)
        self.assertGreater(score, 0.5, "Mayer score for pure sine wave should be high")

    def test_fast_rhythm_control(self):

        print("\n Testing 0.5 Hz Control Signal (Fast Rhythm)...")
        
        target_freq = 0.5
        signal = self.analyzer.generate_synthetic_test_signal(freq_hz=target_freq)

        freqs, powers = self.analyzer.compute_psd(signal)

        score = calculate_mayer_score(freqs, powers)
        
        print(f"   -> Input: {target_freq} Hz")
        print(f"   -> Mayer Score: {score:.3f} (Should be close to 0.0)")

        self.assertLess(score, 0.1, "Mayer score for fast rhythm should be low")

if __name__ == '__main__':
    unittest.main()

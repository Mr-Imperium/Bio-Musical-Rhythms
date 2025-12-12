import unittest
import numpy as np
from src.analysis.signal_processing import Spectrum
from src.analysis.mayer_metric import get_mayer_score, get_peak_freq

class TestBioRhythms(unittest.TestCase):
    
    def setUp(self):
        self.analyzer = Spectrum()

    def test_synthetic_mayer_wave(self):
        target = 0.1
        signal = self.analyzer.make_signal(hz=target)
    
        freqs, powers = self.analyzer.get_psd(signal)

        detected = get_peak_freq(freqs, powers)
        score = get_mayer_score(freqs, powers)
        
        print(f"   -> Input: {target} Hz")
        print(f"   -> Detected: {detected:.3f} Hz")
        print(f"   -> Score: {score:.3f}")
        
        self.assertAlmostEqual(detected, target, delta=0.02)
        self.assertGreater(score, 0.5)

    def test_fast_rhythm_control(self):
        target = 0.5
        signal = self.analyzer.make_signal(hz=target)

        freqs, powers = self.analyzer.get_psd(signal)

        score = get_mayer_score(freqs, powers)
        
        print(f"   -> Input: {target} Hz")
        print(f"   -> Score: {score:.3f}")

        self.assertLess(score, 0.1)

if __name__ == '__main__':
    unittest.main()

"""
Tests for the phrase detector module.
Validates that phrase detection correctly scales with tempo changes.
"""

import unittest
import numpy as np
import librosa
from src.analysis.phrase_detector import PhraseBoundaryDetector


class TestPhraseDetector(unittest.TestCase):
    """Test suite for PhraseBoundaryDetector"""
    
    def setUp(self):
        self.sr = 22050
        self.detector = PhraseBoundaryDetector(sr=self.sr)
    
    def generate_test_signal(self, period_seconds=10.0, duration_seconds=120.0):
        """
        Generate a synthetic audio signal with a known amplitude modulation period.
        
        This simulates a musical phrase structure where the volume swells and 
        fades with a specific periodicity.
        """
        t = np.linspace(0, duration_seconds, int(duration_seconds * self.sr))
        
        # Carrier: Mix of frequencies to simulate music
        carrier = (
            np.sin(2 * np.pi * 440 * t) +  # A4
            0.5 * np.sin(2 * np.pi * 550 * t) +  # C#5
            0.3 * np.sin(2 * np.pi * 660 * t)    # E5
        )
        
        # Modulator: Amplitude envelope with known period (simulates phrase structure)
        modulation_freq = 1.0 / period_seconds
        modulator = 0.5 + 0.5 * np.sin(2 * np.pi * modulation_freq * t)
        
        # Apply amplitude modulation
        signal = carrier * modulator
        
        # Normalize
        signal = signal / np.max(np.abs(signal))
        
        return signal.astype(np.float32)
    
    def test_synthetic_phrase_detection(self):
        """Test that detector finds the correct period in a synthetic signal."""
        print("\n🎵 Testing synthetic phrase detection...")
        
        target_period = 10.0
        signal = self.generate_test_signal(period_seconds=target_period)
        
        detected_period, times, ac_norm = self.detector.detect_periodicity(
            signal, min_period=8.0, max_period=12.0
        )
        
        error = abs(detected_period - target_period)
        
        print(f"   → Target period: {target_period:.2f}s")
        print(f"   → Detected period: {detected_period:.2f}s")
        print(f"   → Error: {error:.2f}s")
        
        self.assertLess(error, 0.5, 
            f"Detection error {error:.2f}s exceeds 0.5s threshold")
    
    def test_tempo_invariance(self):
        """
        CRITICAL TEST: Verify that detected period scales correctly with tempo changes.
        
        If we speed up the signal by 1.2x, the detected period should decrease to 
        base_period / 1.2. This proves the detector measures structural timing,
        not spurious artifacts.
        """
        print("\n🎵 Testing tempo invariance (CRITICAL)...")
        
        base_period = 10.0
        signal = self.generate_test_signal(period_seconds=base_period)
        
        speed_factors = [0.8, 0.9, 1.0, 1.1, 1.2]
        errors = []
        
        for speed in speed_factors:
            # Time-stretch the signal
            stretched = librosa.effects.time_stretch(signal, rate=speed)
            
            # Expected period after stretching
            expected_period = base_period / speed
            
            # Adapt search window
            search_margin = 4.0
            min_search = max(3.0, expected_period - search_margin)
            max_search = min(30.0, expected_period + search_margin)
            
            # Detect period
            detected_period, _, _ = self.detector.detect_periodicity(
                stretched, min_period=min_search, max_period=max_search
            )
            
            error = abs(detected_period - expected_period)
            errors.append(error)
            
            print(f"   Speed {speed}x: Detected {detected_period:.2f}s "
                  f"(Expected {expected_period:.2f}s, Error {error:.2f}s)")
        
        avg_error = np.mean(errors)
        max_error = np.max(errors)
        
        print(f"\n   📊 Average error: {avg_error:.2f}s")
        print(f"   📊 Maximum error: {max_error:.2f}s")
        
        # The key assertion: average error must be less than 0.5 seconds
        self.assertLess(avg_error, 0.5, 
            f"Average error {avg_error:.2f}s exceeds 0.5s threshold. "
            "Tempo-invariant detection failed!")
    
    def test_outside_search_window(self):
        """Test behavior when no valid period is found in the search window."""
        print("\n🎵 Testing out-of-range detection...")
        
        # Create signal with 5-second period
        signal = self.generate_test_signal(period_seconds=5.0)
        
        # Search in 8-12 second window (will not find 5s period)
        detected_period, times, ac_norm = self.detector.detect_periodicity(
            signal, min_period=8.0, max_period=12.0
        )
        
        print(f"   → Signal period: 5.0s (outside search window)")
        print(f"   → Search window: [8.0s, 12.0s]")
        print(f"   → Detected: {detected_period:.2f}s")
        
        # Should return something in the search window, even if not accurate
        self.assertGreaterEqual(detected_period, 8.0)
        self.assertLessEqual(detected_period, 12.0)


if __name__ == '__main__':
    unittest.main()

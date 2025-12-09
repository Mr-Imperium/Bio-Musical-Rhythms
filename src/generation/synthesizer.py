
import numpy as np
from scipy.io.wavfile import write

class BioResonanceComposer:
    def __init__(self, sample_rate=44100):
        self.sr = sample_rate

    def generate_tone(self, frequency, duration, amplitude=0.5):
        t = np.linspace(0, duration, int(self.sr * duration), endpoint=False)
        return amplitude * np.sin(2 * np.pi * frequency * t)

    def generate_therapeutic_drone(self, duration_sec=60, carrier_freq=110, breath_freq=0.1):
        t = np.linspace(0, duration_sec, int(self.sr * duration_sec), endpoint=False)
        
        # A2 (110Hz), A3 (220Hz), E3 (165Hz approx)
        c1 = np.sin(2 * np.pi * carrier_freq * t)
        c2 = np.sin(2 * np.pi * (carrier_freq * 2) * t) * 0.5
        c3 = np.sin(2 * np.pi * (carrier_freq * 1.5) * t) * 0.3
        
        carrier = (c1 + c2 + c3) / 1.8 
        
        modulator = 0.6 + 0.4 * np.sin(2 * np.pi * breath_freq * t - (np.pi/2))
        
        audio = carrier * modulator

        fade_len = int(2 * self.sr)
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        
        audio[:fade_len] *= fade_in
        audio[-fade_len:] *= fade_out
        
        return t, audio

    def save_to_disk(self, audio, filename="therapeutic_drone.wav"):
        scaled = np.int16(audio / np.max(np.abs(audio)) * 32767)
        write(filename, self.sr, scaled)
        return filename

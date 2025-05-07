import numpy as np
import pyaudio

class BeatsGenerator:
    """
    Generates and plays binaural beats with configurable carrier and split frequencies.
    """
    def __init__(self, rate: int = 44100, chunk: int = 1024):
        self.rate = rate
        self.chunk = chunk
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=2,
                                  rate=self.rate,
                                  output=True)

    def generate_wave(self, carrier: float, split: float, duration: float) -> bytes:
        """
        Synthesize a stereo waveform for binaural beats.
        """
        t = np.arange(int(self.rate * duration)) / self.rate
        left = np.sin(2 * np.pi * (carrier - split / 2) * t)
        right = np.sin(2 * np.pi * (carrier + split / 2) * t)
        stereo = np.vstack((left, right)).T.flatten().astype(np.float32)
        return stereo.tobytes()

    def play(self, carrier: float, split: float, duration: float):
        """
        Play binaural beats for a given duration in seconds.
        """
        data = self.generate_wave(carrier, split, duration)
        self.stream.write(data)

    def close(self):
        """
        Clean up the audio stream and terminate PyAudio.
        """
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate() 
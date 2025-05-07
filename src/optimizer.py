import numpy as np
from scipy.signal import welch

class FlowOptimizer:
    """
    Maintains an EEG buffer and computes bandpower for a target frequency band.
    """
    def __init__(self, fs: float, window_size: float, target_band: list):
        self.fs = fs
        self.window_size = window_size
        self.target_band = target_band
        self.buffer = []

    def add_sample(self, sample: list):
        # Use first EEG channel
        self.buffer.append(sample[0])
        # Keep buffer length <= fs * window_size
        maxlen = int(self.fs * self.window_size)
        if len(self.buffer) > maxlen:
            self.buffer = self.buffer[-maxlen:]

    def compute_bandpower(self) -> float:
        """
        Compute bandpower in the target band using Welch's method.
        """
        data = np.array(self.buffer)
        if data.size == 0:
            return 0.0
        nperseg = min(256, len(data))
        freqs, psd = welch(data, fs=self.fs, nperseg=nperseg)
        idx = (freqs >= self.target_band[0]) & (freqs <= self.target_band[1])
        return np.trapz(psd[idx], freqs[idx]) 
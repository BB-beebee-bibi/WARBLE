import time
from pylsl import StreamInlet, resolve_byprop

class MuseConnector:
    """
    Connects to a Muse EEG headband via LSL and streams raw data samples.
    """
    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout
        self.inlet = None

    def connect(self):
        """
        Resolve the first EEG stream and create an inlet.
        """
        print(f"Resolving EEG stream (timeout={self.timeout}s)...")
        streams = resolve_byprop('type', 'EEG', timeout=self.timeout)
        if not streams:
            raise RuntimeError("No EEG stream found. Make sure your Muse is streaming and LSL is available.")
        self.inlet = StreamInlet(streams[0])
        print("Connected to Muse EEG stream.")

    def get_sample(self):
        """
        Pull a single sample and timestamp from the inlet.
        Returns:
            sample (list of floats), timestamp (float)
        """
        if not self.inlet:
            raise RuntimeError("Inlet not initialized. Call connect() first.")
        sample, timestamp = self.inlet.pull_sample(timeout=1.0)
        return sample, timestamp

    def stream(self):
        """
        Generator that continuously yields (sample, timestamp) tuples.
        """
        self.connect()
        print("Starting EEG data stream. Press Ctrl+C to stop.")
        try:
            while True:
                sample, timestamp = self.get_sample()
                yield sample, timestamp
        except KeyboardInterrupt:
            print("EEG streaming stopped by user.") 
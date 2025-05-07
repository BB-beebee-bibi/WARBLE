import sys
import os
import time
import argparse
import yaml

# Ensure src is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from muse_connector import MuseConnector
from beats_generator import BeatsGenerator
from optimizer import FlowOptimizer


def load_config(path='config.yaml') -> dict:
    """
    Load YAML configuration from the given path.
    """
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description='WARBLE: Muse EEG-driven binaural beat optimizer')
    parser.add_argument('--mode', choices=['muse', 'beats', 'optimize'], required=True,
                        help='Mode to run: muse (EEG stream), beats (play fixed), optimize (adaptive)')
    parser.add_argument('--carrier', type=float, help='Carrier frequency for beats (Hz)')
    parser.add_argument('--split', type=float, help='Split difference between channels for beats (Hz)')
    parser.add_argument('--duration', type=float, default=None, help='Duration to play beats (seconds)')
    args = parser.parse_args()

    config = load_config()

    if args.mode == 'muse':
        connector = MuseConnector(timeout=config['bluetooth']['timeout'])
        connector.connect()
        for sample, timestamp in connector.stream():
            print(f"{timestamp:.3f}: {sample}")

    elif args.mode == 'beats':
        carrier = args.carrier or config['initial']['carrier']
        split = args.split or config['initial']['split']
        duration = args.duration or config['optimizer']['window_size']
        beats = BeatsGenerator(rate=config['audio']['rate'], chunk=config['audio']['chunk'])
        try:
            print(f"Playing beats: carrier={carrier} Hz, split={split} Hz, duration={duration}s")
            beats.play(carrier, split, duration)
        finally:
            beats.close()

    elif args.mode == 'optimize':
        connector = MuseConnector(timeout=config['bluetooth']['timeout'])
        beats = BeatsGenerator(rate=config['audio']['rate'], chunk=config['audio']['chunk'])
        optimizer = FlowOptimizer(fs=config['optimizer']['fs'],
                                  window_size=config['optimizer']['window_size'],
                                  target_band=config['optimizer']['target_band'])

        connector.connect()
        print("Starting optimization loop. Press Ctrl+C to stop.")

        current_carrier = config['initial']['carrier']
        current_split = config['initial']['split']
        prev_power = None
        start_time = time.time()
        try:
            for sample, timestamp in connector.stream():
                optimizer.add_sample(sample)
                elapsed = time.time() - start_time
                if elapsed >= config['optimizer']['window_size']:
                    bandpower = optimizer.compute_bandpower()
                    print(f"Bandpower: {bandpower:.4f} (carrier={current_carrier}, split={current_split})")
                    # Placeholder for adaptive logic (e.g., adjust frequencies to maximize bandpower)
                    # For now, just play with current parameters
                    beats.play(current_carrier, current_split, duration=elapsed)
                    start_time = time.time()

        except KeyboardInterrupt:
            print("Optimization stopped by user.")
        finally:
            beats.close()


if __name__ == '__main__':
    main() 
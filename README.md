# WARBLE

WARBLE is an open-source project designed to interface with the Muse EEG headband, stream raw brainwave data, and generate adaptive binaural beats to help users achieve and sustain flow or meditative states.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Connecting to the Muse Headband](#connecting-to-the-muse-headband)
  - [Generating Binaural Beats](#generating-binaural-beats)
  - [Optimizing Flow State](#optimizing-flow-state)
- [Configuration](#configuration)
- [Project Layout](#project-layout)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Real-time EEG Streaming:** Connects to the Muse headband via Bluetooth to stream raw EEG data.
- **Binaural Beat Generator:** Creates two slightly different frequencies (left vs. right channel) to produce binaural beats and supports configurable carrier and split frequencies.
- **Adaptive Optimization:** Analyzes EEG patterns associated with high-awareness or flow states and dynamically adjusts binaural beat parameters to help sustain that state.
- **Modular Design:** Clean separation between data acquisition, signal generation, and optimization algorithms.

## Architecture

- `src/muse_connector.py`  – Handles Bluetooth communication with the Muse headband and streams raw data.
- `src/beats_generator.py` – Generates audio waveforms for binaural beats using NumPy and PyAudio.
- `src/optimizer.py`       – Implements algorithms for detecting flow-state biomarkers in EEG data and adjusting beat parameters.
- `main.py`                – Orchestrates the data flow: capture → analyze → generate → adjust.
- `requirements.txt`       – Lists Python dependencies.

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- A Muse EEG headband (v2 recommended)
- Supported OS: macOS, Linux, Windows 10+
- Bluetooth adapter compatible with your OS

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/WARBLE.git
   cd WARBLE
   ```
2. Create a virtual environment (recommended):
   ```sh
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   .\venv\Scripts\activate  # Windows PowerShell
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Connecting to the Muse Headband

1. Ensure your Muse is powered on and in streaming mode.
2. Run the connector:
   ```sh
   python main.py --mode muse
   ```
3. The script will scan for the Muse device over Bluetooth and begin streaming raw EEG data.

### Generating Binaural Beats

You can manually generate binaural beats with custom parameters:

```sh
python main.py --mode beats --carrier 440 --split 6
```

- `--carrier`: Base frequency in Hz (e.g., 440)
- `--split`: Difference between left and right channels in Hz (e.g., 6)

### Optimizing Flow State

Start the end-to-end loop to capture EEG, analyze, generate beats, and adapt:

```sh
python main.py --mode optimize
```

The optimizer will:
1. Detect EEG biomarkers correlated with high-awareness or flow.
2. Adjust carrier/split frequencies in real-time.
3. Log performance metrics for analysis.

## Configuration

You can edit `config.yaml` (to be created) to customize:

- Bluetooth adapter settings
- Audio output device
- Initial carrier and split frequencies
- EEG analysis parameters (bandpass filters, threshold values)

## Project Layout

```
WARBLE/
├── src/
│   ├── muse_connector.py
│   ├── beats_generator.py
│   ├── optimizer.py
│   └── utils.py
├── main.py
├── config.yaml     # (optional) user configuration
├── requirements.txt
└── README.md
```

## Future Work

- **Flow-State Detection:** Explore advanced machine learning models to better detect flow or meditative states.
- **GUI Interface:** Provide a desktop or web UI for real-time controls and visualization.
- **Cloud Sync:** Store EEG and optimization logs to the cloud for longitudinal analysis.
- **Mobile Companion App:** Stream beats to a mobile app for on-the-go sessions.

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on code standards, branch strategy, and submitting pull requests.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details. 
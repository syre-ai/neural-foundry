"""ART Neural Networks Track.

Learn Claude Code through training Adaptive Resonance Theory (ART) neural networks.
This track uses the artlib library for GPU-accelerated ART implementations.

Requirements:
- torch
- artlib
- numpy

Missions teach Claude Code skills while building real ML models:
- M01: File reading through ART1 pattern recognition
- M02: Iterative editing through FuzzyART clustering
- M03: Code generation through ARTMAP classification
"""

from foundry.engine.base import register_track

# Register this track
register_track(
    track_id="art_neural_networks",
    name="ART Neural Networks",
    description="Learn Claude Code through Adaptive Resonance Theory models",
    requirements=["torch", "artlib", "numpy"],
    models=["ART1", "FuzzyART", "SimpleARTMAP", "ARTMAP"],
)

# Import missions to register them
from foundry.tracks.art_neural_networks.missions import (
    m01_first_resonance,
    m02_signal_noise,
    m03_mappers_path,
)

__all__ = [
    "m01_first_resonance",
    "m02_signal_noise",
    "m03_mappers_path",
]

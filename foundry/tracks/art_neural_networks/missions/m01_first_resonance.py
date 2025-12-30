"""Mission 01: First Resonance - Introduction to ART1 pattern recognition."""

from pathlib import Path
import json
import numpy as np

from foundry.engine.tiers import Tier
from foundry.engine.base import (
    Mission,
    MissionInfo,
    Checkpoint,
    CheckpointStatus,
    register_mission,
)

INSTRUCTIONS = '''
# Mission 01: First Resonance

## Briefing

A research station has recovered fragments of an old pattern recognition system.
The data files contain binary digit patterns (0-9), but the classification model
was lost. Your task: rebuild the classifier using ART1.

## Objectives

1. **Explore the Data** - Read and understand the pattern files in the `data/` folder
2. **Load the Patterns** - Write code to load the binary patterns into numpy arrays
3. **Configure ART1** - Initialize an ART1 model with appropriate vigilance
4. **Train & Classify** - Train the model and achieve >80% clustering purity

## Files

```
workspace/
├── data/
│   ├── patterns.json    # The binary digit patterns
│   └── readme.txt       # Data format documentation
├── train.py             # Your training script (create this)
└── results.json         # Output your results here
```

## Hints

- Start by reading `data/readme.txt` to understand the format
- Use Claude Code to help you explore: "Read the patterns.json file"
- ART1 vigilance controls cluster specificity (0.1 = loose, 0.9 = strict)
- For digits, try vigilance around 0.5-0.7

## Validation

Run `nf check` in the workspace to validate your progress.

Good luck, Apprentice. May your patterns resonate.
'''

MISSION_INFO = MissionInfo(
    id="m01_first_resonance",
    title="First Resonance",
    tier=Tier.APPRENTICE,
    description="Learn to read files and train your first ART1 model",
    story="Rebuild a lost pattern classifier using recovered binary digit data",
    xp_reward=100,
    claude_skills=["File reading", "Data exploration", "Basic model training"],
    track="art_neural_networks",
    track_skills=["ART1"],
)


@register_mission
class FirstResonanceMission(Mission):
    """First mission teaching file reading and ART1 basics."""

    info = MISSION_INFO

    def __init__(self):
        self.workspace: Path | None = None
        self._checkpoints = [
            Checkpoint(
                id="explore_data",
                title="Explore the Data",
                description="Read and understand the pattern files",
                hint="Try: 'Read data/readme.txt' or 'What's in the data folder?'",
                status=CheckpointStatus.AVAILABLE,
            ),
            Checkpoint(
                id="load_patterns",
                title="Load the Patterns",
                description="Create code that loads patterns into numpy arrays",
                hint="Create train.py with numpy array loading logic",
            ),
            Checkpoint(
                id="configure_art1",
                title="Configure ART1",
                description="Initialize ART1 with appropriate parameters",
                hint="Import from artlib: from artlib import ART1",
            ),
            Checkpoint(
                id="train_model",
                title="Train & Classify",
                description="Achieve >80% clustering purity",
                hint="Write results to results.json with 'purity' key",
            ),
        ]

    def setup(self, workspace: Path) -> None:
        """Initialize mission workspace with required files."""
        self.workspace = workspace
        workspace.mkdir(parents=True, exist_ok=True)
        data_dir = workspace / "data"
        data_dir.mkdir(exist_ok=True)

        # Generate and save patterns
        patterns, labels = self._generate_digit_patterns()
        patterns_data = {
            "patterns": patterns.tolist(),
            "labels": labels.tolist(),
            "shape": [8, 8],
            "description": "Binary digit patterns 0-9",
        }
        (data_dir / "patterns.json").write_text(json.dumps(patterns_data, indent=2))

        # Write readme
        readme = '''# Pattern Data Format

This file contains binary representations of handwritten digits (0-9).

## Structure

- patterns.json contains:
  - "patterns": List of 64-element binary arrays (8x8 flattened)
  - "labels": True digit label for each pattern (0-9)
  - "shape": Original 2D shape [8, 8]

## Loading Example

```python
import json
import numpy as np

with open("patterns.json") as f:
    data = json.load(f)

patterns = np.array(data["patterns"])  # Shape: (N, 64)
labels = np.array(data["labels"])      # Shape: (N,)
```

## Notes

- Patterns are binary (0 or 1 values only)
- Each digit has multiple slightly different examples
- Some patterns may have noise/corruption
'''
        (data_dir / "readme.txt").write_text(readme)

        # Write instructions
        (workspace / "MISSION.md").write_text(INSTRUCTIONS)

    def _generate_digit_patterns(self) -> tuple[np.ndarray, np.ndarray]:
        """Generate binary 8x8 digit patterns."""
        # Base patterns for digits 0-9 (8x8 binary)
        base_patterns = {
            0: [
                "00111100",
                "01000010",
                "01000010",
                "01000010",
                "01000010",
                "01000010",
                "01000010",
                "00111100",
            ],
            1: [
                "00011000",
                "00101000",
                "01001000",
                "00001000",
                "00001000",
                "00001000",
                "00001000",
                "01111110",
            ],
            2: [
                "00111100",
                "01000010",
                "00000010",
                "00000100",
                "00001000",
                "00010000",
                "00100000",
                "01111110",
            ],
            3: [
                "00111100",
                "01000010",
                "00000010",
                "00011100",
                "00000010",
                "00000010",
                "01000010",
                "00111100",
            ],
            4: [
                "00000100",
                "00001100",
                "00010100",
                "00100100",
                "01000100",
                "01111110",
                "00000100",
                "00000100",
            ],
            5: [
                "01111110",
                "01000000",
                "01000000",
                "01111100",
                "00000010",
                "00000010",
                "01000010",
                "00111100",
            ],
            6: [
                "00111100",
                "01000010",
                "01000000",
                "01111100",
                "01000010",
                "01000010",
                "01000010",
                "00111100",
            ],
            7: [
                "01111110",
                "00000010",
                "00000100",
                "00001000",
                "00010000",
                "00010000",
                "00010000",
                "00010000",
            ],
            8: [
                "00111100",
                "01000010",
                "01000010",
                "00111100",
                "01000010",
                "01000010",
                "01000010",
                "00111100",
            ],
            9: [
                "00111100",
                "01000010",
                "01000010",
                "00111110",
                "00000010",
                "00000010",
                "01000010",
                "00111100",
            ],
        }

        patterns = []
        labels = []

        rng = np.random.default_rng(42)

        for digit, rows in base_patterns.items():
            # Convert base pattern to array
            base = np.array([[int(c) for c in row] for row in rows]).flatten()

            # Add 5 variants per digit (some with noise)
            for i in range(5):
                pattern = base.copy()
                if i > 0:  # Add some noise to variants
                    noise_idx = rng.choice(64, size=rng.integers(1, 4), replace=False)
                    pattern[noise_idx] = 1 - pattern[noise_idx]
                patterns.append(pattern)
                labels.append(digit)

        return np.array(patterns), np.array(labels)

    def get_checkpoints(self) -> list[Checkpoint]:
        """Return list of mission checkpoints."""
        return self._checkpoints

    def validate_checkpoint(self, checkpoint_id: str) -> tuple[bool, str]:
        """Validate if a checkpoint is complete."""
        if not self.workspace:
            return False, "Mission not initialized"

        if checkpoint_id == "explore_data":
            # Check if user has read the data files (we trust they did)
            readme = self.workspace / "data" / "readme.txt"
            if readme.exists():
                return True, "Data files are ready to explore!"
            return False, "Data files not found"

        elif checkpoint_id == "load_patterns":
            train_py = self.workspace / "train.py"
            if not train_py.exists():
                return False, "Create train.py with your loading code"
            content = train_py.read_text()
            if "numpy" in content or "np." in content:
                if "patterns" in content.lower():
                    return True, "Loading code detected!"
            return False, "train.py should load patterns with numpy"

        elif checkpoint_id == "configure_art1":
            train_py = self.workspace / "train.py"
            if not train_py.exists():
                return False, "Create train.py first"
            content = train_py.read_text()
            if "ART1" in content and "artlib" in content:
                return True, "ART1 configuration found!"
            return False, "Import and configure ART1 from artlib"

        elif checkpoint_id == "train_model":
            results_file = self.workspace / "results.json"
            if not results_file.exists():
                return False, "Run your training and save results.json"
            try:
                results = json.loads(results_file.read_text())
                purity = results.get("purity", 0)
                if purity >= 0.8:
                    return True, f"Excellent! Purity: {purity:.1%}"
                return False, f"Purity {purity:.1%} - need >80%"
            except json.JSONDecodeError:
                return False, "Invalid results.json format"

        return False, "Unknown checkpoint"

    def get_instructions(self) -> str:
        """Return mission instructions/briefing."""
        return INSTRUCTIONS

"""Mission 03: The Mapper's Path - Supervised learning with ARTMAP."""

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
# Mission 03: The Mapper's Path

## Briefing

The research station's classification system was lost in the incident. Fortunately,
we recovered labeled training data. Your task: rebuild the classifier using ARTMAP,
a supervised variant of ART that learns to map inputs to categories.

## Objectives

1. **Load the Data** - Read the train/test splits
2. **Generate the Code** - Ask Claude to help write ARTMAP training code
3. **Train the Model** - Fit on training data with labels
4. **Evaluate** - Achieve >85% test accuracy

## Files

```
workspace/
├── data/
│   ├── train_X.npy    # Training features (100, 8)
│   ├── train_y.npy    # Training labels (100,)
│   ├── test_X.npy     # Test features (50, 8)
│   ├── test_y.npy     # Test labels (50,)
│   └── readme.txt
├── train.py           # Minimal starter - you fill in the rest
└── results.json
```

## ARTMAP Concepts

ARTMAP adds **supervised learning** to ART:

- **SimpleARTMAP**: Wraps any ART module (like FuzzyART) for classification
- **fit(X, y)**: Train with features X and labels y
- **predict(X)**: Classify new samples

```python
from artlib import SimpleARTMAP, FuzzyART

# Create base ART module
fuzzy_art = FuzzyART(rho=0.7, alpha=0.01, beta=1.0)

# Wrap it in ARTMAP for supervised learning
model = SimpleARTMAP(module_a=fuzzy_art)

# Train (X = features, y = integer labels)
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)
```

## The Challenge

This mission has a **minimal starter template**. Instead of filling in TODOs,
you should **ask Claude to generate the code** for you.

Try prompts like:
- "Write a function to create a SimpleARTMAP model with FuzzyART"
- "Add code to train the model and evaluate accuracy"
- "How do I calculate classification accuracy?"

This teaches you to leverage Claude for code generation - a core workflow.

## Hints

- Data is already normalized to [0, 1]
- Remember: FuzzyART needs `prepare_data()` for complement coding
- SimpleARTMAP handles the label mapping internally
- Start with rho=0.7 for the FuzzyART module

## Validation

Run `nf check m03_mappers_path` to validate progress.

Trust the resonance. Let Claude guide you.
'''

MISSION_INFO = MissionInfo(
    id="m03_mappers_path",
    title="The Mapper's Path",
    tier=Tier.APPRENTICE,
    description="Learn code generation with supervised ARTMAP classification",
    story="Rebuild a classification system using labeled training data",
    xp_reward=200,
    claude_skills=["Code generation", "Describing requirements", "Supervised learning"],
    track="art_neural_networks",
    track_skills=["SimpleARTMAP", "FuzzyART"],
)


@register_mission
class MappersPathMission(Mission):
    """Third mission teaching code generation with ARTMAP."""

    info = MISSION_INFO

    def __init__(self):
        self.workspace: Path | None = None
        self._checkpoints = [
            Checkpoint(
                id="load_data",
                title="Load the Data",
                description="Read the train/test numpy files",
                hint="Use np.load() for the 4 data files",
                status=CheckpointStatus.AVAILABLE,
            ),
            Checkpoint(
                id="generate_code",
                title="Generate the Code",
                description="Create ARTMAP training code (use Claude!)",
                hint="Ask: 'Write code to create SimpleARTMAP with FuzzyART'",
            ),
            Checkpoint(
                id="train_model",
                title="Train the Model",
                description="Fit the model on training data",
                hint="model.fit(X_prepared, y_train)",
            ),
            Checkpoint(
                id="evaluate",
                title="Evaluate",
                description="Achieve >85% test accuracy",
                hint="Compare predictions to test_y, save accuracy to results.json",
            ),
        ]

    def setup(self, workspace: Path) -> None:
        """Initialize mission workspace with required files."""
        self.workspace = workspace
        workspace.mkdir(parents=True, exist_ok=True)
        data_dir = workspace / "data"
        data_dir.mkdir(exist_ok=True)

        # Generate synthetic classification data
        train_X, train_y, test_X, test_y = self._generate_classification_data()
        np.save(data_dir / "train_X.npy", train_X)
        np.save(data_dir / "train_y.npy", train_y)
        np.save(data_dir / "test_X.npy", test_X)
        np.save(data_dir / "test_y.npy", test_y)

        # Write readme
        readme = '''# Classification Data Format

## Files

- train_X.npy: Training features, shape (100, 8)
- train_y.npy: Training labels, shape (100,) - integers 0-3
- test_X.npy: Test features, shape (50, 8)
- test_y.npy: Test labels, shape (50,) - integers 0-3

## Loading

```python
import numpy as np

train_X = np.load("train_X.npy")
train_y = np.load("train_y.npy")
test_X = np.load("test_X.npy")
test_y = np.load("test_y.npy")

print(f"Train: {train_X.shape}, Test: {test_X.shape}")
print(f"Classes: {np.unique(train_y)}")
```

## Notes

- All features are normalized to [0, 1] range
- 4 classes (0, 1, 2, 3)
- Classes are well-separated in feature space
- Test set is held out for evaluation
'''
        (data_dir / "readme.txt").write_text(readme)

        # Write instructions
        (workspace / "MISSION.md").write_text(INSTRUCTIONS)

        # Write MINIMAL starter - just loading, rest is up to Claude
        starter = '''"""ARTMAP Classification for sensor data.

This is a MINIMAL starter. Ask Claude to help you write the rest!

Example prompts:
- "Write code to create a SimpleARTMAP model with FuzzyART"
- "Add a function to train and evaluate the model"
- "How do I calculate classification accuracy?"
"""

import numpy as np

# Load the data
train_X = np.load("data/train_X.npy")
train_y = np.load("data/train_y.npy")
test_X = np.load("data/test_X.npy")
test_y = np.load("data/test_y.npy")

print(f"Train: {train_X.shape}, labels: {np.unique(train_y)}")
print(f"Test: {test_X.shape}")

# TODO: Ask Claude to help you write the rest!
# You need to:
# 1. Import SimpleARTMAP and FuzzyART from artlib
# 2. Create and configure the model
# 3. Prepare the data (complement coding)
# 4. Train on training data
# 5. Predict on test data
# 6. Calculate accuracy
# 7. Save results to results.json
'''
        (workspace / "train.py").write_text(starter)

    def _generate_classification_data(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Generate synthetic classification data with 4 classes."""
        rng = np.random.default_rng(42)

        n_classes = 4
        train_per_class = 25
        test_per_class = 12
        n_features = 8

        # Generate class centers spread across feature space
        centers = rng.uniform(0.2, 0.8, size=(n_classes, n_features))

        # Make centers more distinct
        for i in range(n_classes):
            # Each class has 2 dominant features
            dominant = [(i * 2) % n_features, (i * 2 + 1) % n_features]
            centers[i, dominant] = 0.7 + rng.uniform(0, 0.2, size=2)
            # And 2 recessive features
            recessive = [(i * 2 + 4) % n_features, (i * 2 + 5) % n_features]
            centers[i, recessive] = 0.1 + rng.uniform(0, 0.2, size=2)

        train_X, train_y = [], []
        test_X, test_y = [], []

        for class_id in range(n_classes):
            center = centers[class_id]

            # Training samples
            samples = center + rng.normal(0, 0.08, size=(train_per_class, n_features))
            samples = np.clip(samples, 0, 1)
            train_X.append(samples)
            train_y.extend([class_id] * train_per_class)

            # Test samples (slightly different noise)
            samples = center + rng.normal(0, 0.08, size=(test_per_class, n_features))
            samples = np.clip(samples, 0, 1)
            test_X.append(samples)
            test_y.extend([class_id] * test_per_class)

        # Combine and shuffle
        train_X = np.vstack(train_X).astype(np.float32)
        train_y = np.array(train_y)
        test_X = np.vstack(test_X).astype(np.float32)
        test_y = np.array(test_y)

        # Shuffle training data
        perm = rng.permutation(len(train_X))
        train_X = train_X[perm]
        train_y = train_y[perm]

        # Shuffle test data
        perm = rng.permutation(len(test_X))
        test_X = test_X[perm]
        test_y = test_y[perm]

        return train_X, train_y, test_X, test_y

    def get_checkpoints(self) -> list[Checkpoint]:
        """Return list of mission checkpoints."""
        return self._checkpoints

    def validate_checkpoint(self, checkpoint_id: str) -> tuple[bool, str]:
        """Validate if a checkpoint is complete."""
        if not self.workspace:
            return False, "Mission not initialized"

        train_py = self.workspace / "train.py"
        results_file = self.workspace / "results.json"

        if checkpoint_id == "load_data":
            if not train_py.exists():
                return False, "train.py not found"
            content = train_py.read_text()
            if "np.load" in content and "train_X" in content:
                return True, "Data loading detected!"
            return False, "Load the numpy data files"

        elif checkpoint_id == "generate_code":
            if not train_py.exists():
                return False, "train.py not found"
            content = train_py.read_text()
            has_artmap = "SimpleARTMAP" in content or "ARTMAP" in content
            has_fuzzy = "FuzzyART" in content
            if has_artmap and has_fuzzy:
                return True, "ARTMAP code generated!"
            return False, "Ask Claude to write SimpleARTMAP + FuzzyART code"

        elif checkpoint_id == "train_model":
            if not train_py.exists():
                return False, "train.py not found"
            content = train_py.read_text()
            if ".fit(" in content and ("SimpleARTMAP" in content or "ARTMAP" in content):
                return True, "Training code detected!"
            return False, "Add model.fit() call to train the model"

        elif checkpoint_id == "evaluate":
            if not results_file.exists():
                return False, "Run training and save results.json"
            try:
                results = json.loads(results_file.read_text())
                accuracy = results.get("accuracy", 0)
                if accuracy >= 0.85:
                    return True, f"Excellent! Accuracy: {accuracy:.1%}"
                return False, f"Accuracy {accuracy:.1%} - need >85%"
            except json.JSONDecodeError:
                return False, "Invalid results.json format"

        return False, "Unknown checkpoint"

    def get_instructions(self) -> str:
        """Return mission instructions/briefing."""
        return INSTRUCTIONS

"""Mission 02: Signal in the Noise - FuzzyART clustering with iterative refinement."""

from pathlib import Path
import json
import numpy as np

from neural_foundry.game.tiers import Tier
from neural_foundry.missions.base import (
    Mission,
    MissionInfo,
    Checkpoint,
    CheckpointStatus,
    register_mission,
)

INSTRUCTIONS = '''
# Mission 02: Signal in the Noise

## Briefing

An abandoned research station transmitted its final sensor readings before going
offline. The data stream contains compressed embeddings - some are valid sensor
clusters, others are corrupted noise. Your task: separate the signal from the noise.

## Objectives

1. **Load the Embeddings** - Read the numpy data files
2. **First Attempt** - Run FuzzyART and observe the results
3. **Diagnose Issues** - Understand why initial clustering is poor
4. **Iterate to Success** - Adjust parameters and achieve >75% separation score

## Files

```
workspace/
├── data/
│   ├── embeddings.npy   # 100 samples, 16 dimensions (float32)
│   ├── labels.npy       # Ground truth: 0-4 = clusters, -1 = noise
│   └── readme.txt       # Data format documentation
├── train.py             # Your training script (create this)
└── results.json         # Output your results here
```

## FuzzyART Parameters

Unlike ART1, FuzzyART has three parameters to tune:

- `rho` (vigilance): Cluster specificity [0.0 - 1.0]
- `alpha` (choice): Affects category selection (typically small, e.g., 0.01)
- `beta` (learning): Learning rate [0.0 - 1.0]

## The Challenge

Your first attempt will likely produce poor results. This is intentional!

The iterative workflow:
1. Write initial code → Run → See poor results
2. Examine output → Ask Claude for help
3. Adjust parameters → Re-run → Check improvement
4. Repeat until >75% separation score

## Scoring

Separation score measures how well clusters match ground truth labels.
Perfect separation = each cluster contains only one true label (or only noise).

## Hints

- Start simple: `FuzzyART(rho=0.5, alpha=0.01, beta=1.0)`
- If too many clusters form, lower rho
- If clusters mix different labels, raise rho
- Noise points (-1 labels) should ideally form their own cluster(s)
- Ask Claude: "Why is my clustering purity low?"

## Validation

Run `nf check m02_signal_noise` to validate your progress.

Remember: iteration is the path to resonance.
'''

MISSION_INFO = MissionInfo(
    id="m02_signal_noise",
    title="Signal in the Noise",
    tier=Tier.APPRENTICE,
    description="Learn iterative editing with FuzzyART clustering",
    story="Separate valid sensor embeddings from corrupted noise transmissions",
    xp_reward=150,
    art_models=["FuzzyART"],
    claude_skills=["Iterative editing", "Debugging workflow", "Parameter tuning"],
)


@register_mission
class SignalNoiseMission(Mission):
    """Second mission teaching iterative refinement with FuzzyART."""

    info = MISSION_INFO

    def __init__(self):
        self.workspace: Path | None = None
        self._checkpoints = [
            Checkpoint(
                id="load_embeddings",
                title="Load the Embeddings",
                description="Read the numpy data files",
                hint="Use np.load() to read .npy files",
                status=CheckpointStatus.AVAILABLE,
            ),
            Checkpoint(
                id="first_attempt",
                title="First Attempt",
                description="Run FuzzyART and create initial results",
                hint="Import FuzzyART from artlib and run fit()",
            ),
            Checkpoint(
                id="diagnose",
                title="Diagnose Issues",
                description="Add diagnostic output to understand clustering",
                hint="Print cluster counts, check label distribution per cluster",
            ),
            Checkpoint(
                id="iterate_success",
                title="Iterate to Success",
                description="Achieve >75% separation score",
                hint="Adjust rho - try values between 0.3 and 0.7",
            ),
        ]

    def setup(self, workspace: Path) -> None:
        """Initialize mission workspace with required files."""
        self.workspace = workspace
        workspace.mkdir(parents=True, exist_ok=True)
        data_dir = workspace / "data"
        data_dir.mkdir(exist_ok=True)

        # Generate synthetic embeddings
        embeddings, labels = self._generate_embeddings()
        np.save(data_dir / "embeddings.npy", embeddings)
        np.save(data_dir / "labels.npy", labels)

        # Write readme
        readme = '''# Embedding Data Format

## Files

- embeddings.npy: Shape (100, 16) - 100 samples, 16 dimensions
- labels.npy: Shape (100,) - Ground truth labels

## Labels

- 0, 1, 2, 3, 4: Valid sensor cluster IDs
- -1: Corrupted/noise samples

## Loading

```python
import numpy as np

embeddings = np.load("embeddings.npy")  # Shape: (100, 16)
labels = np.load("labels.npy")          # Shape: (100,)

print(f"Samples: {len(embeddings)}")
print(f"Dimensions: {embeddings.shape[1]}")
print(f"Unique labels: {np.unique(labels)}")
```

## Notes

- All values are in range [0, 1] (pre-normalized)
- Noise samples are scattered throughout the embedding space
- Valid clusters have tight groupings
'''
        (data_dir / "readme.txt").write_text(readme)

        # Write instructions
        (workspace / "MISSION.md").write_text(INSTRUCTIONS)

        # Write a starter template to help them get going
        starter = '''"""FuzzyART clustering for sensor embeddings.

TODO: Complete this script to cluster the embeddings.

Workflow:
1. Load the data
2. Initialize FuzzyART
3. Fit the model
4. Evaluate clustering
5. Save results
"""

import numpy as np
# TODO: Import FuzzyART from artlib


def load_data(data_dir: str = "data"):
    """Load embeddings and labels."""
    # TODO: Load embeddings.npy and labels.npy
    pass


def calculate_separation_score(labels: np.ndarray, cluster_assignments: np.ndarray) -> float:
    """
    Calculate separation score.

    For each cluster, find the dominant true label.
    Score = sum of dominant label counts / total samples.
    """
    # TODO: Implement scoring
    pass


def main():
    # Load data
    embeddings, labels = load_data()
    print(f"Loaded {len(embeddings)} embeddings")

    # TODO: Initialize FuzzyART
    # Hint: FuzzyART(rho=?, alpha=?, beta=?)

    # TODO: Fit the model
    # Hint: model.fit(embeddings)

    # TODO: Get cluster assignments
    # Hint: model.labels_

    # TODO: Calculate separation score

    # TODO: Save results to results.json
    # Required keys: "separation_score", "n_clusters"


if __name__ == "__main__":
    main()
'''
        (workspace / "train.py").write_text(starter)

    def _generate_embeddings(self) -> tuple[np.ndarray, np.ndarray]:
        """Generate synthetic embeddings with clusters and noise."""
        rng = np.random.default_rng(42)

        n_clusters = 5
        samples_per_cluster = 15
        n_noise = 25
        n_dims = 16

        embeddings = []
        labels = []

        # Generate cluster centers
        centers = rng.uniform(0.2, 0.8, size=(n_clusters, n_dims))

        # Generate samples around each center
        for cluster_id in range(n_clusters):
            center = centers[cluster_id]
            # Tight clusters with small variance
            samples = center + rng.normal(0, 0.05, size=(samples_per_cluster, n_dims))
            samples = np.clip(samples, 0, 1)  # Keep in [0, 1]
            embeddings.append(samples)
            labels.extend([cluster_id] * samples_per_cluster)

        # Generate noise points scattered throughout
        noise = rng.uniform(0, 1, size=(n_noise, n_dims))
        embeddings.append(noise)
        labels.extend([-1] * n_noise)

        embeddings = np.vstack(embeddings).astype(np.float32)
        labels = np.array(labels)

        # Shuffle
        perm = rng.permutation(len(embeddings))
        embeddings = embeddings[perm]
        labels = labels[perm]

        return embeddings, labels

    def get_checkpoints(self) -> list[Checkpoint]:
        """Return list of mission checkpoints."""
        return self._checkpoints

    def validate_checkpoint(self, checkpoint_id: str) -> tuple[bool, str]:
        """Validate if a checkpoint is complete."""
        if not self.workspace:
            return False, "Mission not initialized"

        train_py = self.workspace / "train.py"
        results_file = self.workspace / "results.json"

        if checkpoint_id == "load_embeddings":
            if not train_py.exists():
                return False, "train.py not found"
            content = train_py.read_text()
            if "np.load" in content and "embeddings" in content.lower():
                return True, "Data loading code detected!"
            return False, "Add np.load() to read the .npy files"

        elif checkpoint_id == "first_attempt":
            if not train_py.exists():
                return False, "train.py not found"
            content = train_py.read_text()
            if "FuzzyART" in content and "fit" in content:
                if results_file.exists():
                    return True, "First attempt completed!"
                return False, "Run your script and save results.json"
            return False, "Add FuzzyART initialization and fit()"

        elif checkpoint_id == "diagnose":
            if not train_py.exists():
                return False, "train.py not found"
            content = train_py.read_text()
            # Look for diagnostic code: print statements, cluster analysis
            has_diagnostics = any(x in content for x in [
                "print", "n_clusters", "unique", "Counter", "distribution"
            ])
            if has_diagnostics and "FuzzyART" in content:
                return True, "Diagnostic code detected!"
            return False, "Add print statements to analyze your clusters"

        elif checkpoint_id == "iterate_success":
            if not results_file.exists():
                return False, "Run training and save results.json"
            try:
                results = json.loads(results_file.read_text())
                score = results.get("separation_score", 0)
                if score >= 0.75:
                    return True, f"Excellent! Score: {score:.1%}"
                return False, f"Score {score:.1%} - need >75%. Adjust parameters!"
            except json.JSONDecodeError:
                return False, "Invalid results.json format"

        return False, "Unknown checkpoint"

    def get_instructions(self) -> str:
        """Return mission instructions/briefing."""
        return INSTRUCTIONS

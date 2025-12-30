# Claude Foundry

**A gamified framework for mastering Claude Code through hands-on missions.**

Claude Foundry is an extensible CLI-based learning platform that teaches effective Claude Code workflows through practical challenges. Instead of reading documentation, you learn by doing—completing missions that naturally require the skills being taught.

## Philosophy

Inspired by Andrej Karpathy's "JIT your work" philosophy, Claude Foundry teaches skills exactly when you need them. The framework is built around **learning tracks**—themed collections of missions that teach Claude Code through domain-specific challenges.

## Architecture

```
foundry/
├── engine/              # Core game engine (track-agnostic)
│   ├── base.py          # Mission framework
│   ├── state.py         # Player progress & saves
│   ├── tiers.py         # Tier progression system
│   └── runner.py        # Mission execution
├── tracks/              # Learning tracks (pluggable content)
│   └── art_neural_networks/   # Example track: ART models
│       └── missions/
├── ui/                  # Terminal UI components
└── cli.py               # Main CLI entry point
```

### Core Concepts

- **Tracks**: Themed collections of missions (e.g., ART Neural Networks, Web Development, Data Analysis)
- **Missions**: Individual challenges that teach specific Claude Code skills
- **Checkpoints**: Validation points within each mission
- **Tiers**: Progression levels (Apprentice → Journeyman → Artisan → Master)

## Installation

### Prerequisites

- Python 3.10+
- [Claude Code CLI](https://claude.ai/claude-code)

### Setup

```bash
# Clone the repository
git clone https://github.com/syre-ai/neural-foundry.git
cd neural-foundry

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS

# Install in development mode
pip install -e .

# Verify installation
nf --version
```

## Quick Start

```bash
# See welcome screen
nf

# List available tracks
nf tracks

# List missions (optionally filter by track)
nf missions
nf missions --track art_neural_networks

# Start a mission
nf play m01_first_resonance

# Check your progress
nf check m01_first_resonance

# Complete and earn XP
nf complete m01_first_resonance
```

## Available Tracks

### ART Neural Networks

Learn Claude Code through Adaptive Resonance Theory models. Requires: `torch`, `artlib`, `numpy`

| Mission | Title | Claude Code Skill | Track Skill | XP |
|---------|-------|-------------------|-------------|-----|
| M01 | First Resonance | File reading | ART1 | 100 |
| M02 | Signal in the Noise | Iterative editing | FuzzyART | 150 |
| M03 | The Mapper's Path | Code generation | SimpleARTMAP | 200 |

## Creating Your Own Track

Tracks are self-contained packages under `foundry/tracks/`. Each track registers itself and its missions.

### 1. Create Track Directory

```
foundry/tracks/your_track/
├── __init__.py         # Track registration
└── missions/
    ├── __init__.py     # Mission imports
    └── m01_example.py  # Mission implementation
```

### 2. Register the Track

```python
# foundry/tracks/your_track/__init__.py
from foundry.engine.base import register_track

register_track(
    track_id="your_track",
    name="Your Track Name",
    description="What this track teaches",
    requirements=["dependency1", "dependency2"],
)

from foundry.tracks.your_track.missions import m01_example
```

### 3. Create a Mission

```python
# foundry/tracks/your_track/missions/m01_example.py
from pathlib import Path
from foundry.engine.tiers import Tier
from foundry.engine.base import (
    Mission, MissionInfo, Checkpoint, CheckpointStatus, register_mission
)

MISSION_INFO = MissionInfo(
    id="m01_your_mission",
    title="Your Mission",
    tier=Tier.APPRENTICE,
    description="What players will learn",
    story="The narrative context",
    xp_reward=100,
    claude_skills=["File reading", "Exploration"],
    track="your_track",
    track_skills=["SpecificTool"],
)

@register_mission
class YourMission(Mission):
    info = MISSION_INFO

    def __init__(self):
        self.workspace = None
        self._checkpoints = [
            Checkpoint(
                id="step1",
                title="First Step",
                description="What to do",
                hint="How to do it",
                status=CheckpointStatus.AVAILABLE,
            ),
        ]

    def setup(self, workspace: Path) -> None:
        """Create workspace files."""
        self.workspace = workspace
        workspace.mkdir(parents=True, exist_ok=True)
        # Create mission files here

    def get_checkpoints(self) -> list[Checkpoint]:
        return self._checkpoints

    def validate_checkpoint(self, checkpoint_id: str) -> tuple[bool, str]:
        """Check if checkpoint is complete."""
        # Implement validation logic
        return False, "Not implemented"

    def get_instructions(self) -> str:
        return "Mission instructions in markdown"
```

### 4. Register in tracks/__init__.py

```python
# foundry/tracks/__init__.py
from foundry.tracks import your_track
```

## How Missions Work

1. **Start**: `nf play <mission_id>` creates a workspace at `~/.claude-foundry/workspace/<mission_id>/`
2. **Read**: Open `MISSION.md` for objectives and hints
3. **Work**: Use Claude Code to complete the challenge
4. **Validate**: Run `nf check <mission_id>` to verify progress
5. **Complete**: Earn XP and unlock new missions

## Tier System

| Tier | Description | XP Required |
|------|-------------|-------------|
| Apprentice | Learning fundamentals | 0 |
| Journeyman | Multi-step workflows | 500 |
| Artisan | Complex integrations | 1500 |
| Master | Advanced patterns | 3000 |

## Tech Stack

- **Python 3.10+** with type hints
- **[Rich](https://rich.readthedocs.io/)** for terminal UI
- **[Click](https://click.palletsprojects.com/)** for CLI framework

## Project Status

The framework is functional with one complete track (ART Neural Networks). The architecture supports adding unlimited custom tracks.

- [x] Core engine
- [x] Mission framework
- [x] Tier progression
- [x] Track system
- [x] ART Neural Networks track (3 missions)
- [ ] Additional tracks
- [ ] Community track support

## Contributing

Want to add a track? Follow the "Creating Your Own Track" guide above. PRs welcome!

## License

MIT License — See [LICENSE](LICENSE) for details.

---

*Built with Claude Code*

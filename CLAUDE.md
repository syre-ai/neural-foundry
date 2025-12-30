# Claude Foundry

A gamified framework for teaching Claude Code through hands-on missions.

## Project Overview

Claude Foundry is an extensible learning platform with pluggable **tracks**. Each track is a themed collection of missions that teach Claude Code skills through domain-specific challenges.

## Architecture

### Core Engine (`foundry/engine/`)

The engine is track-agnostic and handles:
- **base.py**: Mission framework (Mission, MissionInfo, Checkpoint classes)
- **state.py**: Player progress, XP, tier tracking (saves to `~/.claude-foundry/`)
- **tiers.py**: Tier definitions (Apprentice → Journeyman → Artisan → Master)
- **runner.py**: Mission execution, validation, workspace management

### Tracks (`foundry/tracks/`)

Tracks register themselves and their missions. Each track is self-contained:
- Registers via `register_track()` in `__init__.py`
- Contains missions under `missions/` subdirectory
- Missions use `@register_mission` decorator

### Current Track: ART Neural Networks

Located at `foundry/tracks/art_neural_networks/`. Uses:
- `torch` for GPU-accelerated tensors
- `artlib` (AdaptiveResonanceLib) for ART implementations
- `numpy` for data handling

## Project Structure

```
foundry/
├── __init__.py          # Package version
├── __main__.py          # python -m foundry entry
├── cli.py               # CLI commands (nf)
├── engine/
│   ├── __init__.py      # Engine exports
│   ├── base.py          # Mission framework
│   ├── state.py         # Player state
│   ├── tiers.py         # Tier system
│   └── runner.py        # Mission runner
├── tracks/
│   ├── __init__.py      # Track imports
│   └── art_neural_networks/
│       ├── __init__.py  # Track registration
│       └── missions/
│           ├── __init__.py
│           ├── m01_first_resonance.py
│           ├── m02_signal_noise.py
│           └── m03_mappers_path.py
└── ui/
    ├── __init__.py
    └── display.py       # Rich terminal UI
```

## Development Commands

```bash
# Run the game
python -m foundry
# or: nf (after pip install -e .)

# List tracks
nf tracks

# List missions
nf missions

# Start a mission
nf play m01_first_resonance

# Check progress
nf check m01_first_resonance
```

## Adding a New Track

1. Create `foundry/tracks/your_track/`
2. Add `__init__.py` with `register_track()` call
3. Create `missions/` directory with mission files
4. Import track in `foundry/tracks/__init__.py`

See README.md for detailed track creation guide.

## Key Patterns

### JIT Learning
Missions teach Claude Code skills exactly when needed to solve the challenge.

### Checkpoint Validation
Each mission has checkpoints that verify:
- File existence and content
- Code patterns (imports, function calls)
- Output files (results.json with metrics)

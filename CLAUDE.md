# Neural Foundry

A CLI game that teaches people how to use Claude Code effectively through hands-on missions using AdaptiveResonanceLib (ART neural networks).

## Project Overview

Neural Foundry gamifies learning Claude Code workflows by having players train and work with ART neural networks. Each mission teaches a real Claude Code pattern (inspired by Karpathy's "JIT your work" philosophy) while building actual ML models.

## Core Concepts

### Tier System
- **Apprentice**: Basic Claude Code commands, simple ART1 models
- **Journeyman**: Multi-file workflows, FuzzyART clustering
- **Artisan**: Complex pipelines, ARTMAP supervised learning
- **Master**: Advanced patterns, ensemble ART systems

### Mission Structure
Each mission:
1. Presents a neural network challenge using artlib
2. Teaches a specific Claude Code workflow pattern
3. Validates completion through actual model performance
4. Unlocks new techniques and model types

### ART Models Used
- `ART1`: Binary pattern recognition (beginner)
- `FuzzyART`: Continuous data clustering (intermediate)
- `ARTMAP`: Supervised classification (advanced)
- `TopoART`: Topology-preserving learning (master)

## Tech Stack
- Python 3.x with PyTorch (GPU-accelerated)
- artlib (AdaptiveResonanceLib) for ART implementations
- Rich for terminal UI
- Click for CLI commands

## Project Structure
```
neural_foundry/
├── __init__.py
├── cli.py              # Main CLI entry point
├── game/
│   ├── __init__.py
│   ├── state.py        # Player progress, saves
│   ├── tiers.py        # Tier definitions
│   └── missions.py     # Mission framework
├── missions/           # Individual mission modules
│   ├── __init__.py
│   └── apprentice/
├── models/             # ART model wrappers
│   └── __init__.py
└── ui/                 # Terminal UI components
    └── __init__.py
```

## Development Commands
```bash
# Run the game
python -m neural_foundry

# Run tests
pytest tests/

# Quick ART model test
python -c "from artlib import FuzzyART; print('OK')"
```

## Key Patterns

### JIT Learning Philosophy
Missions are designed around "just-in-time" learning - players learn Claude Code features exactly when they need them to solve the current challenge.

### Resonance Metaphor
ART's "resonance" concept (pattern matching) parallels how Claude Code "resonates" with your intent when you provide good context.

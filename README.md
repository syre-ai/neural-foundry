# Neural Foundry

**Learn Claude Code through hands-on ART neural network missions.**

Neural Foundry is a CLI-based educational game that teaches effective Claude Code workflows by having players train and work with Adaptive Resonance Theory (ART) neural networks. Each mission introduces a real-world AI coding pattern while building actual machine learning models.

## Philosophy

Inspired by Andrej Karpathy's "JIT your work" philosophy, Neural Foundry teaches Claude Code skills exactly when you need them. Instead of reading documentation, you learn by doing—solving neural network challenges that naturally require the skills being taught.

The game draws a parallel between ART's "resonance" concept (pattern matching through vigilance tuning) and how Claude Code "resonates" with your intent when you provide good context.

## Features

- **Tiered Progression**: Advance from Apprentice to Master as you complete missions
- **Real ML Models**: Train actual ART neural networks using [AdaptiveResonanceLib](https://github.com/NiklasMelworWorton/AdaptiveResonanceLib)
- **Practical Skills**: Each mission teaches a specific Claude Code workflow pattern
- **GPU Accelerated**: Full PyTorch support for GPU-accelerated training

## Installation

### Prerequisites

- Python 3.10+
- CUDA-capable GPU (recommended)
- [Claude Code CLI](https://claude.ai/claude-code)

### Setup

```bash
# Clone the repository
git clone https://github.com/syre-ai/neural-foundry.git
cd neural-foundry

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

# Install dependencies
pip install -e .

# Verify installation
nf --version
```

## Quick Start

```bash
# Start the game
nf

# View your progress
nf status

# List available missions
nf missions

# Start a mission
nf play m01_first_resonance

# Check mission progress
nf check m01_first_resonance

# Complete a mission
nf complete m01_first_resonance
```

## Missions

### Apprentice Tier

| Mission | Title | ART Model | Claude Code Skill | XP |
|---------|-------|-----------|-------------------|-----|
| M01 | First Resonance | ART1 | File reading & exploration | 100 |
| M02 | Signal in the Noise | FuzzyART | Iterative editing (edit→test→refine) | 150 |
| M03 | The Mapper's Path | SimpleARTMAP | Code generation | 200 |
| M04 | *Coming Soon* | — | — | — |
| M05 | *Coming Soon* | — | — | — |

### Future Tiers

- **Journeyman**: Multi-file workflows, advanced clustering
- **Artisan**: Test-driven development, architecture decisions
- **Master**: System design, performance optimization

## Project Structure

```
neural-foundry/
├── neural_foundry/
│   ├── cli.py                 # Main CLI entry point
│   ├── game/
│   │   ├── state.py           # Player progress & saves
│   │   ├── tiers.py           # Tier definitions
│   │   └── runner.py          # Mission execution engine
│   ├── missions/
│   │   ├── base.py            # Mission framework
│   │   └── apprentice/        # Apprentice tier missions
│   │       ├── m01_first_resonance/
│   │       ├── m02_signal_noise/
│   │       └── m03_mappers_path/
│   ├── models/                # ART model wrappers
│   └── ui/                    # Terminal UI components
├── docs/
│   └── devlog/                # Development session logs
├── tests/
├── pyproject.toml
├── CLAUDE.md                  # Claude Code context file
└── README.md
```

## How It Works

1. **Start a Mission**: Each mission creates a workspace at `~/.neural_foundry/workspace/<mission_id>/`
2. **Read the Briefing**: Understand the neural network challenge and objectives
3. **Use Claude Code**: Work alongside Claude to explore data, write code, and train models
4. **Validate Progress**: Run `nf check <mission_id>` to verify checkpoints
5. **Complete & Advance**: Earn XP and unlock new missions and tiers

## ART Neural Networks

Neural Foundry uses Adaptive Resonance Theory (ART) models—a family of neural networks known for:

- **Stability-Plasticity Balance**: Learn new patterns without forgetting old ones
- **Online Learning**: No need to retrain from scratch
- **Interpretable Clusters**: Understand what the model learned

Models used in the game:

| Model | Type | Use Case |
|-------|------|----------|
| ART1 | Unsupervised | Binary pattern recognition |
| FuzzyART | Unsupervised | Continuous data clustering |
| SimpleARTMAP | Supervised | Classification with discrete labels |
| ARTMAP | Supervised | Complex input-output mappings |

## Development

### Running Tests

```bash
pytest tests/
```

### Development Logs

Detailed session logs are maintained in `docs/devlog/`. These capture design decisions, experiments, and learnings from each development session.

### Adding New Missions

1. Create a new directory under `neural_foundry/missions/<tier>/`
2. Implement the `Mission` base class
3. Register the mission in `neural_foundry/missions/__init__.py`
4. Test with `nf play <mission_id>`

## Tech Stack

- **Python 3.10+** with type hints
- **PyTorch** for GPU-accelerated tensor operations
- **[artlib](https://github.com/NiklasMelworWorton/AdaptiveResonanceLib)** for ART implementations
- **[Rich](https://rich.readthedocs.io/)** for terminal UI
- **[Click](https://click.palletsprojects.com/)** for CLI framework

## Status

🚧 **Active Development** — Apprentice tier missions in progress.

- [x] Core game engine
- [x] Mission framework
- [x] 3/5 Apprentice missions
- [ ] Journeyman tier
- [ ] Artisan tier
- [ ] Master tier

## License

MIT License — See [LICENSE](LICENSE) for details.

## Acknowledgments

- [AdaptiveResonanceLib](https://github.com/NiklasMelworWorton/AdaptiveResonanceLib) for ART implementations
- [Claude Code](https://claude.ai/claude-code) for AI-assisted development
- Andrej Karpathy for the "JIT your work" philosophy

---

*Built with Claude Code* 🤖

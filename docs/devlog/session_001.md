# Neural Foundry Development Log - Session 001

**Date:** 2024-12-30
**Duration:** ~45 minutes
**Participants:** User (syre), Claude Code (Opus 4.5)

---

## Session Overview

First development session for Neural Foundry - a CLI game teaching Claude Code workflows through ART neural network missions.

## Environment Setup

### System Configuration
- **OS:** WSL2 (Linux 6.6.87.2-microsoft-standard-WSL2)
- **GPU:** NVIDIA GeForce RTX 2070 SUPER
- **CUDA:** 12.4
- **PyTorch:** 2.6.0+cu124
- **Python:** 3.11

### Verification Commands
```bash
python3 -c "import torch; print(torch.cuda.is_available())"  # True
python3 -c "from artlib import FuzzyART; print('OK')"        # OK
```

---

## Phase 1: Project Scaffolding

### Files Created

```
neural_foundry/
├── __init__.py           # Package init, version 0.1.0
├── __main__.py           # Entry point for python -m
├── cli.py                # Click-based CLI commands
├── game/
│   ├── __init__.py
│   ├── state.py          # Player state persistence (~/.neural_foundry/save.json)
│   ├── tiers.py          # 4-tier progression system
│   └── runner.py         # Mission execution engine
├── missions/
│   ├── __init__.py       # Mission registry
│   ├── base.py           # Abstract mission framework
│   └── apprentice/
│       ├── __init__.py
│       └── m01_first_resonance/
│           └── __init__.py
├── models/
│   └── __init__.py
└── ui/
    ├── __init__.py
    └── display.py        # Rich terminal UI components

pyproject.toml            # Package configuration
CLAUDE.md                 # Project context for Claude Code
tests/__init__.py
```

### Key Design Decisions

1. **Tier System:** Apprentice → Journeyman → Artisan → Master
2. **State Persistence:** JSON file at ~/.neural_foundry/save.json
3. **Mission Workspaces:** Created at ~/.neural_foundry/workspace/<mission_id>/
4. **CLI Tool:** `nf` or `neural-foundry` commands

---

## Phase 2: Mission 01 - "First Resonance"

### Mission Design

| Attribute | Value |
|-----------|-------|
| ID | m01_first_resonance |
| Tier | Apprentice |
| XP Reward | 100 |
| ART Model | ART1 |
| Claude Skill | File reading & exploration |

### Learning Objectives

1. Use Claude Code to explore unfamiliar data files
2. Understand ART1's vigilance parameter
3. Iterative development workflow (edit → test → refine)

### Checkpoints

1. **Explore the Data** - Read patterns.json and readme.txt
2. **Load the Patterns** - Create train.py with numpy loading
3. **Configure ART1** - Import and initialize ART1 from artlib
4. **Train & Classify** - Achieve >80% clustering purity

### Dataset

- 50 binary digit patterns (0-9)
- 5 variants per digit (some with noise)
- 8x8 grid flattened to 64-element arrays
- Generated with seed 42 for reproducibility

### Training Experiments

| Attempt | Vigilance (rho) | Clusters | Purity | Result |
|---------|-----------------|----------|--------|--------|
| 1 | 0.6 | 50 | 100% | Over-clustering (no generalization) |
| 2 | 0.3 | 36 | 98% | Still too many clusters |
| 3 | 0.1 | 5 | 48% | Under-clustering (mixing digits) |
| 4 | 0.2 | 10 | 62% | Ideal cluster count, low purity |
| 5 | 0.25 | 17 | 74% | Getting closer |
| 6 | 0.28 | 28 | 88% | **SUCCESS** - passes >80% threshold |

### Key Insight

**Vigilance tuning in ART parallels prompt specificity in Claude Code:**
- Too high (rho=0.6): Every pattern unique, no generalization
- Too low (rho=0.1): Everything lumped together, loses distinctions
- Sweet spot (rho=0.28): Meaningful clusters with good purity

### Bug Fixes During Development

1. **ART1 API:** Removed `beta` parameter (not supported)
2. **Data type:** Changed `np.float64` to `np.bool_` (ART1 requires binary)

---

## User Learning: Claude Code Workflow

### Split-Screen Setup

User configured dual-monitor workflow:
- Monitor 1: Claude Code conversation (this session)
- Monitor 2: WSL terminal for direct command execution

### Key Commands Learned

```bash
# Resume conversation
claude --continue

# Mission commands
nf missions                    # List available
nf play m01_first_resonance    # Start mission
nf check m01_first_resonance   # Check progress
nf complete m01_first_resonance # Claim rewards
```

---

## Session Results

- **Project:** Fully scaffolded with working CLI
- **Mission 01:** Complete and playable
- **Player State:** 100 XP, 1 mission completed, Apprentice tier
- **Next:** 4 more missions to reach Journeyman tier

---

## Files Modified This Session

| File | Lines | Purpose |
|------|-------|---------|
| neural_foundry/__init__.py | 3 | Package version |
| neural_foundry/cli.py | 75 | CLI commands |
| neural_foundry/game/state.py | 70 | Player persistence |
| neural_foundry/game/tiers.py | 75 | Tier definitions |
| neural_foundry/game/runner.py | 145 | Mission runner |
| neural_foundry/missions/base.py | 105 | Mission framework |
| neural_foundry/missions/apprentice/m01_first_resonance/__init__.py | 200 | First mission |
| neural_foundry/ui/display.py | 85 | Terminal UI |
| pyproject.toml | 25 | Package config |
| CLAUDE.md | 80 | Project context |
| **Total** | ~860 | |

---

## Phase 3: Mission 02 - "Signal in the Noise"

### Mission Design

| Attribute | Value |
|-----------|-------|
| ID | m02_signal_noise |
| Tier | Apprentice |
| XP Reward | 150 |
| ART Model | FuzzyART |
| Claude Skill | Iterative editing (edit → test → refine) |

### Learning Objectives

1. Understand that first attempts often fail
2. Learn the iterative debugging workflow
3. Master FuzzyART's three parameters (rho, alpha, beta)
4. Connect to real-world ML: working with embeddings

### Dataset

- 100 synthetic embeddings, 16 dimensions
- 5 true clusters (15 samples each) + 25 noise points
- Pre-normalized to [0, 1] range
- Generated with seed 42 for reproducibility

### Checkpoints

1. **Load the Embeddings** - Use np.load() for .npy files
2. **First Attempt** - Run FuzzyART, observe poor results
3. **Diagnose Issues** - Add diagnostic output
4. **Iterate to Success** - Achieve >75% separation score

### Design Philosophy

Mission intentionally starts with a broken starter template to teach:
- Reading error messages
- Asking Claude for debugging help
- Iterating on parameters until success

### FuzzyART vs ART1

| Aspect | ART1 | FuzzyART |
|--------|------|----------|
| Data type | Binary only | Continuous [0,1] |
| Parameters | rho, L | rho, alpha, beta |
| Use case | Pattern matching | Clustering embeddings |

---

## Git Commits This Session

| Hash | Message |
|------|---------|
| 07d9b23 | Initial commit: Neural Foundry project scaffold + Mission 01 |
| 3d4d67a | Add Mission 02: Signal in the Noise |

---

## Session Summary

- **Duration:** ~1 hour
- **Missions Built:** 2 (First Resonance, Signal in the Noise)
- **Total XP Available:** 250
- **Progress Tracking:** Git + devlogs initialized

---

## Next Session Plans

- [ ] Play through Mission 02 to validate difficulty
- [ ] Add Mission 03 (perhaps ARTMAP for supervised learning?)
- [ ] Add more Apprentice missions to reach 5 total
- [ ] Consider adding cluster visualization
- [ ] Implement models/ wrappers for easier ART usage

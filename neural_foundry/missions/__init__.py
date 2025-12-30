"""Mission framework and registry."""

from neural_foundry.missions.base import (
    Mission,
    MissionInfo,
    Checkpoint,
    CheckpointStatus,
    register_mission,
    get_mission,
    get_all_missions,
    get_missions_for_tier,
)

# Import missions to trigger registration
from neural_foundry.missions.apprentice.m01_first_resonance import FirstResonanceMission

__all__ = [
    "Mission",
    "MissionInfo",
    "Checkpoint",
    "CheckpointStatus",
    "register_mission",
    "get_mission",
    "get_all_missions",
    "get_missions_for_tier",
    "FirstResonanceMission",
]

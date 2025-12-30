"""Claude Foundry game engine - domain-agnostic core."""

from foundry.engine.tiers import Tier, TierInfo, TIER_INFO, get_next_tier
from foundry.engine.base import (
    Mission,
    MissionInfo,
    Checkpoint,
    CheckpointStatus,
    register_mission,
    get_mission,
    get_all_missions,
    get_missions_for_tier,
)
from foundry.engine.state import GameState
from foundry.engine.runner import (
    start_mission,
    check_mission,
    complete_mission,
    list_missions,
)

__all__ = [
    "Tier",
    "TierInfo",
    "TIER_INFO",
    "get_next_tier",
    "Mission",
    "MissionInfo",
    "Checkpoint",
    "CheckpointStatus",
    "register_mission",
    "get_mission",
    "get_all_missions",
    "get_missions_for_tier",
    "GameState",
    "start_mission",
    "check_mission",
    "complete_mission",
    "list_missions",
]

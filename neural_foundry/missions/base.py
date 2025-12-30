"""Base classes for mission framework."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable

from neural_foundry.game.tiers import Tier


class CheckpointStatus(Enum):
    """Status of a mission checkpoint."""
    LOCKED = "locked"
    AVAILABLE = "available"
    COMPLETED = "completed"


@dataclass
class Checkpoint:
    """A single mission checkpoint/objective."""
    id: str
    title: str
    description: str
    hint: str
    validator: Callable[[], bool] | None = None
    status: CheckpointStatus = CheckpointStatus.LOCKED


@dataclass
class MissionInfo:
    """Mission metadata."""
    id: str
    title: str
    tier: Tier
    description: str
    story: str
    xp_reward: int
    art_models: list[str]
    claude_skills: list[str]
    checkpoints: list[Checkpoint] = field(default_factory=list)


class Mission(ABC):
    """Base class for all missions."""

    info: MissionInfo
    workspace: Path | None = None

    @abstractmethod
    def setup(self, workspace: Path) -> None:
        """Initialize mission workspace with required files."""
        pass

    @abstractmethod
    def get_checkpoints(self) -> list[Checkpoint]:
        """Return list of mission checkpoints."""
        pass

    @abstractmethod
    def validate_checkpoint(self, checkpoint_id: str) -> tuple[bool, str]:
        """
        Validate if a checkpoint is complete.
        Returns (success, message).
        """
        pass

    @abstractmethod
    def get_instructions(self) -> str:
        """Return mission instructions/briefing."""
        pass

    def get_current_checkpoint(self) -> Checkpoint | None:
        """Get the first non-completed checkpoint."""
        for cp in self.get_checkpoints():
            if cp.status != CheckpointStatus.COMPLETED:
                return cp
        return None

    def is_complete(self) -> bool:
        """Check if all checkpoints are completed."""
        return all(
            cp.status == CheckpointStatus.COMPLETED
            for cp in self.get_checkpoints()
        )


# Mission registry
_missions: dict[str, type[Mission]] = {}


def register_mission(mission_class: type[Mission]) -> type[Mission]:
    """Decorator to register a mission."""
    _missions[mission_class.info.id] = mission_class
    return mission_class


def get_mission(mission_id: str) -> type[Mission] | None:
    """Get a mission class by ID."""
    return _missions.get(mission_id)


def get_all_missions() -> dict[str, type[Mission]]:
    """Get all registered missions."""
    return _missions.copy()


def get_missions_for_tier(tier: Tier) -> list[type[Mission]]:
    """Get all missions for a specific tier."""
    return [m for m in _missions.values() if m.info.tier == tier]

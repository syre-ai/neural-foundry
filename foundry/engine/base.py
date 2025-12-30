"""Base classes for mission framework - domain agnostic."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable

from foundry.engine.tiers import Tier


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
    claude_skills: list[str]  # Claude Code skills taught
    track: str = "default"  # Which track this mission belongs to
    track_skills: list[str] = field(default_factory=list)  # Track-specific skills
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


# Mission registry - organized by track
_missions: dict[str, type[Mission]] = {}
_tracks: dict[str, dict] = {}  # Track metadata


def register_track(track_id: str, name: str, description: str, **kwargs) -> None:
    """Register a learning track."""
    _tracks[track_id] = {
        "id": track_id,
        "name": name,
        "description": description,
        **kwargs
    }


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


def get_missions_for_track(track_id: str) -> list[type[Mission]]:
    """Get all missions for a specific track."""
    return [m for m in _missions.values() if m.info.track == track_id]


def get_all_tracks() -> dict[str, dict]:
    """Get all registered tracks."""
    return _tracks.copy()

"""Tier definitions for player progression - domain agnostic."""

from enum import Enum
from dataclasses import dataclass, field


class Tier(Enum):
    """Player progression tiers."""
    APPRENTICE = "Apprentice"
    JOURNEYMAN = "Journeyman"
    ARTISAN = "Artisan"
    MASTER = "Master"


@dataclass
class TierInfo:
    """Detailed tier information."""
    tier: Tier
    description: str
    claude_skills: list[str]
    missions_required: int
    track_skills: list[str] = field(default_factory=list)  # Track-specific skills


# Default tier info (track-agnostic Claude Code skills)
TIER_INFO = {
    Tier.APPRENTICE: TierInfo(
        tier=Tier.APPRENTICE,
        description="Beginning your Claude Code journey",
        claude_skills=[
            "File reading and exploration",
            "Basic editing and iteration",
            "Simple code generation",
        ],
        missions_required=0,
    ),
    Tier.JOURNEYMAN: TierInfo(
        tier=Tier.JOURNEYMAN,
        description="Building confidence with multi-step workflows",
        claude_skills=[
            "Multi-file refactoring",
            "Task planning with todos",
            "Debugging with Claude",
        ],
        missions_required=5,
    ),
    Tier.ARTISAN: TierInfo(
        tier=Tier.ARTISAN,
        description="Mastering complex development patterns",
        claude_skills=[
            "Test-driven development",
            "Architecture decisions",
            "Code review workflows",
        ],
        missions_required=12,
    ),
    Tier.MASTER: TierInfo(
        tier=Tier.MASTER,
        description="Teaching others and pushing boundaries",
        claude_skills=[
            "System design",
            "Performance optimization",
            "Creating custom workflows",
        ],
        missions_required=20,
    ),
}


def get_next_tier(current: Tier) -> Tier | None:
    """Get the next tier in progression."""
    tiers = list(Tier)
    idx = tiers.index(current)
    if idx < len(tiers) - 1:
        return tiers[idx + 1]
    return None

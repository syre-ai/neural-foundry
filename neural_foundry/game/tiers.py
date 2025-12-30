"""Tier definitions for player progression."""

from enum import Enum
from dataclasses import dataclass


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
    art_models: list[str]
    claude_skills: list[str]
    missions_required: int


TIER_INFO = {
    Tier.APPRENTICE: TierInfo(
        tier=Tier.APPRENTICE,
        description="Beginning your journey with Claude Code and ART fundamentals",
        art_models=["ART1", "FuzzyART"],
        claude_skills=[
            "Basic file reading and editing",
            "Simple bash commands",
            "Understanding context windows",
        ],
        missions_required=0,
    ),
    Tier.JOURNEYMAN: TierInfo(
        tier=Tier.JOURNEYMAN,
        description="Building multi-file workflows and clustering pipelines",
        art_models=["FuzzyART", "HypersphereART"],
        claude_skills=[
            "Multi-file refactoring",
            "Task planning with todos",
            "Iterative development cycles",
        ],
        missions_required=5,
    ),
    Tier.ARTISAN: TierInfo(
        tier=Tier.ARTISAN,
        description="Mastering supervised learning and complex code generation",
        art_models=["ARTMAP", "FuzzyARTMAP"],
        claude_skills=[
            "Test-driven development",
            "Architecture decisions",
            "Code review patterns",
        ],
        missions_required=12,
    ),
    Tier.MASTER: TierInfo(
        tier=Tier.MASTER,
        description="Creating ensemble systems and teaching others",
        art_models=["TopoART", "DeepARTMAP", "SMART"],
        claude_skills=[
            "System design",
            "Performance optimization",
            "Knowledge transfer",
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

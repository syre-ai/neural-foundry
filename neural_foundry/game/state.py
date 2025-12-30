"""Player game state and persistence."""

import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime

from neural_foundry.game.tiers import Tier, TIER_INFO, get_next_tier


SAVE_PATH = Path.home() / ".neural_foundry" / "save.json"


@dataclass
class MissionProgress:
    """Progress within a single mission."""
    mission_id: str
    started_at: str
    completed_at: str | None = None
    checkpoints: list[str] = field(default_factory=list)


@dataclass
class GameState:
    """Complete player game state."""
    player_name: str = "Neural Apprentice"
    tier: Tier = Tier.APPRENTICE
    xp: int = 0
    missions_completed: list[str] = field(default_factory=list)
    current_mission: MissionProgress | None = None
    total_models_trained: int = 0
    achievements: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @classmethod
    def load(cls) -> "GameState":
        """Load game state from disk or create new."""
        if SAVE_PATH.exists():
            try:
                data = json.loads(SAVE_PATH.read_text())
                data["tier"] = Tier(data["tier"])
                if data.get("current_mission"):
                    data["current_mission"] = MissionProgress(**data["current_mission"])
                return cls(**data)
            except (json.JSONDecodeError, KeyError):
                pass
        return cls()

    def save(self) -> None:
        """Persist game state to disk."""
        SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = asdict(self)
        data["tier"] = self.tier.value
        SAVE_PATH.write_text(json.dumps(data, indent=2))

    def add_xp(self, amount: int) -> bool:
        """Add XP and check for tier advancement. Returns True if tier changed."""
        self.xp += amount
        next_tier = get_next_tier(self.tier)
        if next_tier:
            required = TIER_INFO[next_tier].missions_required
            if len(self.missions_completed) >= required:
                self.tier = next_tier
                return True
        return False

    def complete_mission(self, mission_id: str, xp_reward: int) -> None:
        """Mark a mission as completed."""
        if mission_id not in self.missions_completed:
            self.missions_completed.append(mission_id)
        self.add_xp(xp_reward)
        self.current_mission = None
        self.save()

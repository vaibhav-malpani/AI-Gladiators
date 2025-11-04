"""
Fighter class - Represents an AI Gladiator with personality, stats, and combat style
"""

import json
import uuid
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from datetime import datetime


@dataclass
class Fighter:
    """Represents an AI fighter with unique personality and combat capabilities"""

    name: str
    personality: str
    backstory: str
    preferred_moves: List[str]
    aggression_level: float  # 0.0 to 1.0
    defense_bias: float  # 0.0 to 1.0
    reaction_speed: str  # "slow", "medium", "fast"
    special_trait: str

    # Combat stats
    health: int = 100
    max_health: int = 100
    stamina: int = 100
    max_stamina: int = 100
    power: int = 50
    technique: int = 50

    # Experience and progression
    level: int = 1
    experience: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0

    # Metadata
    fighter_id: str = None
    created_at: str = None

    def __post_init__(self):
        if self.fighter_id is None:
            self.fighter_id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def take_damage(self, damage: int) -> bool:
        """Apply damage to fighter. Returns True if fighter is still alive."""
        self.health = max(0, self.health - damage)
        return self.health > 0

    def heal(self, amount: int):
        """Heal the fighter"""
        self.health = min(self.max_health, self.health + amount)

    def use_stamina(self, amount: int) -> bool:
        """Use stamina. Returns True if there was enough stamina."""
        if self.stamina >= amount:
            self.stamina -= amount
            return True
        return False

    def recover_stamina(self, amount: int = 10):
        """Recover stamina"""
        self.stamina = min(self.max_stamina, self.stamina + amount)

    def reset_for_battle(self):
        """Reset health and stamina for a new battle"""
        self.health = self.max_health
        self.stamina = self.max_stamina

    def add_experience(self, exp: int):
        """Add experience and handle level ups"""
        self.experience += exp
        exp_for_next_level = self.level * 100

        while self.experience >= exp_for_next_level:
            self.level_up()
            self.experience -= exp_for_next_level
            exp_for_next_level = self.level * 100

    def level_up(self):
        """Increase fighter level and stats"""
        self.level += 1
        self.max_health += 10
        self.max_stamina += 5
        self.power += 3
        self.technique += 3
        self.health = self.max_health
        self.stamina = self.max_stamina

    def record_win(self):
        """Record a victory"""
        self.wins += 1
        self.add_experience(100)

    def record_loss(self):
        """Record a loss"""
        self.losses += 1
        self.add_experience(25)

    def record_draw(self):
        """Record a draw"""
        self.draws += 1
        self.add_experience(50)

    def get_win_rate(self) -> float:
        """Calculate win rate"""
        total_battles = self.wins + self.losses + self.draws
        if total_battles == 0:
            return 0.0
        return (self.wins / total_battles) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert fighter to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Fighter':
        """Create fighter from dictionary"""
        return cls(**data)

    def save(self, filepath: str):
        """Save fighter to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, filepath: str) -> 'Fighter':
        """Load fighter from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)

    def __str__(self) -> str:
        return (f"{self.name} (Lvl {self.level}) - "
                f"{self.wins}W/{self.losses}L/{self.draws}D - "
                f"Win Rate: {self.get_win_rate():.1f}%")

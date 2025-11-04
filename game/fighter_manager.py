"""
Fighter Manager - Handles fighter creation, storage, and retrieval
"""

import os
import json
from typing import List, Optional
from game.fighter import Fighter


class FighterManager:
    """Manages fighter persistence and retrieval"""

    def __init__(self, fighters_dir: str = "data/fighters"):
        self.fighters_dir = fighters_dir
        os.makedirs(fighters_dir, exist_ok=True)

    def save_fighter(self, fighter: Fighter) -> bool:
        """Save a fighter to disk"""
        try:
            filepath = os.path.join(self.fighters_dir, f"{fighter.fighter_id}.json")
            fighter.save(filepath)
            return True
        except Exception as e:
            print(f"Error saving fighter: {e}")
            return False

    def load_fighter(self, fighter_id: str) -> Optional[Fighter]:
        """Load a fighter by ID"""
        try:
            filepath = os.path.join(self.fighters_dir, f"{fighter_id}.json")
            if os.path.exists(filepath):
                return Fighter.load(filepath)
        except Exception as e:
            print(f"Error loading fighter: {e}")
        return None

    def list_all_fighters(self) -> List[Fighter]:
        """Load all saved fighters"""
        fighters = []
        try:
            for filename in os.listdir(self.fighters_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.fighters_dir, filename)
                    try:
                        fighter = Fighter.load(filepath)
                        fighters.append(fighter)
                    except Exception as e:
                        print(f"Error loading {filename}: {e}")
        except Exception as e:
            print(f"Error listing fighters: {e}")

        return sorted(fighters, key=lambda f: f.created_at, reverse=True)

    def delete_fighter(self, fighter_id: str) -> bool:
        """Delete a fighter"""
        try:
            filepath = os.path.join(self.fighters_dir, f"{fighter_id}.json")
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        except Exception as e:
            print(f"Error deleting fighter: {e}")
        return False

    def search_fighters(self, query: str) -> List[Fighter]:
        """Search fighters by name"""
        all_fighters = self.list_all_fighters()
        query_lower = query.lower()
        return [f for f in all_fighters if query_lower in f.name.lower()]

"""
AI Gladiators - FastAPI Backend
REST API for fighter management and battle simulation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import sys

# Add parent directory to path to import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.fighter_manager import FighterManager
from game.battle_engine import BattleEngine
from game.ai_agent import AIAgent
from game.fighter import Fighter

# Initialize FastAPI app
app = FastAPI(
    title="AI Gladiators API",
    description="Backend API for AI Gladiators game",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and common React ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize game components
fighter_manager = FighterManager()
ai_agent = AIAgent()
battle_engine = BattleEngine(ai_agent)

# Ensure data directories exist
os.makedirs('data', exist_ok=True)
os.makedirs('data/fighters', exist_ok=True)
os.makedirs('data/battles', exist_ok=True)


# Pydantic models for API
class FighterCreateRequest(BaseModel):
    prompt: str


class FighterResponse(BaseModel):
    fighter_id: str
    name: str
    personality: str
    backstory: str
    preferred_moves: List[str]
    aggression_level: float
    defense_bias: float
    reaction_speed: str
    special_trait: str
    health: int
    max_health: int
    stamina: int
    max_stamina: int
    power: int
    technique: int
    level: int
    experience: int
    wins: int
    losses: int
    draws: int
    created_at: str


class BattleRequest(BaseModel):
    fighter1_id: str
    fighter2_id: str


class BattleRoundLog(BaseModel):
    round: int
    fighter1_name: str
    fighter2_name: str
    f1_action_type: str
    f1_move: str
    f2_action_type: str
    f2_move: str
    f1_health: int
    f2_health: int
    result: str


class BattleResponse(BaseModel):
    winner: str
    winner_name: Optional[str]
    battle_log: List[Dict[str, Any]]
    commentary: str
    fighter1_stats: Dict[str, int]
    fighter2_stats: Dict[str, int]


# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "⚔️ Welcome to AI Gladiators API ⚔️",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/fighters", response_model=List[FighterResponse])
async def get_all_fighters():
    """Get all fighters"""
    fighters = fighter_manager.list_all_fighters()
    return [FighterResponse(**fighter.to_dict()) for fighter in fighters]


@app.get("/api/fighters/{fighter_id}", response_model=FighterResponse)
async def get_fighter(fighter_id: str):
    """Get a specific fighter by ID"""
    fighter = fighter_manager.load_fighter(fighter_id)
    if not fighter:
        raise HTTPException(status_code=404, detail="Fighter not found")
    return FighterResponse(**fighter.to_dict())


@app.post("/api/fighters", response_model=FighterResponse)
async def create_fighter(request: FighterCreateRequest):
    """Create a new fighter from natural language description"""
    if not request.prompt or len(request.prompt.strip()) < 10:
        raise HTTPException(
            status_code=400, 
            detail="Prompt must be at least 10 characters long"
        )

    # Generate fighter from prompt
    fighter_config = ai_agent.generate_fighter_from_prompt(request.prompt)
    fighter = Fighter(**fighter_config)

    # Save fighter
    if not fighter_manager.save_fighter(fighter):
        raise HTTPException(status_code=500, detail="Failed to save fighter")

    return FighterResponse(**fighter.to_dict())


@app.delete("/api/fighters/{fighter_id}")
async def delete_fighter(fighter_id: str):
    """Delete a fighter"""
    if not fighter_manager.delete_fighter(fighter_id):
        raise HTTPException(status_code=404, detail="Fighter not found")
    return {"message": "Fighter deleted successfully"}


@app.post("/api/battle", response_model=BattleResponse)
async def start_battle(request: BattleRequest):
    """Start a battle between two fighters"""
    # Load fighters
    fighter1 = fighter_manager.load_fighter(request.fighter1_id)
    fighter2 = fighter_manager.load_fighter(request.fighter2_id)

    if not fighter1:
        raise HTTPException(status_code=404, detail="Fighter 1 not found")
    if not fighter2:
        raise HTTPException(status_code=404, detail="Fighter 2 not found")

    if fighter1.fighter_id == fighter2.fighter_id:
        raise HTTPException(status_code=400, detail="A fighter cannot battle itself")

    # Store original stats
    f1_original_wins = fighter1.wins
    f1_original_losses = fighter1.losses
    f2_original_wins = fighter2.wins
    f2_original_losses = fighter2.losses

    # Simulate battle
    winner = battle_engine.simulate_battle(fighter1, fighter2, show_animation=False)

    # Get commentary
    commentary = battle_engine.get_battle_report()

    # Save updated fighters
    fighter_manager.save_fighter(fighter1)
    fighter_manager.save_fighter(fighter2)

    # Prepare response
    winner_name = None
    if winner == 'fighter1':
        winner_name = fighter1.name
    elif winner == 'fighter2':
        winner_name = fighter2.name

    return BattleResponse(
        winner=winner,
        winner_name=winner_name,
        battle_log=battle_engine.battle_log,
        commentary=commentary,
        fighter1_stats={
            "health": fighter1.health,
            "wins": fighter1.wins,
            "losses": fighter1.losses,
            "level": fighter1.level,
            "exp_gained": fighter1.wins - f1_original_wins
        },
        fighter2_stats={
            "health": fighter2.health,
            "wins": fighter2.wins,
            "losses": fighter2.losses,
            "level": fighter2.level,
            "exp_gained": fighter2.wins - f2_original_wins
        }
    )


@app.post("/api/fighters/{fighter_id}/train")
async def train_fighter(fighter_id: str):
    """Train a fighter through sparring sessions"""
    fighter = fighter_manager.load_fighter(fighter_id)
    if not fighter:
        raise HTTPException(status_code=404, detail="Fighter not found")

    # Create training dummy
    dummy_config = {
        "name": "Training Dummy",
        "personality": "Basic sparring partner",
        "backstory": "A practice opponent",
        "preferred_moves": ["punch", "block"],
        "aggression_level": 0.5,
        "defense_bias": 0.5,
        "reaction_speed": "medium",
        "special_trait": "None",
        "power": 30,
        "technique": 30
    }

    original_level = fighter.level
    wins = 0
    sessions = []

    # Run 3 training sessions
    for i in range(3):
        dummy = Fighter(**dummy_config)
        result = battle_engine.simulate_battle(fighter, dummy, show_animation=False)

        session_result = {
            "session": i + 1,
            "result": "victory" if result == 'fighter1' else "defeat"
        }
        sessions.append(session_result)

        if result == 'fighter1':
            wins += 1

    # Bonus experience
    bonus_exp = wins * 30
    fighter.add_experience(bonus_exp)

    # Save fighter
    fighter_manager.save_fighter(fighter)

    leveled_up = fighter.level > original_level

    return {
        "fighter_id": fighter_id,
        "sessions": sessions,
        "wins": wins,
        "bonus_exp": bonus_exp,
        "leveled_up": leveled_up,
        "new_level": fighter.level,
        "fighter": FighterResponse(**fighter.to_dict())
    }


@app.get("/api/rankings", response_model=List[FighterResponse])
async def get_rankings():
    """Get fighter rankings sorted by performance"""
    fighters = fighter_manager.list_all_fighters()

    # Sort by wins, then by win rate
    ranked = sorted(
        fighters, 
        key=lambda f: (f.wins, f.get_win_rate()), 
        reverse=True
    )

    return [FighterResponse(**fighter.to_dict()) for fighter in ranked]


@app.get("/api/stats")
async def get_global_stats():
    """Get global game statistics"""
    fighters = fighter_manager.list_all_fighters()

    if not fighters:
        return {
            "total_fighters": 0,
            "total_battles": 0,
            "highest_level": 0,
            "best_win_rate": 0
        }

    total_battles = sum(f.wins + f.losses + f.draws for f in fighters) // 2
    highest_level = max(f.level for f in fighters)
    best_win_rate = max(f.get_win_rate() for f in fighters)

    return {
        "total_fighters": len(fighters),
        "total_battles": total_battles,
        "highest_level": highest_level,
        "best_win_rate": round(best_win_rate, 1)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

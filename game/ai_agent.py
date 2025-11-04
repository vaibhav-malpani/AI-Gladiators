"""
AI Agent - Handles natural language processing and intelligent decision making
Integrated with Google Gemini for advanced AI capabilities
"""

import os
import random
import re
import json
from typing import Dict, List, Tuple, Any
from dotenv import load_dotenv
import google.generativeai as genai
from game.fighter import Fighter

# Load environment variables
load_dotenv()


class AIAgent:
    """
    AI Agent that processes natural language and makes combat decisions
    This is a simplified local implementation. In production, integrate with:
    - Google Gemini API for natural language understanding
    - Vertex AI for reinforcement learning and model fine-tuning
    """

    def __init__(self):
        self.move_types = [
            "punch", "kick", "grapple", "counter", "feint", 
            "pressure_point", "sweep", "throw", "block", "dodge"
        ]

        # Configure Google Gemini API
        api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.use_ai = True
            print("✅ Gemini API initialized successfully")
        else:
            self.model = None
            self.use_ai = False
            print("⚠️  Warning: GOOGLE_GEMINI_API_KEY not found. Using fallback rule-based AI.")

    def generate_fighter_from_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Generate a fighter configuration from natural language description
        Uses Gemini API for intelligent parsing and character generation
        """
        if self.use_ai and self.model:
            try:
                # Use Gemini to generate fighter attributes
                gemini_prompt = f"""
Based on this fighter description, generate a detailed fighter profile in JSON format:
"{prompt}"

Return a JSON object with these exact fields:
{{
    "name": "creative fighter name based on description",
    "personality": "brief personality description (max 50 words)",
    "backstory": "compelling 2-3 sentence backstory",
    "preferred_moves": ["list", "of", "3-5", "moves", "from: punch, kick, grapple, counter, feint, pressure_point, sweep, throw, block, dodge"],
    "aggression_level": 0.5,  // float between 0.0 (defensive) and 1.0 (aggressive)
    "defense_bias": 0.5,  // float between 0.0 (offensive) and 1.0 (defensive)
    "reaction_speed": "fast/medium/slow",
    "special_trait": "unique fighting trait or ability"
}}

Be creative and ensure the attributes match the description. Make it exciting and thematic!
"""

                response = self.model.generate_content(gemini_prompt)
                response_text = response.text.strip()

                # Extract JSON from response (handle markdown code blocks)
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()
                elif "```" in response_text:
                    json_start = response_text.find("```") + 3
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()

                fighter_data = json.loads(response_text)

                # Validate and ensure all fields are present
                fighter_data.setdefault("name", self._extract_name(prompt))
                fighter_data.setdefault("personality", "Mysterious warrior")
                fighter_data.setdefault("backstory", f"Born from the vision: '{prompt}'")
                fighter_data.setdefault("preferred_moves", random.sample(self.move_types, 4))
                fighter_data.setdefault("aggression_level", 0.5)
                fighter_data.setdefault("defense_bias", 0.5)
                fighter_data.setdefault("reaction_speed", "medium")
                fighter_data.setdefault("special_trait", "Adaptive combat style")

                # Ensure values are in valid ranges
                fighter_data["aggression_level"] = max(0.0, min(1.0, float(fighter_data["aggression_level"])))
                fighter_data["defense_bias"] = max(0.0, min(1.0, float(fighter_data["defense_bias"])))

                print(f"🤖 Gemini AI generated fighter: {fighter_data['name']}")
                return fighter_data

            except Exception as e:
                print(f"⚠️  Gemini API error: {e}. Falling back to rule-based generation.")

        # Fallback to rule-based generation
        prompt_lower = prompt.lower()

        # Extract name if mentioned
        name = self._extract_name(prompt)

        # Analyze personality traits
        aggression = self._analyze_aggression(prompt_lower)
        defense = self._analyze_defense(prompt_lower)
        speed = self._analyze_speed(prompt_lower)

        # Determine preferred moves based on description
        preferred_moves = self._extract_preferred_moves(prompt_lower)

        # Generate personality and special trait
        personality = self._generate_personality(prompt_lower)
        special_trait = self._generate_special_trait(prompt_lower, personality)

        return {
            "name": name,
            "personality": personality,
            "backstory": f"Born from the vision: '{prompt}'",
            "preferred_moves": preferred_moves,
            "aggression_level": aggression,
            "defense_bias": defense,
            "reaction_speed": speed,
            "special_trait": special_trait
        }

    def _extract_name(self, prompt: str) -> str:
        """Extract or generate a name from the prompt"""
        # Look for "named X" or "called X" patterns
        name_patterns = [
            r"named?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
            r"called\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)"
        ]

        for pattern in name_patterns:
            match = re.search(pattern, prompt)
            if match:
                return match.group(1)

        # Generate a thematic name based on keywords
        if any(word in prompt.lower() for word in ["patient", "calm", "zen", "serene"]):
            return random.choice(["Serenity Fist", "Zen Warrior", "Still Waters", "Patient Dragon"])
        elif any(word in prompt.lower() for word in ["aggressive", "fierce", "brutal"]):
            return random.choice(["Iron Fury", "Storm Breaker", "Raging Titan", "Savage Force"])
        elif any(word in prompt.lower() for word in ["robot", "machine", "android"]):
            return random.choice(["Mech-Alpha", "Combat Unit X", "Binary Fist", "Cyber Gladiator"])
        elif any(word in prompt.lower() for word in ["bruce lee", "martial", "master"]):
            return random.choice(["Shadow Dragon", "Master Flow", "Iron Lotus", "Silent Thunder"])
        else:
            return random.choice(["The Challenger", "Unknown Fighter", "Arena Warrior", "Battle Spirit"])

    def _analyze_aggression(self, prompt: str) -> float:
        """Analyze aggression level from prompt (0.0 to 1.0)"""
        aggressive_words = ["aggressive", "offensive", "attack", "fierce", "brutal", "relentless"]
        passive_words = ["patient", "defensive", "careful", "cautious", "wait"]

        aggressive_count = sum(1 for word in aggressive_words if word in prompt)
        passive_count = sum(1 for word in passive_words if word in prompt)

        if aggressive_count > passive_count:
            return min(0.9, 0.6 + (aggressive_count * 0.1))
        elif passive_count > aggressive_count:
            return max(0.2, 0.4 - (passive_count * 0.1))
        return 0.5

    def _analyze_defense(self, prompt: str) -> float:
        """Analyze defense bias from prompt (0.0 to 1.0)"""
        defensive_words = ["defensive", "block", "counter", "guard", "protect", "patient"]
        offensive_words = ["attack", "strike", "assault", "rush"]

        defensive_count = sum(1 for word in defensive_words if word in prompt)
        offensive_count = sum(1 for word in offensive_words if word in prompt)

        if defensive_count > offensive_count:
            return min(0.9, 0.6 + (defensive_count * 0.1))
        elif offensive_count > defensive_count:
            return max(0.2, 0.4 - (offensive_count * 0.1))
        return 0.5

    def _analyze_speed(self, prompt: str) -> str:
        """Analyze reaction speed from prompt"""
        if any(word in prompt for word in ["fast", "quick", "rapid", "lightning", "swift"]):
            return "fast"
        elif any(word in prompt for word in ["slow", "deliberate", "patient", "calculated"]):
            return "slow"
        return "medium"

    def _extract_preferred_moves(self, prompt: str) -> List[str]:
        """Extract preferred fighting moves from prompt"""
        moves = []

        if any(word in prompt for word in ["counter", "defensive", "patient"]):
            moves.extend(["counter", "block", "dodge"])
        if any(word in prompt for word in ["grapple", "wrestle", "throw"]):
            moves.extend(["grapple", "throw"])
        if any(word in prompt for word in ["strike", "punch", "hit"]):
            moves.extend(["punch", "kick"])
        if any(word in prompt for word in ["pressure point", "precise", "tactical"]):
            moves.append("pressure_point")
        if any(word in prompt for word in ["feint", "deceive", "trick"]):
            moves.append("feint")
        if "sweep" in prompt:
            moves.append("sweep")

        # If no specific moves found, use balanced defaults
        if not moves:
            moves = random.sample(self.move_types, 4)

        return list(set(moves))[:5]  # Return up to 5 unique moves

    def _generate_personality(self, prompt: str) -> str:
        """Generate personality description"""
        traits = []

        if any(word in prompt for word in ["patient", "calm", "zen"]):
            traits.append("patient and calculated")
        if any(word in prompt for word in ["aggressive", "fierce"]):
            traits.append("fierce and relentless")
        if any(word in prompt for word in ["strategic", "tactical", "smart"]):
            traits.append("highly strategic")
        if any(word in prompt for word in ["defensive", "cautious"]):
            traits.append("cautious defender")
        if any(word in prompt for word in ["adaptive", "learn"]):
            traits.append("adaptive learner")

        if not traits:
            traits = ["balanced fighter", "versatile combatant"]

        return ", ".join(traits[:3]).capitalize()

    def _generate_special_trait(self, prompt: str, personality: str) -> str:
        """Generate a unique special trait"""
        if any(word in prompt for word in ["predict", "read", "anticipate"]):
            return "Predictive defense — tries to read the opponent's moves"
        elif any(word in prompt for word in ["counter", "wait"]):
            return "Perfect counter — excels at punishing opponent mistakes"
        elif any(word in prompt for word in ["adapt", "learn", "study"]):
            return "Adaptive combat — learns opponent patterns during battle"
        elif any(word in prompt for word in ["aggressive", "relentless"]):
            return "Berserker mode — grows stronger as health decreases"
        elif any(word in prompt for word in ["robot", "machine"]):
            return "Machine precision — consistent and calculated strikes"
        else:
            return "Balanced warrior — adapts strategy to match the situation"

    def decide_action(self, fighter: Fighter, opponent: Fighter, battle_context: Dict) -> Tuple[str, str]:
        """
        AI decision making for combat actions
        Uses Gemini for sophisticated strategic reasoning

        Returns: (action_type, specific_move)
        """
        round_number = battle_context.get('round', 1)
        last_opponent_move = battle_context.get('last_opponent_move', None)

        # Use Gemini for advanced decision making (but keep it fast)
        if self.use_ai and self.model and round_number % 2 == 1:  # Use AI every other round for performance
            try:
                gemini_prompt = f"""
You are {fighter.name}, a combat AI making a split-second battle decision.

Current Situation:
- Your Health: {fighter.health}/{fighter.max_health} ({(fighter.health/fighter.max_health)*100:.0f}%)
- Your Stamina: {fighter.stamina}/{fighter.max_stamina} ({(fighter.stamina/fighter.max_stamina)*100:.0f}%)
- Opponent Health: {opponent.health}/{opponent.max_health} ({(opponent.health/opponent.max_health)*100:.0f}%)
- Opponent Stamina: {opponent.stamina}/{opponent.max_stamina}
- Round: {round_number}
- Your Personality: {fighter.personality}
- Special Trait: {fighter.special_trait}
- Opponent Last Move: {last_opponent_move or 'Unknown'}
- Your Preferred Moves: {', '.join(fighter.preferred_moves)}

Based on your fighting style and the battle situation, choose ONE action.
Respond with ONLY a JSON object (no other text):
{{
    "action_type": "attack/defend/special",
    "move": "one move from: {', '.join(self.move_types)}",
    "reasoning": "brief one-sentence tactical reasoning"
}}
"""

                response = self.model.generate_content(gemini_prompt)
                response_text = response.text.strip()

                # Extract JSON
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()
                elif "```" in response_text:
                    json_start = response_text.find("```") + 3
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()

                decision = json.loads(response_text)
                action_type = decision.get("action_type", "attack")
                move = decision.get("move", "punch")

                # Validate move is in available moves
                if move not in self.move_types:
                    move = random.choice(fighter.preferred_moves)

                return action_type, move

            except Exception as e:
                # Silently fall back to rule-based (Gemini can be slow/error in battle)
                pass

        # Rule-based decision making (original logic)
        weights = self._calculate_action_weights(fighter, opponent, battle_context)

        # Choose action type based on weights
        action_type = random.choices(
            ['attack', 'defend', 'special'],
            weights=[weights['attack'], weights['defend'], weights['special']]
        )[0]

        # Choose specific move
        if action_type == 'attack':
            move = self._choose_attack_move(fighter, opponent)
        elif action_type == 'defend':
            move = self._choose_defense_move(fighter, last_opponent_move)
        else:
            move = self._choose_special_move(fighter)

        return action_type, move

    def _calculate_action_weights(self, fighter: Fighter, opponent: Fighter, context: Dict) -> Dict[str, float]:
        """Calculate probability weights for different action types"""
        health_ratio = fighter.health / fighter.max_health
        stamina_ratio = fighter.stamina / fighter.max_stamina
        opponent_health_ratio = opponent.health / opponent.max_health

        # Base weights from personality
        attack_weight = fighter.aggression_level
        defend_weight = fighter.defense_bias
        special_weight = 0.2

        # Adjust based on health
        if health_ratio < 0.3:
            defend_weight *= 1.5  # More defensive when low health
        elif health_ratio > 0.7 and opponent_health_ratio < 0.5:
            attack_weight *= 1.3  # Press advantage

        # Adjust based on stamina
        if stamina_ratio < 0.3:
            defend_weight *= 1.4  # Conserve stamina
            attack_weight *= 0.7

        # Normalize weights
        total = attack_weight + defend_weight + special_weight
        return {
            'attack': attack_weight / total,
            'defend': defend_weight / total,
            'special': special_weight / total
        }

    def _choose_attack_move(self, fighter: Fighter, opponent: Fighter) -> str:
        """Choose an attack move from preferred moves"""
        attack_moves = [m for m in fighter.preferred_moves if m in ["punch", "kick", "sweep", "throw"]]
        if not attack_moves:
            attack_moves = ["punch", "kick"]
        return random.choice(attack_moves)

    def _choose_defense_move(self, fighter: Fighter, last_opponent_move: str) -> str:
        """Choose a defensive move"""
        defense_moves = [m for m in fighter.preferred_moves if m in ["block", "dodge", "counter"]]
        if not defense_moves:
            defense_moves = ["block", "dodge"]

        # If we know opponent's last move, counter appropriately
        if last_opponent_move in ["punch", "kick"]:
            return "counter" if "counter" in defense_moves else random.choice(defense_moves)

        return random.choice(defense_moves)

    def _choose_special_move(self, fighter: Fighter) -> str:
        """Choose a special move"""
        special_moves = [m for m in fighter.preferred_moves if m in ["feint", "grapple", "pressure_point"]]
        if not special_moves:
            special_moves = ["feint"]
        return random.choice(special_moves)

    def generate_battle_commentary(self, battle_log: List[Dict]) -> str:
        """
        Generate AI commentary about the battle
        Uses Gemini to create natural, engaging commentary
        """
        if not battle_log:
            return "The battle was too brief to analyze."

        # Use Gemini for dynamic commentary generation
        if self.use_ai and self.model:
            try:
                # Prepare battle summary for Gemini
                total_rounds = len(battle_log)
                fighter1_name = battle_log[0].get('fighter1_name', 'Fighter 1')
                fighter2_name = battle_log[0].get('fighter2_name', 'Fighter 2')

                # Calculate key statistics
                f1_attacks = sum(1 for r in battle_log if r.get('f1_action_type') == 'attack')
                f2_attacks = sum(1 for r in battle_log if r.get('f2_action_type') == 'attack')
                final_f1_health = battle_log[-1].get('f1_health', 0)
                final_f2_health = battle_log[-1].get('f2_health', 0)

                winner = fighter1_name if final_f1_health > final_f2_health else fighter2_name

                # Create battle summary
                battle_summary = {
                    "total_rounds": total_rounds,
                    "fighter1": {"name": fighter1_name, "attacks": f1_attacks, "final_health": final_f1_health},
                    "fighter2": {"name": fighter2_name, "attacks": f2_attacks, "final_health": final_f2_health},
                    "winner": winner
                }

                gemini_prompt = f"""
You are an enthusiastic sports commentator analyzing an epic gladiatorial combat match.

Battle Statistics:
- Total Rounds: {total_rounds}
- {fighter1_name}: {f1_attacks} attacks, final health {final_f1_health}%
- {fighter2_name}: {f2_attacks} attacks, final health {final_f2_health}%
- Winner: {winner}

Generate exciting battle commentary with the following structure:
1. Opening Hook (2-3 sentences about the battle's intensity)
2. Fighting Style Analysis (compare their approaches)
3. Key Turning Points (dramatic moments)
4. Final Verdict (celebrate the winner and honor both fighters)

Make it dramatic, exciting, and use emojis. Format with clear sections.
Keep it under 500 words.
"""

                response = self.model.generate_content(gemini_prompt)
                commentary_text = response.text.strip()

                # Format the commentary nicely
                formatted_commentary = [
                    f"\n{'='*60}",
                    "🎙️  BATTLE COMMENTARY",
                    f"{'='*60}\n",
                    commentary_text,
                    f"\n{'='*60}"
                ]

                return "\n".join(formatted_commentary)

            except Exception as e:
                print(f"⚠️  Gemini commentary error: {e}. Using fallback commentary.")

        # Analyze battle patterns
        total_rounds = len(battle_log)
        fighter1_name = battle_log[0].get('fighter1_name', 'Fighter 1')
        fighter2_name = battle_log[0].get('fighter2_name', 'Fighter 2')

        commentary = [
            f"\n{'='*60}",
            "🎙️  BATTLE COMMENTARY",
            f"{'='*60}\n"
        ]

        # Opening Assessment
        commentary.append(f"📺 What a clash! {fighter1_name} and {fighter2_name} entered the arena...")
        commentary.append(f"   This epic confrontation lasted {total_rounds} intense rounds.\n")

        # Calculate comprehensive statistics
        f1_attacks = sum(1 for r in battle_log if r.get('f1_action_type') == 'attack')
        f2_attacks = sum(1 for r in battle_log if r.get('f2_action_type') == 'attack')
        f1_defends = sum(1 for r in battle_log if r.get('f1_action_type') == 'defend')
        f2_defends = sum(1 for r in battle_log if r.get('f2_action_type') == 'defend')
        f1_specials = sum(1 for r in battle_log if r.get('f1_action_type') == 'special')
        f2_specials = sum(1 for r in battle_log if r.get('f2_action_type') == 'special')

        # Track health changes and damage
        initial_f1_health = battle_log[0].get('f1_health', 100)
        initial_f2_health = battle_log[0].get('f2_health', 100)
        final_f1_health = battle_log[-1].get('f1_health', 0)
        final_f2_health = battle_log[-1].get('f2_health', 0)

        f1_damage_taken = initial_f1_health - final_f1_health
        f2_damage_taken = initial_f2_health - final_f2_health
        f1_damage_dealt = f2_damage_taken
        f2_damage_dealt = f1_damage_taken

        # Opening Round Analysis
        commentary.append("⚔️  OPENING ROUNDS:")
        if battle_log[0].get('f1_action_type') == 'attack' and battle_log[0].get('f2_action_type') == 'attack':
            commentary.append(f"   Both fighters came out swinging! An aggressive start from both sides.")
        elif battle_log[0].get('f1_action_type') == 'defend' or battle_log[0].get('f2_action_type') == 'defend':
            commentary.append(f"   A cautious beginning as both fighters sized each other up.")

        # Find most dramatic moments
        max_health_drop = 0
        dramatic_round = 0
        for i, round_data in enumerate(battle_log):
            if i == 0:
                continue
            prev_round = battle_log[i-1]
            f1_drop = prev_round.get('f1_health', 0) - round_data.get('f1_health', 0)
            f2_drop = prev_round.get('f2_health', 0) - round_data.get('f2_health', 0)
            if max(f1_drop, f2_drop) > max_health_drop:
                max_health_drop = max(f1_drop, f2_drop)
                dramatic_round = i + 1

        if dramatic_round > 0 and max_health_drop > 15:
            commentary.append(f"\n💥 TURNING POINT - ROUND {dramatic_round}:")
            commentary.append(f"   Devastating blow! {max_health_drop} damage dealt in a single exchange!")

        # Aggression Analysis
        commentary.append("\n📊 FIGHTING STYLES:")
        if f1_attacks > f2_attacks * 1.4:
            commentary.append(f"   ✊ {fighter1_name} was relentlessly aggressive, pressing forward with {f1_attacks} attacks!")
            commentary.append(f"      Their offensive output was {int((f1_attacks/f2_attacks)*100 - 100)}% higher than their opponent.")
        elif f2_attacks > f1_attacks * 1.4:
            commentary.append(f"   ✊ {fighter2_name} was relentlessly aggressive, pressing forward with {f2_attacks} attacks!")
            commentary.append(f"      Their offensive output was {int((f2_attacks/f1_attacks)*100 - 100)}% higher than their opponent.")
        else:
            commentary.append(f"   ⚖️  Both fighters showed balanced aggression ({f1_attacks} vs {f2_attacks} attacks)")
            commentary.append(f"      A tactical chess match of offense and defense!")

        # Defensive Strategy
        if f1_defends > total_rounds * 0.35:
            commentary.append(f"\n   🛡️  {fighter1_name} played the long game with {f1_defends} defensive maneuvers")
            commentary.append(f"      Patient and calculated, waiting for the perfect opening...")
        if f2_defends > total_rounds * 0.35:
            commentary.append(f"\n   🛡️  {fighter2_name} played the long game with {f2_defends} defensive maneuvers")
            commentary.append(f"      Patient and calculated, waiting for the perfect opening...")

        # Special Moves Analysis
        if f1_specials > 0 or f2_specials > 0:
            commentary.append(f"\n✨ SPECIAL TECHNIQUES:")
            if f1_specials > 0:
                commentary.append(f"   {fighter1_name} unleashed {f1_specials} devastating special move(s)!")
            if f2_specials > 0:
                commentary.append(f"   {fighter2_name} unleashed {f2_specials} devastating special move(s)!")

        # Damage Efficiency Analysis
        commentary.append(f"\n💪 DAMAGE STATISTICS:")
        commentary.append(f"   {fighter1_name}: {f1_damage_dealt} damage dealt, {f1_damage_taken} taken")
        if f1_attacks > 0:
            f1_efficiency = f1_damage_dealt / f1_attacks
            commentary.append(f"      Efficiency: {f1_efficiency:.1f} damage per attack")

        commentary.append(f"   {fighter2_name}: {f2_damage_dealt} damage dealt, {f2_damage_taken} taken")
        if f2_attacks > 0:
            f2_efficiency = f2_damage_dealt / f2_attacks
            commentary.append(f"      Efficiency: {f2_efficiency:.1f} damage per attack")

        # Momentum shifts
        momentum_shifts = 0
        leader = None
        for round_data in battle_log:
            current_leader = 'f1' if round_data.get('f1_health', 0) > round_data.get('f2_health', 0) else 'f2'
            if leader and leader != current_leader:
                momentum_shifts += 1
            leader = current_leader

        if momentum_shifts > 3:
            commentary.append(f"\n🔄 The momentum shifted {momentum_shifts} times - a truly back-and-forth battle!")

        # Final Assessment
        commentary.append(f"\n🏆 FINAL VERDICT:")
        if final_f1_health > final_f2_health * 2:
            commentary.append(f"   Dominant victory for {fighter1_name}! A masterclass performance.")
        elif final_f2_health > final_f1_health * 2:
            commentary.append(f"   Dominant victory for {fighter2_name}! A masterclass performance.")
        elif abs(final_f1_health - final_f2_health) < 15:
            commentary.append(f"   Incredibly close battle! The outcome could have gone either way.")
        else:
            commentary.append(f"   Hard-fought victory! Both warriors gave their all in the arena.")

        commentary.append(f"\n{'='*60}")
        return "\n".join(commentary)

"""
Battle Engine - Handles combat simulation between AI fighters
"""

import random
import time
from typing import Dict
from game.fighter import Fighter
from game.ai_agent import AIAgent


class BattleEngine:
    """Simulates battles between AI fighters with autonomous decision making"""

    def __init__(self, ai_agent: AIAgent):
        self.ai_agent = ai_agent
        self.battle_log = []
        self.max_rounds = 30

    def simulate_battle(self, fighter1: Fighter, fighter2: Fighter, show_animation: bool = True) -> str:
        """
        Simulate a complete battle between two fighters
        Returns: 'fighter1', 'fighter2', or 'draw'
        """
        # Reset fighters for battle
        fighter1.reset_for_battle()
        fighter2.reset_for_battle()

        self.battle_log = []
        battle_context = {'round': 0, 'last_f1_move': None, 'last_f2_move': None}

        if show_animation:
            print(f"\n{'='*60}", "cyan")
            print(f"⚔️  BATTLE START: {fighter1.name} vs {fighter2.name} ⚔️", "yellow", bold=True)
            print(f"{'='*60}\n", "cyan")
            time.sleep(1)

        for round_num in range(1, self.max_rounds + 1):
            battle_context['round'] = round_num

            if show_animation:
                print(f"\n--- Round {round_num} ---", "cyan", bold=True)
                self._display_fighter_status(fighter1, fighter2)

            # Both fighters decide their actions simultaneously
            f1_action_type, f1_move = self.ai_agent.decide_action(
                fighter1, fighter2, 
                {**battle_context, 'last_opponent_move': battle_context.get('last_f2_move')}
            )
            f2_action_type, f2_move = self.ai_agent.decide_action(
                fighter2, fighter1,
                {**battle_context, 'last_opponent_move': battle_context.get('last_f1_move')}
            )

            # Execute actions and calculate results
            round_result = self._execute_round(
                fighter1, f1_action_type, f1_move,
                fighter2, f2_action_type, f2_move,
                show_animation
            )

            # Log round
            self.battle_log.append({
                'round': round_num,
                'fighter1_name': fighter1.name,
                'fighter2_name': fighter2.name,
                'f1_action_type': f1_action_type,
                'f1_move': f1_move,
                'f2_action_type': f2_action_type,
                'f2_move': f2_move,
                'f1_health': fighter1.health,
                'f2_health': fighter2.health,
                'result': round_result
            })

            battle_context['last_f1_move'] = f1_move
            battle_context['last_f2_move'] = f2_move

            if show_animation:
                time.sleep(0.8)

            # Check for knockout
            if fighter1.health <= 0 or fighter2.health <= 0:
                break

        # Determine winner
        winner = self._determine_winner(fighter1, fighter2, show_animation)

        # Update fighter records
        self._update_fighter_records(fighter1, fighter2, winner)

        return winner

    def _execute_round(
        self, 
        fighter1: Fighter, f1_action: str, f1_move: str,
        fighter2: Fighter, f2_action: str, f2_move: str,
        show_animation: bool
    ) -> str:
        """Execute a single round of combat"""

        # Determine initiative based on reaction speed
        speed_map = {'fast': 3, 'medium': 2, 'slow': 1}
        f1_speed = speed_map.get(fighter1.reaction_speed, 2) + random.random()
        f2_speed = speed_map.get(fighter2.reaction_speed, 2) + random.random()

        if f1_speed >= f2_speed:
            first, second = (fighter1, f1_action, f1_move), (fighter2, f2_action, f2_move)
            first_is_f1 = True
        else:
            first, second = (fighter2, f2_action, f2_move), (fighter1, f1_action, f1_move)
            first_is_f1 = False

        # Execute first fighter's action
        first_result = self._execute_action(first[0], second[0], first[1], first[2], show_animation)

        # Check if second fighter can still act
        if second[0].health > 0:
            second_result = self._execute_action(second[0], first[0], second[1], second[2], show_animation)

        # Both fighters recover some stamina
        fighter1.recover_stamina(10)
        fighter2.recover_stamina(10)

        return "round_complete"

    def _execute_action(
        self, 
        attacker: Fighter, 
        defender: Fighter, 
        action_type: str, 
        move: str,
        show_animation: bool
    ) -> Dict:
        """Execute a single fighter's action"""

        if action_type == 'attack':
            damage = self._calculate_damage(attacker, defender, move)
            stamina_cost = 15

            if attacker.use_stamina(stamina_cost):
                hit_chance = self._calculate_hit_chance(attacker, defender, move)

                if random.random() < hit_chance:
                    defender.take_damage(damage)
                    if show_animation:
                        print(
                            attacker.name, 
                            f"hits with {move.replace('_', ' ')}",
                            f"-{damage} HP",
                            "red"
                        )
                    return {'hit': True, 'damage': damage}
                else:
                    if show_animation:
                        print(
                            attacker.name,
                            f"attempts {move.replace('_', ' ')} but misses",
                            "MISS",
                            "yellow"
                        )
                    return {'hit': False, 'damage': 0}
            else:
                if show_animation:
                    print(
                        attacker.name,
                        "is too exhausted to attack",
                        "No stamina",
                        "gray"
                    )
                return {'hit': False, 'damage': 0, 'exhausted': True}

        elif action_type == 'defend':
            stamina_cost = 5
            if attacker.use_stamina(stamina_cost):
                # Defensive stance might reduce incoming damage
                heal_amount = random.randint(2, 5)
                attacker.heal(heal_amount)
                if show_animation:
                    print(
                        attacker.name,
                        f"takes defensive stance ({move.replace('_', ' ')})",
                        f"+{heal_amount} HP",
                        "green"
                    )
                return {'defended': True, 'heal': heal_amount}
            else:
                return {'defended': False}

        elif action_type == 'special':
            stamina_cost = 25
            if attacker.use_stamina(stamina_cost):
                # Special moves have unique effects
                damage = self._calculate_damage(attacker, defender, move, multiplier=1.5)
                hit_chance = self._calculate_hit_chance(attacker, defender, move) * 0.8

                if random.random() < hit_chance:
                    defender.take_damage(damage)
                    if show_animation:
                        print(
                            attacker.name,
                            f"executes special {move.replace('_', ' ')}!",
                            f"-{damage} HP ✨",
                            "magenta"
                        )
                    return {'hit': True, 'damage': damage, 'special': True}
                else:
                    if show_animation:
                        print(
                            attacker.name,
                            f"special {move.replace('_', ' ')} fails",
                            "MISS",
                            "yellow"
                        )
                    return {'hit': False, 'damage': 0}
            else:
                if show_animation:
                    print(
                        attacker.name,
                        "doesn't have enough stamina for special move",
                        "No stamina",
                        "gray"
                    )
                return {'hit': False, 'exhausted': True}

        return {}

    def _calculate_damage(self, attacker: Fighter, defender: Fighter, move: str, multiplier: float = 1.0) -> int:
        """Calculate damage for an attack"""
        base_damage = attacker.power * 0.3
        technique_bonus = attacker.technique * 0.2

        # Move-specific modifiers
        move_modifiers = {
            'punch': 0.8,
            'kick': 1.0,
            'sweep': 0.7,
            'throw': 1.2,
            'grapple': 1.1,
            'pressure_point': 0.9,
        }

        move_mod = move_modifiers.get(move, 0.8)

        # Random variance
        variance = random.uniform(0.8, 1.2)

        damage = int((base_damage + technique_bonus) * move_mod * multiplier * variance)
        return max(5, damage)  # Minimum 5 damage

    def _calculate_hit_chance(self, attacker: Fighter, defender: Fighter, move: str) -> float:
        """Calculate probability of hit landing"""
        base_chance = 0.7

        # Attacker technique increases hit chance
        technique_bonus = (attacker.technique / 100) * 0.2

        # Defender defense reduces hit chance
        defense_penalty = (defender.defense_bias) * 0.15

        # Speed affects hit chance
        speed_bonus = {'fast': 0.1, 'medium': 0.05, 'slow': 0}
        speed_mod = speed_bonus.get(attacker.reaction_speed, 0)

        hit_chance = base_chance + technique_bonus - defense_penalty + speed_mod
        return max(0.3, min(0.95, hit_chance))  # Clamp between 30% and 95%

    def _display_fighter_status(self, fighter1: Fighter, fighter2: Fighter):
        """Display current status of both fighters"""
        def status_bar(current: int, maximum: int, length: int = 20) -> str:
            filled = int((current / maximum) * length)
            bar = '█' * filled + '░' * (length - filled)
            return bar

        print(f"\n{fighter1.name}:")
        print(f"  HP: {status_bar(fighter1.health, fighter1.max_health)} {fighter1.health}/{fighter1.max_health}")
        print(f"  ST: {status_bar(fighter1.stamina, fighter1.max_stamina)} {fighter1.stamina}/{fighter1.max_stamina}")

        print(f"\n{fighter2.name}:")
        print(f"  HP: {status_bar(fighter2.health, fighter2.max_health)} {fighter2.health}/{fighter2.max_health}")
        print(f"  ST: {status_bar(fighter2.stamina, fighter2.max_stamina)} {fighter2.stamina}/{fighter2.max_stamina}")

    def _determine_winner(self, fighter1: Fighter, fighter2: Fighter, show_animation: bool) -> str:
        """Determine the winner of the battle"""
        if show_animation:
            print(f"\n{'='*60}", "cyan")

        if fighter1.health <= 0 and fighter2.health <= 0:
            if show_animation:
                print("💥 DOUBLE KNOCKOUT! IT'S A DRAW! 💥", "yellow", bold=True)
            return 'draw'
        elif fighter1.health <= 0:
            if show_animation:
                print(f"🏆 {fighter2.name} WINS! 🏆", "green", bold=True)
            return 'fighter2'
        elif fighter2.health <= 0:
            if show_animation:
                print(f"🏆 {fighter1.name} WINS! 🏆", "green", bold=True)
            return 'fighter1'
        else:
            # Max rounds reached, decide by health
            if fighter1.health > fighter2.health:
                if show_animation:
                    print(f"🏆 {fighter1.name} WINS BY DECISION! 🏆", "green", bold=True)
                return 'fighter1'
            elif fighter2.health > fighter1.health:
                if show_animation:
                    print(f"🏆 {fighter2.name} WINS BY DECISION! 🏆", "green", bold=True)
                return 'fighter2'
            else:
                if show_animation:
                    print("⚔️  IT'S A DRAW! ⚔️", "yellow", bold=True)
                return 'draw'

    def _update_fighter_records(self, fighter1: Fighter, fighter2: Fighter, winner: str):
        """Update fighter win/loss records"""
        if winner == 'fighter1':
            fighter1.record_win()
            fighter2.record_loss()
        elif winner == 'fighter2':
            fighter2.record_win()
            fighter1.record_loss()
        else:
            fighter1.record_draw()
            fighter2.record_draw()

    def get_battle_report(self) -> str:
        """Generate a detailed battle report using AI analysis"""
        return self.ai_agent.generate_battle_commentary(self.battle_log)

## Battle logic and mechanics
## Damage formulas and turn order
## Exp calculations and level ups

# backend/services/battle_service.py

import random
from backend.models.pokemon import Pokemon

# Basic damage calculation with STAB
def damage_calc(attacker: Pokemon, defender: Pokemon, power: int, move_type: str):
    """Basic damage calc with STAB. Returns (damage, stab_bool)."""
    lvl = (2 * attacker.level) / 5 + 2
    base = (lvl * attacker.attack * power) / defender.defense
    damage = int(base / 50) + 2

    stab = attacker.pokemon_type == move_type.lower()
    if stab:
        damage = int(damage * 1.5)

    # always at least 1 damage
    return max(damage, 1), stab

# Execute a turn
def take_turn(attacker: Pokemon, defender: Pokemon, move: tuple):
    """
    Execute a move and return a result dict.
    move = (name, power, move_type, category)
    """
    name, power, move_type, category = move

    # Healing move
    if category == "heal":
        old_hp = attacker.hp
        attacker.hp = min(attacker.hp + power, attacker.max_hp)
        healed = attacker.hp - old_hp
        return {
            "action": "heal",
            "move_name": name,
            "user": attacker.name,
            "target": attacker.name,
            "healed": healed,
            "user_hp": attacker.hp,
            "user_max_hp": attacker.max_hp,
        }

    # Damage move
    dmg, stab = damage_calc(attacker, defender, power, move_type)
    defender.hp = max(defender.hp - dmg, 0)

    return {
        "action": "damage",
        "move_name": name,
        "user": attacker.name,
        "target": defender.name,
        "damage": dmg,
        "stab": stab,
        "target_hp": defender.hp,
        "target_max_hp": defender.max_hp,
    }

# Simple enemy AI to choose a move randomly
def enemy_choose_move(enemy: Pokemon):
    """Very simple AI: pick a random move."""
    return random.choice(enemy.moves)

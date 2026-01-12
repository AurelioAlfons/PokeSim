## Battle logic and mechanics
## Damage formulas and turn order
## Exp calculations and level ups

# backend/services/battle_service.py

import random
from backend.models.pokemon import Pokemon


def _normalize_move(move):
    """
    Supports BOTH formats:
    - dict: {"name": "...", "power": 40, "type": "fire", "category": "damage"}
    - tuple/list: ("Ember", 40, "fire", "damage")

    Returns: (name, power:int, move_type:str, category:str)
    """
    # New format (dict)
    if isinstance(move, dict):
        name = move.get("name", "Unknown")
        power = int(move.get("power", 0))
        move_type = str(move.get("type", "normal")).lower()
        category = str(move.get("category", "damage")).lower()
        return name, power, move_type, category

    # Old format (tuple/list)
    if isinstance(move, (tuple, list)) and len(move) == 4:
        name, power, move_type, category = move
        return str(name), int(power), str(move_type).lower(), str(category).lower()

    raise TypeError(f"Unsupported move format: {move}")


# Basic damage calculation with STAB
def damage_calc(attacker: Pokemon, defender: Pokemon, power: int, move_type: str):
    """Basic damage calc with STAB. Returns (damage, stab_bool)."""
    lvl = (2 * attacker.level) / 5 + 2

    # avoid divide-by-zero just in case
    defense = max(1, defender.defense)

    base = (lvl * attacker.attack * power) / defense
    damage = int(base / 50) + 2

    # UPDATED: attacker has .types list now (not .pokemon_type)
    stab = move_type in attacker.types
    if stab:
        damage = int(damage * 1.5)

    # always at least 1 damage
    return max(damage, 1), stab


# Execute a turn
def take_turn(attacker: Pokemon, defender: Pokemon, move):
    """
    Execute a move and return a result dict.
    Accepts:
    - dict move
    - tuple move
    """
    name, power, move_type, category = _normalize_move(move)

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

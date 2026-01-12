# backend/services/battle_service.py
"""
Battle logic and mechanics (1v1 only)

✅ What this file should do:
- Turn order (speed)
- Damage + healing moves
- A small battle loop for ONE fight: player_pokemon vs wild_pokemon
- Return a simple outcome for Rogue mode:
    "wild_fainted"   -> you won the fight
    "player_fainted" -> your active fainted

❌ What this file should NOT do:
- Endless rogue waves (that lives in rogue_service.py)
- Team switching / run progression
"""

import random
from backend.models.pokemon import Pokemon


# -----------------------------
# Move helpers
# -----------------------------
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


# -----------------------------
# Damage
# -----------------------------
def damage_calc(attacker: Pokemon, defender: Pokemon, power: int, move_type: str):
    """Basic damage calc with STAB. Returns (damage, stab_bool)."""
    lvl = (2 * attacker.level) / 5 + 2

    # avoid divide-by-zero just in case
    defense = max(1, defender.defense)

    base = (lvl * attacker.attack * power) / defense
    damage = int(base / 50) + 2

    # attacker has .types list now
    stab = move_type in attacker.types
    if stab:
        damage = int(damage * 1.5)

    return max(damage, 1), stab


# -----------------------------
# Execute a turn
# -----------------------------
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


# -----------------------------
# Enemy AI
# -----------------------------
def enemy_choose_move(enemy: Pokemon):
    """Very simple AI: pick a random move."""
    return random.choice(enemy.moves)


# -----------------------------
# Player input (CLI)
# -----------------------------
def player_choose_move(player: Pokemon):
    """CLI prompt to choose a move. Returns a move object from player.moves."""
    while True:
        print(f"\nChoose a move for {player.name}:")
        for i, mv in enumerate(player.moves, start=1):
            name, power, move_type, category = _normalize_move(mv)
            if category == "heal":
                print(f"{i}. {name} | Heal: {power}")
            else:
                print(f"{i}. {name} | Type: {move_type} | Power: {power}")

        choice = input("Enter move number: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(player.moves):
                return player.moves[idx - 1]

        print("Invalid choice, try again.")


# -----------------------------
# EXP + Level ups (dummy-safe)
# -----------------------------
def award_exp_if_supported(winner: Pokemon, loser: Pokemon):
    """
    Keeps this file safe even if EXP isn't implemented yet.
    If your Pokemon model has gain_exp(), we call it.
    """
    gain_exp = getattr(winner, "gain_exp", None)
    if not callable(gain_exp):
        return

    # super simple EXP formula (dummy for now)
    exp = 10 + loser.level * 2
    gain_exp(exp)


# -----------------------------
# 1v1 Battle loop (used by Rogue)
# -----------------------------
def run_battle(player: Pokemon, enemy: Pokemon) -> str:
    """
    Runs ONE full fight: player vs enemy.

    Returns:
        "wild_fainted"   -> enemy.hp reached 0
        "player_fainted" -> player.hp reached 0
    """

    while player.hp > 0 and enemy.hp > 0:
        # show HP (simple print; your demo boxes can wrap this later)
        print(f"\n{player.name} HP: {player.hp}/{player.max_hp}")
        print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")

        # pick moves
        player_move = player_choose_move(player)
        enemy_move = enemy_choose_move(enemy)

        # turn order by speed (tie -> player goes first)
        player_first = player.speed >= enemy.speed

        if player_first:
            # player attacks
            res = take_turn(player, enemy, player_move)
            _print_turn_result(res)
            if enemy.hp <= 0:
                print(f"\n💥 {enemy.name} fainted!")
                award_exp_if_supported(player, enemy)
                return "wild_fainted"

            # enemy attacks
            res = take_turn(enemy, player, enemy_move)
            _print_turn_result(res)
            if player.hp <= 0:
                print(f"\n💀 {player.name} fainted!")
                return "player_fainted"
        else:
            # enemy attacks first
            res = take_turn(enemy, player, enemy_move)
            _print_turn_result(res)
            if player.hp <= 0:
                print(f"\n💀 {player.name} fainted!")
                return "player_fainted"

            # player attacks
            res = take_turn(player, enemy, player_move)
            _print_turn_result(res)
            if enemy.hp <= 0:
                print(f"\n💥 {enemy.name} fainted!")
                award_exp_if_supported(player, enemy)
                return "wild_fainted"

    # fallback (shouldn't happen)
    return "player_fainted" if player.hp <= 0 else "wild_fainted"


def _print_turn_result(result: dict) -> None:
    """Simple readable output. Later you can wrap this in your colored boxes."""
    if result["action"] == "heal":
        print(f"{result['user']} used {result['move_name']} → healed {result['healed']} HP")
        return

    stab_txt = " (STAB!)" if result.get("stab") else ""
    print(f"{result['user']} used {result['move_name']}{stab_txt} → {result['damage']} dmg")

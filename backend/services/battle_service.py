"""
Battle logic and mechanics (1v1 only)

Handles:
- Turn order (speed)
- Damage + healing moves
- STAB
- One full turn for UI
- One full fight for Rogue mode

Does NOT handle:
- Endless rogue waves
- Team progression logic
"""

import random
from dataclasses import dataclass, field
from typing import List, Tuple
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
    if isinstance(move, dict):
        return (
            move.get("name", "Unknown"),
            int(move.get("power", 0)),
            str(move.get("type", "normal")).lower(),
            str(move.get("category", "damage")).lower(),
        )

    if isinstance(move, (tuple, list)) and len(move) == 4:
        name, power, move_type, category = move
        return str(name), int(power), str(move_type).lower(), str(category).lower()

    raise TypeError(f"Unsupported move format: {move}")


# -----------------------------
# Damage
# -----------------------------
def damage_calc(attacker: Pokemon, defender: Pokemon, power: int, move_type: str):
    """Basic damage calc with STAB."""
    lvl = (2 * attacker.level) / 5 + 2
    defense = max(1, defender.defense)

    base = (lvl * attacker.attack * power) / defense
    damage = int(base / 50) + 2

    stab = move_type in attacker.types
    if stab:
        damage = int(damage * 1.5)

    return max(damage, 1), stab


# -----------------------------
# Execute a move
# -----------------------------
def take_turn(attacker: Pokemon, defender: Pokemon, move):
    name, power, move_type, category = _normalize_move(move)

    # Healing move
    if category == "heal":
        old_hp = attacker.hp
        attacker.hp = min(attacker.hp + power, attacker.max_hp)
        return {
            "action": "heal",
            "user": attacker.name,
            "move_name": name,
            "healed": attacker.hp - old_hp,
        }

    # Damage move
    dmg, stab = damage_calc(attacker, defender, power, move_type)
    defender.hp = max(defender.hp - dmg, 0)

    return {
        "action": "damage",
        "user": attacker.name,
        "move_name": name,
        "damage": dmg,
        "stab": stab,
    }


# -----------------------------
# Enemy AI
# -----------------------------
def enemy_choose_move(enemy: Pokemon):
    return random.choice(enemy.moves)


# -----------------------------
# EXP
# -----------------------------
def award_exp_if_supported(winner: Pokemon, loser: Pokemon):
    gain_exp = getattr(winner, "gain_exp", None)
    if callable(gain_exp):
        gain_exp(10 + loser.level * 2)


# -----------------------------
# CLI rogue battle (optional)
# -----------------------------
def run_battle(player: Pokemon, enemy: Pokemon) -> str:
    while player.hp > 0 and enemy.hp > 0:
        player_move = random.choice(player.moves)
        enemy_move = enemy_choose_move(enemy)

        player_first = player.speed >= enemy.speed

        if player_first:
            take_turn(player, enemy, player_move)
            if enemy.hp <= 0:
                award_exp_if_supported(player, enemy)
                return "wild_fainted"

            take_turn(enemy, player, enemy_move)
            if player.hp <= 0:
                return "player_fainted"
        else:
            take_turn(enemy, player, enemy_move)
            if player.hp <= 0:
                return "player_fainted"

            take_turn(player, enemy, player_move)
            if enemy.hp <= 0:
                award_exp_if_supported(player, enemy)
                return "wild_fainted"

    return "player_fainted" if player.hp <= 0 else "wild_fainted"


# =============================
# API BATTLE SESSION (UI)
# =============================
@dataclass
class BattleSession:
    team: List[Pokemon]
    active_index: int
    enemy: Pokemon
    log: List[str] = field(default_factory=list)

    def player(self) -> Pokemon:
        return self.team[self.active_index]

    # -----------------------------
    # Switch Pokémon
    # -----------------------------
    def apply_switch(self, idx: int) -> Tuple[bool, str]:
        if idx < 0 or idx >= len(self.team):
            self.log.append("Can't switch: invalid slot.")
            return False, "Invalid slot."

        picked = self.team[idx]
        if picked.hp <= 0:
            self.log.append(f"{picked.name} has fainted!")
            return False, "That Pokémon has fainted."

        self.active_index = idx
        self.log.append(f"Go! {picked.name}!")
        return True, "Switched."

    # -----------------------------
    # Use move
    # -----------------------------
    def apply_move(self, move_index: int) -> Tuple[bool, str]:
        p = self.player()
        e = self.enemy

        # ❌ fainted Pokémon cannot act
        if p.hp <= 0:
            self.log.append(f"{p.name} has fainted! Switch Pokémon.")
            return False, "Active Pokémon fainted."

        # ❌ invalid move
        if move_index < 0 or move_index >= len(p.moves):
            self.log.append("Invalid move.")
            return False, "Invalid move index."

        player_move = p.moves[move_index]
        enemy_move = enemy_choose_move(e)

        player_first = p.speed >= e.speed

        if player_first:
            self._do_action(p, e, player_move)
            if e.hp <= 0:
                self.log.append(f"{e.name} fainted!")
                award_exp_if_supported(p, e)
                return True, "Enemy fainted."

            self._do_action(e, p, enemy_move)
            if p.hp <= 0:
                self.log.append(f"{p.name} fainted!")
                return True, "Player fainted."
        else:
            self._do_action(e, p, enemy_move)
            if p.hp <= 0:
                self.log.append(f"{p.name} fainted!")
                return True, "Player fainted."

            self._do_action(p, e, player_move)
            if e.hp <= 0:
                self.log.append(f"{e.name} fainted!")
                award_exp_if_supported(p, e)
                return True, "Enemy fainted."

        return True, "Turn resolved."

    # -----------------------------
    # Internal executor
    # -----------------------------
    def _do_action(self, attacker: Pokemon, defender: Pokemon, move):
        res = take_turn(attacker, defender, move)

        if res["action"] == "heal":
            self.log.append(
                f"{res['user']} used {res['move_name']} → healed {res['healed']} HP"
            )
        else:
            stab_txt = " (STAB!)" if res.get("stab") else ""
            self.log.append(
                f"{res['user']} used {res['move_name']}{stab_txt} → {res['damage']} dmg"
            )

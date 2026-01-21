"""
Battle logic and mechanics (1v1 only)

Handles:
- Turn order (speed)
- Damage + healing moves
- STAB
- One full turn for UI

EXP:
- Uses backend/services/exp_service.py (single source of truth)

Does NOT handle:
- Endless rogue waves
- Team progression logic
"""

import random
from dataclasses import dataclass, field
from typing import Any, List, Tuple

from backend.models.pokemon import Pokemon
from backend.services.exp_service import award_exp


# -----------------------------
# Move helpers
# -----------------------------
def _normalize_move(move: Any) -> Tuple[str, int, str, str]:
    """
    Supports BOTH formats:
    - dict: {"name": "...", "power": 40, "type": "fire", "category": "damage"}
    - tuple/list: ("Ember", 40, "fire", "damage")

    Returns: (name, power:int, move_type:str, category:str)
    """
    if isinstance(move, dict):
        return (
            str(move.get("name", "Unknown")),
            int(move.get("power", 0) or 0),
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
def damage_calc(attacker: Pokemon, defender: Pokemon, power: int, move_type: str) -> Tuple[int, bool]:
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
def take_turn(attacker: Pokemon, defender: Pokemon, move: Any) -> dict:
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

    # Damage move (default)
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
def enemy_choose_move(enemy: Pokemon) -> Any:
    return random.choice(enemy.moves)


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
    # EXP helper
    # -----------------------------
    def _award_exp_for_faint(self, active: Pokemon, wild: Pokemon) -> None:
        rows = award_exp(team=self.team, active=active, wild=wild)
        for r in rows:
            self.log.append(f"{r.name} gained {r.gained} EXP!")
            if r.leveled_up:
                self.log.append(f"{r.name} leveled up! ({r.before_level} → {r.after_level})")

    # -----------------------------
    # Use move (one full turn)
    # -----------------------------
    def apply_move(self, move_index: int) -> Tuple[bool, str]:
        p = self.player()
        e = self.enemy

        # fainted cannot act
        if p.hp <= 0:
            self.log.append(f"{p.name} has fainted! Switch Pokémon.")
            return False, "Active Pokémon fainted."

        # invalid move
        if move_index < 0 or move_index >= len(p.moves):
            self.log.append("Invalid move.")
            return False, "Invalid move index."

        player_move = p.moves[move_index]
        enemy_move = enemy_choose_move(e)

        def player_attack() -> str | None:
            self._do_action(p, e, player_move)
            if e.hp <= 0:
                self.log.append(f"{e.name} fainted!")
                self._award_exp_for_faint(active=p, wild=e)
                return "Enemy fainted."
            return None

        def enemy_attack() -> str | None:
            self._do_action(e, p, enemy_move)
            if p.hp <= 0:
                self.log.append(f"{p.name} fainted!")
                return "Player fainted."
            return None

        player_first = p.speed >= e.speed

        if player_first:
            out = player_attack()
            if out:
                return True, out

            out = enemy_attack()
            if out:
                return True, out
        else:
            out = enemy_attack()
            if out:
                return True, out

            out = player_attack()
            if out:
                return True, out

        return True, "Turn resolved."

    # -----------------------------
    # Internal executor
    # -----------------------------
    def _do_action(self, attacker: Pokemon, defender: Pokemon, move: Any) -> None:
        res = take_turn(attacker, defender, move)

        if res["action"] == "heal":
            self.log.append(f"{res['user']} used {res['move_name']} → healed {res['healed']} HP")
        else:
            stab_txt = " (STAB!)" if res.get("stab") else ""
            self.log.append(f"{res['user']} used {res['move_name']}{stab_txt} → {res['damage']} dmg")

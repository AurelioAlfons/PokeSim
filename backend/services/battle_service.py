"""
Battle logic and mechanics (1v1 only)

Handles:
- Turn order (speed, quartered by paralysis)
- Damage + healing moves
- Physical/special split, type effectiveness, accuracy, crits, STAB
- Status conditions: burn, paralysis, sleep, poison (the 4 classic
  non-volatile ones) - pure status moves only, one status at a time
- One full turn for UI

EXP:
- Uses /services/exp_service.py (single source of truth)

Does NOT handle:
- Endless rogue waves
- Team progression logic
- Freeze/confusion, or secondary ailment chances on damaging moves
  (Flamethrower's 10% burn etc) - stat-boost "status" moves are still a
  no-op, only ailment-inflicting ones do anything
"""

import random
from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple

from data.type_chart import type_multiplier
from models.pokemon import Pokemon
from services.exp_service import award_exp

CRIT_CHANCE = 1 / 16  # Gen 4 base critical hit rate

# pure status moves only (category == "status") - PokeAPI's raw ailment name
# maps to the short code stored on Pokemon.status. Anything not in here
# (confusion, freeze, stat moves with ailment "none", etc) stays a no-op.
HANDLED_STATUSES = {
    "burn": "brn",
    "paralysis": "par",
    "sleep": "slp",
    "poison": "psn",
}


# -----------------------------
# Move helpers
# -----------------------------
def _normalize_move(move: Any) -> Tuple[str, int, str, str, Optional[int], str]:
    """
    Supports BOTH formats:
    - dict: {"name", "power", "type", "category", "accuracy", "ailment"}
    - tuple/list: ("Ember", 40, "fire", "damage")

    Returns: (name, power:int, move_type:str, category:str, accuracy:int|None, ailment:str)
    accuracy=None means "always hits" (matches PokeAPI's convention).
    ailment defaults to "none" for the tuple format and any move saved
    before this field existed.
    """
    if isinstance(move, dict):
        return (
            str(move.get("name", "Unknown")),
            int(move.get("power", 0) or 0),
            str(move.get("type", "normal")).lower(),
            str(move.get("category", "physical")).lower(),
            move.get("accuracy"),
            str(move.get("ailment") or "none").lower(),
        )

    if isinstance(move, (tuple, list)) and len(move) == 4:
        name, power, move_type, category = move
        return str(name), int(power), str(move_type).lower(), str(category).lower(), None, "none"

    raise TypeError(f"Unsupported move format: {move}")


# -----------------------------
# Damage
# -----------------------------
def damage_calc(attacker: Pokemon, defender: Pokemon, power: int, move_type: str, category: str) -> dict:
    """
    Gen 4-style damage calc: physical/special split, type effectiveness,
    STAB, crit chance, and +-15% random variance.
    """
    if category == "special":
        atk, defn = attacker.sp_attack, max(1, defender.sp_defense)
    else:
        atk, defn = attacker.attack, max(1, defender.defense)

    effectiveness = type_multiplier(move_type, defender.types)
    if effectiveness == 0:
        return {"damage": 0, "stab": False, "effectiveness": 0, "crit": False}

    stab = move_type in attacker.types
    crit = random.random() < CRIT_CHANCE

    lvl = (2 * attacker.level) / 5 + 2
    base = (lvl * atk * power) / defn
    damage = base / 50 + 2

    damage *= 1.5 if stab else 1.0
    damage *= effectiveness
    damage *= 2.0 if crit else 1.0
    damage *= random.uniform(0.85, 1.0)

    # burn only softens physical damage, not special - real mechanic
    if category == "physical" and attacker.status == "brn":
        damage *= 0.5

    return {
        "damage": max(1, int(damage)),
        "stab": stab,
        "effectiveness": effectiveness,
        "crit": crit,
    }


# -----------------------------
# Execute a move
# -----------------------------
def take_turn(attacker: Pokemon, defender: Pokemon, move: Any) -> dict:
    name, power, move_type, category, accuracy, ailment = _normalize_move(move)

    # Healing move (flat HP restore, kept simple - not a real status effect)
    if category == "heal":
        old_hp = attacker.hp
        attacker.hp = min(attacker.hp + power, attacker.max_hp)
        return {
            "action": "heal",
            "user": attacker.name,
            "move_name": name,
            "healed": attacker.hp - old_hp,
            "user_hp": attacker.hp,
            "user_max_hp": attacker.max_hp,
        }

    # Status moves - only the 4 classic non-volatile statuses are handled,
    # everything else (stat moves, confusion, freeze) stays a no-op
    if category == "status":
        status_code = HANDLED_STATUSES.get(ailment)
        if status_code is None:
            return {"action": "status", "user": attacker.name, "move_name": name, "applied": False, "handled": False}

        if defender.status is not None:
            return {"action": "status", "user": attacker.name, "move_name": name, "applied": False, "handled": True}

        defender.status = status_code
        if status_code == "slp":
            defender.status_turns = random.randint(1, 3)

        return {
            "action": "status",
            "user": attacker.name,
            "move_name": name,
            "applied": True,
            "handled": True,
            "status": status_code,
            "target": defender.name,
        }

    # Accuracy check (None = always hits)
    if accuracy is not None and random.uniform(0, 100) > accuracy:
        return {
            "action": "miss",
            "user": attacker.name,
            "move_name": name,
        }

    # Damage move (physical/special)
    result = damage_calc(attacker, defender, power, move_type, category)
    defender.hp = max(defender.hp - result["damage"], 0)

    return {
        "action": "damage",
        "user": attacker.name,
        "move_name": name,
        "damage": result["damage"],
        "stab": result["stab"],
        "effectiveness": result["effectiveness"],
        "crit": result["crit"],
        "target": defender.name,
        "target_hp": defender.hp,
        "target_max_hp": defender.max_hp,
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
    team_id: Any = "sample"
    team_name: str = "Sample Team"

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
    # Status helpers
    # -----------------------------
    def _can_act(self, pokemon: Pokemon) -> bool:
        """Sleep/paralysis can eat a turn entirely - logs why, returns whether it can still move."""
        if pokemon.status == "slp":
            pokemon.status_turns -= 1
            if pokemon.status_turns <= 0:
                pokemon.status = None
                pokemon.status_turns = 0
                self.log.append(f"{pokemon.name} woke up!")
                return True
            self.log.append(f"{pokemon.name} is fast asleep.")
            return False

        if pokemon.status == "par" and random.random() < 0.25:
            self.log.append(f"{pokemon.name} is fully paralyzed!")
            return False

        return True

    def _apply_end_of_turn_status(self) -> str | None:
        """Burn/poison chip damage after both attacks resolve. Returns a faint message if this kills someone."""
        p = self.player()
        e = self.enemy

        for pokemon, is_enemy in ((e, True), (p, False)):
            if pokemon.hp <= 0 or pokemon.status not in ("brn", "psn"):
                continue

            fraction = 1 / 16 if pokemon.status == "brn" else 1 / 8
            dmg = max(1, int(pokemon.max_hp * fraction))
            pokemon.hp = max(0, pokemon.hp - dmg)

            status_word = "burn" if pokemon.status == "brn" else "poison"
            self.log.append(f"{pokemon.name} is hurt by {status_word}! (-{dmg} HP)")

            if pokemon.hp <= 0:
                self.log.append(f"{pokemon.name} fainted!")
                if is_enemy:
                    self._award_exp_for_faint(active=p, wild=e)
                    return "Enemy fainted."
                return "Player fainted."

        return None

    @staticmethod
    def _effective_speed(pokemon: Pokemon) -> float:
        # paralysis quarters effective speed - real Gen 4 mechanic, not just skip chance
        return pokemon.speed / 4 if pokemon.status == "par" else pokemon.speed

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
            if self._can_act(p):
                self._do_action(p, e, player_move)
                if e.hp <= 0:
                    self.log.append(f"{e.name} fainted!")
                    self._award_exp_for_faint(active=p, wild=e)
                    return "Enemy fainted."
            return None

        def enemy_attack() -> str | None:
            if self._can_act(e):
                self._do_action(e, p, enemy_move)
                if p.hp <= 0:
                    self.log.append(f"{p.name} fainted!")
                    return "Player fainted."
            return None

        player_first = self._effective_speed(p) >= self._effective_speed(e)

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

        out = self._apply_end_of_turn_status()
        if out:
            return True, out

        return True, "Turn resolved."

    # -----------------------------
    # Internal executor
    # -----------------------------
    def _do_action(self, attacker: Pokemon, defender: Pokemon, move: Any) -> None:
        res = take_turn(attacker, defender, move)
        action = res["action"]

        if action == "heal":
            self.log.append(f"{res['user']} used {res['move_name']} → healed {res['healed']} HP")
        elif action == "status":
            if res.get("applied"):
                status_words = {"brn": "burned", "par": "paralyzed", "slp": "put to sleep", "psn": "poisoned"}
                word = status_words[res["status"]]
                self.log.append(f"{res['user']} used {res['move_name']} → {res['target']} was {word}!")
            elif res.get("handled"):
                self.log.append(f"{res['user']} used {res['move_name']}, but it failed!")
            else:
                self.log.append(f"{res['user']} used {res['move_name']}, but nothing happened.")
        elif action == "miss":
            self.log.append(f"{res['user']} used {res['move_name']} → it missed!")
        else:
            tags = []
            if res.get("stab"):
                tags.append("STAB!")
            if res.get("crit"):
                tags.append("Critical hit!")
            eff = res.get("effectiveness", 1)
            if eff > 1:
                tags.append("Super effective!")
            elif 0 < eff < 1:
                tags.append("Not very effective...")
            tag_txt = f" ({' '.join(tags)})" if tags else ""
            self.log.append(f"{res['user']} used {res['move_name']}{tag_txt} → {res['damage']} dmg")

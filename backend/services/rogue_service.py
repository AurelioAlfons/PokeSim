# backend/services/rogue_service.py
"""
Rogue (endless) mode runner.

This file ONLY handles the endless "wave" loop:
- spawn wild
- run 1v1 battle using battle_service
- if active faints -> auto switch to next alive
- if wild faints -> next wave + rewards
- run ends when whole team is wiped

How to use (from demo.py):
    from backend.services.rogue_service import run_rogue_run
    run_rogue_run(team)

Requirements / expectations:
- Your Pokemon objects have: name, level, hp, max_hp
- Your battle function exists and returns a simple outcome:
    "wild_fainted"  -> player won this fight
    "player_fainted"-> active player pokemon fainted
  (If your battle returns True/False instead, see the adapter notes below.)
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import List, Optional, Literal


BattleOutcome = Literal["wild_fainted", "player_fainted"]


@dataclass
class RogueConfig:
    # level rule: wild = (lowest alive level - 2) + difficulty ramp
    level_offset: int = -2

    # difficulty ramp: every N waves add +1 level
    level_ramp_every: int = 3

    # small heal after each win (percent of max hp)
    between_fight_heal_pct: float = 0.15

    # EXP rewards (you can keep as stubs if you don't have exp yet)
    base_exp: int = 10
    exp_per_wild_level: int = 2
    active_bonus_mult: float = 1.5


# ----------------------------
# Public entry point
# ----------------------------

def run_rogue_run(team: List[object], config: RogueConfig = RogueConfig()) -> None:
    """
    Runs endless rogue mode until the whole team is wiped.
    """
    wave = 1
    wins = 0

    while True:
        if is_team_wiped(team):
            print(f"\n💀 RUN OVER. You cleared {wins} wins.\n")
            return

        active = next_alive_pokemon(team)
        wild = generate_wild_pokemon(team, wave, config)

        print(f"\n=== WAVE {wave} ===")
        print(f"Wild {wild.name} (Lv {wild.level}) appeared!")

        outcome = _run_battle_adapter(active, wild)

        if outcome == "wild_fainted":
            wins += 1

            # rewards
            award_exp(team, active, wild, config)
            small_between_fight_heal(team, config)

            print(f"✅ You won! Total wins: {wins}")
            wave += 1

        elif outcome == "player_fainted":
            # active fainted; rogue continues if team still has alive mons
            print(f"⚠️  {active.name} fainted!")
            if is_team_wiped(team):
                print(f"\n💀 RUN OVER. You cleared {wins} wins.\n")
                return
            else:
                nxt = next_alive_pokemon(team)
                print(f"➡️  Go! {nxt.name}!")
                # same wave continues vs same wild (OPTION A)
                # If you want a NEW wild after fainting, change logic here.
                # We'll continue the same fight by just looping again without wave++,
                # but we need to re-run battle with the new active and the same wild.
                # So: continue the while-loop but DO NOT change wave.
                # Re-run battle immediately:
                outcome2 = _run_battle_adapter(nxt, wild)
                if outcome2 == "wild_fainted":
                    wins += 1
                    award_exp(team, nxt, wild, config)
                    small_between_fight_heal(team, config)
                    print(f"✅ You won! Total wins: {wins}")
                    wave += 1
                else:
                    # if the next one also fainted, loop will naturally continue
                    # and keep swapping until team wiped or wild dies
                    continue
        else:
            raise ValueError(f"Unknown battle outcome: {outcome}")


# ----------------------------
# Core helpers
# ----------------------------

def is_team_wiped(team: List[object]) -> bool:
    return all(getattr(p, "hp", 0) <= 0 for p in team)

def next_alive_pokemon(team: List[object]) -> object:
    for p in team:
        if getattr(p, "hp", 0) > 0:
            return p
    # if no alive, return None-ish (should be handled by is_team_wiped)
    raise RuntimeError("No alive Pokemon found, but team not marked as wiped.")

def lowest_alive_level(team: List[object]) -> int:
    levels = [getattr(p, "level", 1) for p in team if getattr(p, "hp", 0) > 0]
    return min(levels) if levels else 1

def generate_wild_pokemon(team: List[object], wave: int, config: RogueConfig) -> object:
    """
    Generates a wild pokemon with level based on:
        (lowest alive team level + offset) + ramp
    You MUST implement make_random_gen4_pokemon(level) in your project
    (or swap this out to your existing pokemon factory).
    """
    base_level = max(1, lowest_alive_level(team) + config.level_offset)
    ramp = wave // max(1, config.level_ramp_every)  # +1 every N waves
    wild_level = max(1, base_level + ramp)

    return make_random_gen4_pokemon(wild_level)

def small_between_fight_heal(team: List[object], config: RogueConfig) -> None:
    pct = max(0.0, float(config.between_fight_heal_pct))
    if pct <= 0:
        return

    for p in team:
        if getattr(p, "hp", 0) > 0:
            max_hp = getattr(p, "max_hp", getattr(p, "hp", 0))
            heal = max(1, int(max_hp * pct))
            p.hp = min(max_hp, p.hp + heal)

def award_exp(team: List[object], active: object, wild: object, config: RogueConfig) -> None:
    """
    Safe even if you don't have EXP system yet.
    If Pokemon has gain_exp(exp) method, it will be used.
    """
    base = config.base_exp + getattr(wild, "level", 1) * config.exp_per_wild_level

    for p in team:
        if getattr(p, "hp", 0) <= 0:
            continue

        exp = base
        if p is active:
            exp = int(base * config.active_bonus_mult)

        gain_exp = getattr(p, "gain_exp", None)
        if callable(gain_exp):
            gain_exp(exp)
        # else: silently ignore (you can add exp system later)


# ----------------------------
# Battle adapter
# ----------------------------

def _run_battle_adapter(player_pokemon: object, wild_pokemon: object) -> BattleOutcome:
    """
    This wraps your existing battle logic so rogue_service stays stable.

    EXPECTED IDEAL:
        from backend.services.battle_service import run_battle
        outcome = run_battle(player_pokemon, wild_pokemon)
        return "wild_fainted" or "player_fainted"

    If your battle function returns True/False:
        True  -> player won (wild fainted)
        False -> player lost (player fainted)
    this adapter will convert it.

    If you have a different function name, just update this adapter.
    """
    try:
        # Change this import/function name to match your project
        from backend.services.battle_service import run_battle  # type: ignore
    except Exception as e:
        raise ImportError(
            "Could not import run_battle from backend.services.battle_service.\n"
            "Fix: make sure battle_service.py has a function named run_battle(active, wild)\n"
            "OR edit _run_battle_adapter() to call your actual battle function."
        ) from e

    result = run_battle(player_pokemon, wild_pokemon)

    # If your run_battle already returns a string outcome, pass it through
    if result in ("wild_fainted", "player_fainted"):
        return result  # type: ignore

    # If it's boolean:
    if isinstance(result, bool):
        return "wild_fainted" if result else "player_fainted"

    # If it's dict-like and has a winner:
    if isinstance(result, dict):
        winner = result.get("winner")
        if winner == "player":
            return "wild_fainted"
        if winner == "wild":
            return "player_fainted"

    raise ValueError(
        f"run_battle() returned unsupported value: {result!r}\n"
        "Make it return 'wild_fainted'/'player_fainted' or True/False."
    )


# ----------------------------
# Wild factory (stub)
# ----------------------------

def make_random_gen4_pokemon(level: int) -> object:
    """
    Stub for now.
    Replace this with your real factory (PokéAPI or your own DB).
    """
    # Example minimal dummy to prevent crashes if you run it early:
    class _Wild:
        def __init__(self, name: str, level: int):
            self.name = name
            self.level = level
            self.max_hp = 20 + level * 3
            self.hp = self.max_hp

    names = ["Bidoof", "Starly", "Shinx", "Kricketot", "Buizel", "Geodude"]
    return _Wild(random.choice(names), level)

# backend/services/rogue_service.py
"""
Rogue (endless) mode runner.

This file ONLY handles the endless "wave" loop:
- spawn wild
- run 1v1 battle using battle_service.run_battle()
- if active faints -> auto switch to next alive and keep fighting same wild
- if wild faints -> next wave + rewards
- run ends when whole team is wiped
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import List


# ✅ Rogue uses the battle engine directly (no adapter)
from backend.services.battle_service import run_battle


@dataclass
class RogueConfig:
    # level rule: wild = (lowest alive level - 2) + difficulty ramp
    level_offset: int = -2

    # difficulty ramp: every N waves add +1 level
    level_ramp_every: int = 3

    # small heal after each win (percent of max hp)
    between_fight_heal_pct: float = 0.15

    # EXP rewards (safe even if exp isn't implemented)
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

        wild = generate_wild_pokemon(team, wave, config)

        print(f"\n=== WAVE {wave} ===")
        print(f"Wild {wild.name} (Lv {wild.level}) appeared!")

        # Fight this SAME wild until it faints OR the team wipes
        while wild.hp > 0:
            if is_team_wiped(team):
                print(f"\n💀 RUN OVER. You cleared {wins} wins.\n")
                return

            active = next_alive_pokemon(team)
            print(f"\n➡️  Go! {active.name}!")

            outcome = run_battle(active, wild)

            if outcome == "wild_fainted":
                wins += 1

                # rewards
                award_exp(team, active, wild, config)
                small_between_fight_heal(team, config)

                print(f"✅ You won! Total wins: {wins}")
                wave += 1
                break  # go spawn next wild

            if outcome == "player_fainted":
                print(f"⚠️  {active.name} fainted!")
                # loop continues, next_alive_pokemon will swap automatically
                continue

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
    raise RuntimeError("No alive Pokemon found, but team not marked as wiped.")


def lowest_alive_level(team: List[object]) -> int:
    levels = [getattr(p, "level", 1) for p in team if getattr(p, "hp", 0) > 0]
    return min(levels) if levels else 1


def generate_wild_pokemon(team: List[object], wave: int, config: RogueConfig) -> object:
    """
    Generates a wild pokemon with level based on:
        (lowest alive team level + offset) + ramp
    """
    base_level = max(1, lowest_alive_level(team) + config.level_offset)
    ramp = (wave - 1) // max(1, config.level_ramp_every)  # +1 every N waves
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


# ----------------------------
# Wild factory (stub)
# ----------------------------
def make_random_gen4_pokemon(level: int) -> object:
    """
    Stub for now.
    Replace this with your real factory (PokéAPI or your own DB).
    """
    class _Wild:
        def __init__(self, name: str, level: int):
            self.name = name
            self.level = level
            self.max_hp = 20 + level * 3
            self.hp = self.max_hp

    names = ["Bidoof", "Starly", "Shinx", "Kricketot", "Buizel", "Geodude"]
    return _Wild(random.choice(names), level)

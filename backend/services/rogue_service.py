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

from backend.models.pokemon import Pokemon
from backend.services.battle_service import run_battle


@dataclass
class RogueConfig:
    # level rule: wild = (lowest alive level - 2) + difficulty ramp
    level_offset: int = -2

    # difficulty ramp: every N waves add +1 level
    level_ramp_every: int = 3

    # small heal after each win (percent of max hp)
    between_fight_heal_pct: float = 0.15

    # EXP rewards
    base_exp: int = 10
    exp_per_wild_level: int = 2

    # active mon gets more exp
    active_bonus_mult: float = 1.5


# ----------------------------
# Public entry point
# ----------------------------
def run_rogue_run(team: List[Pokemon], config: RogueConfig = RogueConfig()) -> None:
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
def is_team_wiped(team: List[Pokemon]) -> bool:
    return all(p.hp <= 0 for p in team)


def next_alive_pokemon(team: List[Pokemon]) -> Pokemon:
    for p in team:
        if p.hp > 0:
            return p
    raise RuntimeError("No alive Pokemon found, but team not marked as wiped.")


def lowest_alive_level(team: List[Pokemon]) -> int:
    levels = [p.level for p in team if p.hp > 0]
    return min(levels) if levels else 1


def generate_wild_pokemon(team: List[Pokemon], wave: int, config: RogueConfig) -> Pokemon:
    """
    Generates a wild pokemon with level based on:
        (lowest alive team level + offset) + ramp
    """
    base_level = max(1, lowest_alive_level(team) + config.level_offset)
    ramp = (wave - 1) // max(1, config.level_ramp_every)  # +1 every N waves
    wild_level = max(1, base_level + ramp)

    return make_random_gen4_pokemon(wild_level)


def small_between_fight_heal(team: List[Pokemon], config: RogueConfig) -> None:
    pct = max(0.0, float(config.between_fight_heal_pct))
    if pct <= 0:
        return

    for p in team:
        if p.hp > 0:
            heal = max(1, int(p.max_hp * pct))
            p.hp = min(p.max_hp, p.hp + heal)


def award_exp(team: List[Pokemon], active: Pokemon, wild: Pokemon, config: RogueConfig) -> None:
    """
    Gives EXP to alive team members.
    Active gets a bonus multiplier.
    Prints EXP gained + level ups.
    """
    base = config.base_exp + (wild.level * config.exp_per_wild_level)

    print("\n✨ EXP GAINED:")
    for p in team:
        if p.hp <= 0:
            continue

        exp_gain = base
        if p is active:
            exp_gain = int(base * config.active_bonus_mult)

        before_level = p.level

        leveled_up = p.gain_exp(exp_gain)

        # Clean output for demo
        if leveled_up:
            print(f"  - {p.name} +{exp_gain} EXP → Lv {before_level} → Lv {p.level} 🎉")
        else:
            print(f"  - {p.name} +{exp_gain} EXP")


# ----------------------------
# Wild factory (now returns real Pokemon)
# ----------------------------
def make_random_gen4_pokemon(level: int) -> Pokemon:
    """
    Simple Gen4-ish wild Pokemon factory for Rogue mode.
    Replace later with PokéAPI / DB.
    """
    wild_pool = [
        {
            "id": 399,
            "name": "Bidoof",
            "types": ["normal"],
            "base_stats": {"hp": 59, "atk": 45, "def": 40, "spd": 31},
            "moves": [
                {"name": "Tackle", "power": 40, "type": "normal", "category": "damage"},
                {"name": "Rest", "power": 0, "type": "normal", "category": "heal"},
            ],
        },
        {
            "id": 396,
            "name": "Starly",
            "types": ["normal", "flying"],
            "base_stats": {"hp": 40, "atk": 55, "def": 30, "spd": 60},
            "moves": [
                {"name": "Quick Attack", "power": 40, "type": "normal", "category": "damage"},
                {"name": "Growl", "power": 0, "type": "normal", "category": "status"},
            ],
        },
        {
            "id": 403,
            "name": "Shinx",
            "types": ["electric"],
            "base_stats": {"hp": 45, "atk": 65, "def": 34, "spd": 45},
            "moves": [
                {"name": "Tackle", "power": 40, "type": "normal", "category": "damage"},
                {"name": "Thunder Shock", "power": 40, "type": "electric", "category": "damage"},
            ],
        },
        {
            "id": 401,
            "name": "Kricketot",
            "types": ["bug"],
            "base_stats": {"hp": 37, "atk": 25, "def": 41, "spd": 25},
            "moves": [
                {"name": "Pound", "power": 40, "type": "normal", "category": "damage"},
                {"name": "Rest", "power": 0, "type": "normal", "category": "heal"},
            ],
        },
        {
            "id": 418,
            "name": "Buizel",
            "types": ["water"],
            "base_stats": {"hp": 55, "atk": 65, "def": 35, "spd": 85},
            "moves": [
                {"name": "Quick Attack", "power": 40, "type": "normal", "category": "damage"},
                {"name": "Water Gun", "power": 40, "type": "water", "category": "damage"},
            ],
        },
        {
            "id": 74,
            "name": "Geodude",
            "types": ["rock", "ground"],
            "base_stats": {"hp": 40, "atk": 80, "def": 100, "spd": 20},
            "moves": [
                {"name": "Tackle", "power": 40, "type": "normal", "category": "damage"},
                {"name": "Rock Throw", "power": 50, "type": "rock", "category": "damage"},
            ],
        },
    ]

    data = random.choice(wild_pool)

    return Pokemon(
        pokedex_id=data["id"],
        name=data["name"],
        level=level,
        types=data["types"],
        base_stats=data["base_stats"],
        moves=data["moves"],
        ability=None,
    )

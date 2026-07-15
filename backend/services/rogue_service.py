# backend/services/rogue_service.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from models.pokemon import Pokemon


def team_wiped(team: list[Pokemon]) -> bool:
    return all(p.hp <= 0 for p in team)


def next_alive(team: list[Pokemon]) -> Optional[Pokemon]:
    """First non-fainted Pokemon in the team, or None if the team is wiped."""
    return next((p for p in team if p.hp > 0), None)


def between_fight_heal(team: list[Pokemon], percent: float = 0.15) -> None:
    """Small heal between fights (used by rogue mode) - also clears status, doesn't carry between waves."""
    for p in team:
        if p.hp > 0:
            heal = max(1, int(p.max_hp * percent))
            p.hp = min(p.max_hp, p.hp + heal)
            p.status = None
            p.status_turns = 0


def lowest_alive_level(team: list[Pokemon]) -> int:
    alive_levels = [p.level for p in team if p.hp > 0]
    return min(alive_levels) if alive_levels else 1


@dataclass(frozen=True)
class WaveInfo:
    wave: int
    wild_level: int


def compute_wave_info(team: list[Pokemon], wave: int) -> WaveInfo:
    # Current rule: wild is based on your weakest alive mon (minus 4), min level 1
    wild_level = max(1, lowest_alive_level(team) - 4)
    return WaveInfo(wave=wave, wild_level=wild_level)

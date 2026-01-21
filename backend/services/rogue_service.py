# backend/services/rogue_service.py
from __future__ import annotations

from dataclasses import dataclass
from backend.models.pokemon import Pokemon


def next_alive(team: list[Pokemon]) -> Pokemon | None:
    for p in team:
        if p.hp > 0:
            return p
    return None


def team_wiped(team: list[Pokemon]) -> bool:
    return all(p.hp <= 0 for p in team)


def lowest_alive_level(team: list[Pokemon]) -> int:
    alive = [p.level for p in team if p.hp > 0]
    return min(alive) if alive else 1


def between_fight_heal(team: list[Pokemon], percent: float = 0.15) -> None:
    """Small heal between fights (used by rogue mode)."""
    for p in team:
        if p.hp > 0:
            heal = max(1, int(p.max_hp * percent))
            p.hp = min(p.max_hp, p.hp + heal)


@dataclass
class WaveInfo:
    wave: int
    base_level: int
    ramp: int
    wild_level: int


def compute_wave_info(team: list[Pokemon], wave: int) -> WaveInfo:
    wild_level = max(1, lowest_alive_level(team) - 2)
    return WaveInfo(
        wave=wave,
        base_level=wild_level,
        ramp=0,
        wild_level=wild_level,
    )
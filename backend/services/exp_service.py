# backend/services/exp_service.py
from __future__ import annotations

from dataclasses import dataclass
from backend.models.pokemon import Pokemon


@dataclass
class ExpGainRow:
    name: str
    gained: int
    leveled_up: bool
    before_level: int
    after_level: int


def award_exp(team: list[Pokemon], active: Pokemon, wild: Pokemon) -> list[ExpGainRow]:
    """
    Reusable EXP logic.
    Returns rows that UI/CLI can render however they want.
    """
    base_exp = 10 + (wild.level * 2)
    active_mult = 1.5

    rows: list[ExpGainRow] = []
    for p in team:
        if p.hp <= 0:
            continue

        gained = int(base_exp * active_mult) if p is active else base_exp
        before = p.level
        leveled = p.gain_exp(gained)  # assumes your Pokemon model has this
        after = p.level

        rows.append(
            ExpGainRow(
                name=p.name,
                gained=gained,
                leveled_up=bool(leveled),
                before_level=before,
                after_level=after,
            )
        )

    return rows

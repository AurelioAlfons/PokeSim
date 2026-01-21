"""
Team helpers (session/team management).

Keeping this separate so battle_service.py stays focused on battle mechanics.
"""

from typing import List
from backend.models.pokemon import Pokemon


def reset_team_full(team: List[Pokemon]) -> None:
    """
    Full reset for /start or /run:
    - Heal everyone
    - Reset EXP fields if present
    """
    for p in team:
        p.hp = p.max_hp

        if hasattr(p, "exp"):
            p.exp = 0
        if hasattr(p, "exp_to_next_level"):
            p.exp_to_next_level = getattr(p, "exp_to_next_level", 0)

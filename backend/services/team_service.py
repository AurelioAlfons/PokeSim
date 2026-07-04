"""
Team helpers (session/team management).

Keeping this separate so battle_service.py stays focused on battle mechanics.
"""

from typing import List
from models.pokemon import Pokemon


def reset_team_full(team: List[Pokemon]) -> None:
    """
    Full reset for /start or /run:
    - Heal everyone
    - Reset EXP fields if present
    """
    for p in team:
        p.hp = p.max_hp
        p.reset_exp()

# backend/services/wild_factory.py
from __future__ import annotations

import random
from backend.models.pokemon import Pokemon


def make_wild(level: int) -> Pokemon:
    pool = [
        (
            "Bidoof",
            399,
            ["normal"],
            {"hp": 59, "atk": 45, "def": 40, "spd": 31},
            [
                {"name": "Tackle", "power": 40, "type": "normal", "category": "damage"},
                {"name": "Rest", "power": 5, "type": "normal", "category": "heal"},
            ],
        ),
        (
            "Starly",
            396,
            ["normal", "flying"],
            {"hp": 40, "atk": 55, "def": 30, "spd": 60},
            [
                {"name": "Tackle", "power": 40, "type": "normal", "category": "damage"},
                {"name": "QuickAtk", "power": 40, "type": "normal", "category": "damage"},
            ],
        ),
        (
            "Shinx",
            403,
            ["electric"],
            {"hp": 45, "atk": 65, "def": 34, "spd": 45},
            [
                {"name": "Tackle", "power": 40, "type": "normal", "category": "damage"},
                {"name": "Spark", "power": 40, "type": "electric", "category": "damage"},
            ],
        ),
    ]

    name, dex, types, stats, moves = random.choice(pool)
    return Pokemon(
        pokedex_id=dex,
        name=name,
        level=level,
        types=types,
        base_stats=stats,
        moves=moves,
    )

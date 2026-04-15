# backend/services/wild_factory.py
from __future__ import annotations

import random
from models.pokemon import Pokemon


def make_wild(level: int) -> Pokemon:
    pool = [
        # -----------------------------
        # Staraptor
        # -----------------------------
        (
            "Staraptor",
            398,
            ["normal", "flying"],
            {"hp": 85, "atk": 120, "def": 70, "spd": 100},
            [
                {"name": "Brave Bird", "power": 120, "type": "flying", "category": "damage"},
                {"name": "Close Combat", "power": 120, "type": "fighting", "category": "damage"},
                {"name": "Quick Attack", "power": 40, "type": "normal", "category": "damage"},
            ],
        ),

        # -----------------------------
        # Lucario
        # -----------------------------
        (
            "Lucario",
            448,
            ["fighting", "steel"],
            {"hp": 70, "atk": 110, "def": 70, "spd": 90},
            [
                {"name": "Aura Sphere", "power": 80, "type": "fighting", "category": "damage"},
                {"name": "Flash Cannon", "power": 80, "type": "steel", "category": "damage"},
                {"name": "Extreme Speed", "power": 80, "type": "normal", "category": "damage"},
            ],
        ),

        # -----------------------------
        # Garchomp
        # -----------------------------
        (
            "Garchomp",
            445,
            ["dragon", "ground"],
            {"hp": 108, "atk": 130, "def": 95, "spd": 102},
            [
                {"name": "Dragon Claw", "power": 80, "type": "dragon", "category": "damage"},
                {"name": "Earthquake", "power": 100, "type": "ground", "category": "damage"},
                {"name": "Crunch", "power": 80, "type": "dark", "category": "damage"},
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

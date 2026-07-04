# backend/services/wild_factory.py
from __future__ import annotations

import random

from models.pokemon import Pokemon
from services.pokedex_service import GEN4_DEX_RANGE, get_detail


def make_wild(level: int) -> Pokemon:
    """Builds a random wild Pokemon from the full Gen 4 dex via PokeAPI."""
    dex_id = random.choice(GEN4_DEX_RANGE)
    data = get_detail(dex_id)

    # Only moves the Pokemon has actually learned by this level, newest first
    learned = [m for m in data["moves"] if m["level_learned_at"] <= level]
    if not learned:
        learned = data["moves"][:1]  # fall back to its earliest move
    moves = learned[-4:]

    ability = random.choice(data["abilities"])["name"]

    return Pokemon(
        pokedex_id=data["id"],
        name=data["name"].title(),
        level=level,
        types=data["types"],
        base_stats=data["base_stats"],
        moves=moves,
        ability=ability,
    )

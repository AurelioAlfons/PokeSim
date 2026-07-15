# backend/services/pokedex_service.py
#
# Gen 4 dex data (National Dex #387 Turtwig - #493 Arceus) is fully static,
# so we don't hit PokeAPI at request time at all - gen4_dex.json is a
# one-time snapshot built by scripts/build_gen4_dex.py, and this just reads
# it off disk. list_summary/get_detail below are dumb lookups, no reshaping.

import json
import os

from services.pokeapi_client import get_move

# Which games' level-up lists we care about. Kept here since
# build_gen4_dex.py imports _level_up_moves() from this module.
VERSION_GROUP = "platinum"

GEN4_DEX_RANGE = range(387, 494)

_DEX_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "gen4_dex.json")
with open(_DEX_PATH, encoding="utf-8") as f:
    _DEX = json.load(f)
_DEX_BY_ID = {entry["id"]: entry for entry in _DEX}


def _sprite_path(dex_id: int) -> str:
    return f"/assets/SVG/{dex_id}.svg"


def list_summary() -> list:
    """Lightweight list for browsing the dex (team builder grid)."""
    return [
        {
            "id": entry["id"],
            "name": entry["name"],
            "types": entry["types"],
            "sprite": entry["sprite"],
        }
        for entry in _DEX
    ]


def _level_up_moves(data: dict) -> list:
    """Level-up moves for VERSION_GROUP, each resolved to full move info."""
    moves = []
    for entry in data["moves"]:
        learn = next(
            (vgd for vgd in entry["version_group_details"]
             if vgd["version_group"]["name"] == VERSION_GROUP
             and vgd["move_learn_method"]["name"] == "level-up"),
            None,
        )
        if learn is None:
            continue

        move_data = get_move(entry["move"]["name"])
        # meta can be missing on a handful of oddball moves - "none" matches
        # PokeAPI's own convention for "doesn't inflict a status"
        ailment = move_data.get("meta", {}).get("ailment", {}).get("name", "none")
        moves.append({
            "name": move_data["name"].replace("-", " ").title(),
            "power": move_data["power"] or 0,
            "type": move_data["type"]["name"],
            "category": move_data["damage_class"]["name"],  # physical/special/status
            "accuracy": move_data["accuracy"],  # None means "never misses"
            "ailment": ailment,  # e.g. "burn", "paralysis", "sleep", "poison", "none"
            "level_learned_at": learn["level_learned_at"],
        })

    moves.sort(key=lambda m: m["level_learned_at"])
    return moves


def get_detail(dex_id: int) -> dict:
    """Full detail for one Pokemon: stats, types, abilities, level-up moves."""
    return _DEX_BY_ID[dex_id]

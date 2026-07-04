# backend/services/pokedex_service.py
#
# Shapes raw PokeAPI data into what the rest of PokeSim actually needs.
# Scoped to Gen 4 (National Dex #387 Turtwig - #493 Arceus) since that's
# what this project covers and what we have sprites for.

from services.pokeapi_client import get_pokemon, get_move

GEN4_DEX_RANGE = range(387, 494)

# Which games' level-up lists we care about. Keeping this to one version
# group is enough for a Gen 4 team builder without pulling in every TM/egg
# move too.
VERSION_GROUP = "platinum"


def _sprite_path(dex_id: int) -> str:
    return f"/assets/SVG/{dex_id}.svg"


def list_summary() -> list:
    """Lightweight list for browsing the dex (team builder grid)."""
    out = []
    for dex_id in GEN4_DEX_RANGE:
        data = get_pokemon(dex_id)
        out.append({
            "id": dex_id,
            "name": data["name"],
            "types": [t["type"]["name"] for t in data["types"]],
            "sprite": _sprite_path(dex_id),
        })
    return out


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
        moves.append({
            "name": move_data["name"].replace("-", " ").title(),
            "power": move_data["power"] or 0,
            "type": move_data["type"]["name"],
            "category": move_data["damage_class"]["name"],  # physical/special/status
            "accuracy": move_data["accuracy"],  # None means "never misses"
            "level_learned_at": learn["level_learned_at"],
        })

    moves.sort(key=lambda m: m["level_learned_at"])
    return moves


def get_detail(dex_id: int) -> dict:
    """Full detail for one Pokemon: stats, types, abilities, level-up moves."""
    data = get_pokemon(dex_id)
    stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}

    return {
        "id": dex_id,
        "name": data["name"],
        "types": [t["type"]["name"] for t in data["types"]],
        "sprite": _sprite_path(dex_id),
        "base_stats": {
            "hp": stats["hp"],
            "atk": stats["attack"],
            "def": stats["defense"],
            "spatk": stats["special-attack"],
            "spdef": stats["special-defense"],
            "spd": stats["speed"],
        },
        "abilities": [
            {"name": a["ability"]["name"], "hidden": a["is_hidden"]}
            for a in data["abilities"]
        ],
        "moves": _level_up_moves(data),
    }

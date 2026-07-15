# backend/scripts/build_gen4_dex.py
#
# One-off build step, not something that runs on every deploy. Hits PokeAPI
# for all 107 Gen 4 species + their level-up moves and dumps the result to
# data/gen4_dex.json, so pokedex_service.py can serve everything from disk
# instead of doing 100+ live requests per pageload.
#
# Run from project root: python -m backend.scripts.build_gen4_dex
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.pokeapi_client import get_pokemon
from services.pokedex_service import GEN4_DEX_RANGE, _level_up_moves, _sprite_path

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "gen4_dex.json")


def build_entry(dex_id: int) -> dict:
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


def main():
    dex = []
    for dex_id in GEN4_DEX_RANGE:
        print(f"fetching {dex_id}...")
        dex.append(build_entry(dex_id))

    out_path = os.path.abspath(OUT_PATH)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dex, f, separators=(",", ":"))

    print(f"wrote {len(dex)} entries to {out_path}")


if __name__ == "__main__":
    main()

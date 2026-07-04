# backend/test/demo.py
#
# CLI is meant to be run from the project root (`python -m backend.test.demo`),
# but the modules it pulls in (battle_service, rogue_service, ...) import
# each other with bare names like `from models.pokemon import ...`, which
# only resolves if backend/ itself is also on sys.path. This puts it there.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models.pokemon import Pokemon
from backend.cli.rogue_cli import rogue_run_cli


def build_demo_team():
    chimchar = Pokemon(
        pokedex_id=390,
        name="Chimchar",
        level=16,
        types=["fire"],
        base_stats={"hp": 44, "atk": 58, "def": 44, "spatk": 58, "spdef": 44, "spd": 61},
        moves=[
            {"name": "Scratch", "power": 40, "type": "normal", "category": "physical", "accuracy": 100},
            {"name": "Ember", "power": 40, "type": "fire", "category": "special", "accuracy": 100},
        ],
    )

    bidoof = Pokemon(
        pokedex_id=399,
        name="Bidoof",
        level=6,
        types=["normal"],
        base_stats={"hp": 59, "atk": 45, "def": 40, "spatk": 35, "spdef": 40, "spd": 31},
        moves=[
            {"name": "Tackle", "power": 40, "type": "normal", "category": "physical", "accuracy": 100},
            {"name": "Rest", "power": 5, "type": "normal", "category": "heal", "accuracy": 100},
        ],
    )

    return [chimchar, bidoof]


if __name__ == "__main__":
    rogue_run_cli(build_demo_team())

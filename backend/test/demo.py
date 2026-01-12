# backend/test/demo.py
from backend.models.pokemon import Pokemon
from backend.cli.rogue_cli import rogue_run_cli


def build_demo_team():
    chimchar = Pokemon(
        pokedex_id=390,
        name="Chimchar",
        level=16,
        types=["fire"],
        base_stats={"hp": 44, "atk": 58, "def": 44, "spd": 61},
        moves=[
            {"name": "Scratch", "power": 40, "type": "normal", "category": "damage"},
            {"name": "Ember", "power": 40, "type": "fire", "category": "damage"},
        ],
    )

    bidoof = Pokemon(
        pokedex_id=399,
        name="Bidoof",
        level=5,
        types=["normal"],
        base_stats={"hp": 59, "atk": 45, "def": 40, "spd": 31},
        moves=[
            {"name": "Tackle", "power": 40, "type": "normal", "category": "damage"},
            {"name": "Rest", "power": 5, "type": "normal", "category": "heal"},
        ],
    )

    return [chimchar, bidoof]


if __name__ == "__main__":
    rogue_run_cli(build_demo_team())

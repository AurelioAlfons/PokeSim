# backend/data/sample_team.py

from models.pokemon import Pokemon


class SampleTeam:
    def __init__(self):
        self.id = "sample"
        self.name = "Sinnoh Starters"

        self.pokemon = [
            # -----------------------------
            # Infernape
            # -----------------------------
            Pokemon(
                pokedex_id=392,
                name="Infernape",
                level=36,
                types=["fire", "fighting"],
                base_stats={
                    "hp": 76,
                    "atk": 104,
                    "def": 71,
                    "spd": 108,
                },
                moves=[
                    {
                        "name": "Flamethrower",
                        "power": 90,
                        "type": "fire",
                        "category": "damage",
                    },
                    {
                        "name": "Close Combat",
                        "power": 120,
                        "type": "fighting",
                        "category": "damage",
                    },
                    {
                        "name": "Mach Punch",
                        "power": 40,
                        "type": "fighting",
                        "category": "damage",
                    },
                    {
                        "name": "Bulk Up",
                        "power": 10,
                        "type": "fighting",
                        "category": "heal",
                    },
                ],
            ),

            # -----------------------------
            # Torterra
            # -----------------------------
            Pokemon(
                pokedex_id=389,
                name="Torterra",
                level=36,
                types=["grass", "ground"],
                base_stats={
                    "hp": 95,
                    "atk": 109,
                    "def": 105,
                    "spd": 56,
                },
                moves=[
                    {
                        "name": "Razor Leaf",
                        "power": 55,
                        "type": "grass",
                        "category": "damage",
                    },
                    {
                        "name": "Earthquake",
                        "power": 100,
                        "type": "ground",
                        "category": "damage",
                    },
                    {
                        "name": "Crunch",
                        "power": 80,
                        "type": "dark",
                        "category": "damage",
                    },
                    {
                        "name": "Synthesis",
                        "power": 40,
                        "type": "grass",
                        "category": "heal",
                    },
                ],
            ),

            # -----------------------------
            # Empoleon
            # -----------------------------
            Pokemon(
                pokedex_id=395,
                name="Empoleon",
                level=36,
                types=["water", "steel"],
                base_stats={
                    "hp": 84,
                    "atk": 86,
                    "def": 88,
                    "spd": 60,
                },
                moves=[
                    {
                        "name": "Surf",
                        "power": 90,
                        "type": "water",
                        "category": "damage",
                    },
                    {
                        "name": "Flash Cannon",
                        "power": 80,
                        "type": "steel",
                        "category": "damage",
                    },
                    {
                        "name": "Ice Beam",
                        "power": 90,
                        "type": "ice",
                        "category": "damage",
                    },
                    {
                        "name": "Aqua Ring",
                        "power": 15,
                        "type": "water",
                        "category": "heal",
                    },
                ],
            ),
        ]


# single instance (easy import)
SAMPLE_TEAM = SampleTeam()

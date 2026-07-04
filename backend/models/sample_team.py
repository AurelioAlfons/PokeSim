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
                    "spatk": 104,
                    "spdef": 71,
                    "spd": 108,
                },
                ability="blaze",
                moves=[
                    {
                        "name": "Flamethrower",
                        "power": 90,
                        "type": "fire",
                        "category": "special",
                        "accuracy": 100,
                    },
                    {
                        "name": "Close Combat",
                        "power": 120,
                        "type": "fighting",
                        "category": "physical",
                        "accuracy": 100,
                    },
                    {
                        "name": "Mach Punch",
                        "power": 40,
                        "type": "fighting",
                        "category": "physical",
                        "accuracy": 100,
                    },
                    {
                        "name": "Bulk Up",
                        "power": 10,
                        "type": "fighting",
                        "category": "heal",
                        "accuracy": 100,
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
                    "spatk": 75,
                    "spdef": 85,
                    "spd": 56,
                },
                ability="overgrow",
                moves=[
                    {
                        "name": "Razor Leaf",
                        "power": 55,
                        "type": "grass",
                        "category": "physical",
                        "accuracy": 95,
                    },
                    {
                        "name": "Earthquake",
                        "power": 100,
                        "type": "ground",
                        "category": "physical",
                        "accuracy": 100,
                    },
                    {
                        "name": "Crunch",
                        "power": 80,
                        "type": "dark",
                        "category": "physical",
                        "accuracy": 100,
                    },
                    {
                        "name": "Synthesis",
                        "power": 40,
                        "type": "grass",
                        "category": "heal",
                        "accuracy": 100,
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
                    "spatk": 111,
                    "spdef": 101,
                    "spd": 60,
                },
                ability="torrent",
                moves=[
                    {
                        "name": "Surf",
                        "power": 90,
                        "type": "water",
                        "category": "special",
                        "accuracy": 100,
                    },
                    {
                        "name": "Flash Cannon",
                        "power": 80,
                        "type": "steel",
                        "category": "special",
                        "accuracy": 100,
                    },
                    {
                        "name": "Ice Beam",
                        "power": 90,
                        "type": "ice",
                        "category": "special",
                        "accuracy": 100,
                    },
                    {
                        "name": "Aqua Ring",
                        "power": 15,
                        "type": "water",
                        "category": "heal",
                        "accuracy": 100,
                    },
                ],
            ),
        ]


# single instance (easy import)
SAMPLE_TEAM = SampleTeam()

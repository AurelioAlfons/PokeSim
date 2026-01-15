# backend/data/sample_team.py

from backend.models.pokemon import Pokemon


class SampleTeam:
    def __init__(self):
        self.id = "sample"
        self.name = "Sample Team"

        self.pokemon = [
            Pokemon(
                pokedex_id=390,
                name="Chimchar",
                level=5,
                types=["fire"],
                base_stats={
                    "hp": 44,
                    "atk": 58,
                    "def": 44,
                    "spd": 61,
                },
                moves=[
                    {
                        "name": "Scratch",
                        "power": 40,
                        "type": "normal",
                        "category": "damage",
                    },
                    {
                        "name": "Ember",
                        "power": 40,
                        "type": "fire",
                        "category": "damage",
                    },
                ],
            ),
            Pokemon(
                pokedex_id=399,
                name="Bidoof",
                level=5,
                types=["normal"],
                base_stats={
                    "hp": 59,
                    "atk": 45,
                    "def": 40,
                    "spd": 31,
                },
                moves=[
                    {
                        "name": "Tackle",
                        "power": 40,
                        "type": "normal",
                        "category": "damage",
                    }
                ],
            ),
            Pokemon(
                pokedex_id=396,
                name="Starly",
                level=5,
                types=["normal", "flying"],
                base_stats={
                    "hp": 40,
                    "atk": 55,
                    "def": 30,
                    "spd": 60,
                },
                moves=[
                    {
                        "name": "Quick Attack",
                        "power": 40,
                        "type": "normal",
                        "category": "damage",
                    }
                ],
            ),
        ]


# single instance (easy import)
SAMPLE_TEAM = SampleTeam()

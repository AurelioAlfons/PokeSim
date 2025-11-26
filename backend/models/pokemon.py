## Define pokemon model and stats

# backend/models/pokemon.py

# Main Pokemon class
class Pokemon:
    def __init__(
        self,
        pokedex_id: int,
        name: str,
        level: int,
        types: list,                   # ["fire", "fighting"]
        base_stats: dict,              # {"hp": 76, "atk": 104, "def": 71, "spd": 108}
        moves: list,                   # list of move dicts
        ability: str = None            # optional (future feature)
    ):
        self.id = pokedex_id
        self.name = name
        self.level = level
        self.types = [t.lower() for t in types]  # clean formatting
        self.ability = ability

        # Base stats dict must contain hp/atk/def/spd
        base_hp     = base_stats["hp"]
        base_atk    = base_stats["atk"]
        base_def    = base_stats["def"]
        base_speed  = base_stats["spd"]

        # ----- Simple level scaling -----
        self.max_hp = base_hp + (level * 3)
        self.hp = self.max_hp

        self.attack  = base_atk    + (level * 1)
        self.defense = base_def    + (level * 1)
        self.speed   = base_speed  + (level * 1)
        # ---------------------------------

        # moves: list of {"name": "...", "power": 40, "type": "fire", "category": "damage"}
        self.moves = moves

        # sprite path — this is what React will use
        self.sprite = f"/assets/SVG/{self.id}.svg"

    def is_fainted(self) -> bool:
        return self.hp <= 0

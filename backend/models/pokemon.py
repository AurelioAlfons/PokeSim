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
        base_hp = base_stats["hp"]
        base_atk = base_stats["atk"]
        base_def = base_stats["def"]
        base_speed = base_stats["spd"]

        # ----- Simple level scaling -----
        self.max_hp = base_hp + (level * 3)
        self.hp = self.max_hp

        self.attack = base_atk + (level * 1)
        self.defense = base_def + (level * 1)
        self.speed = base_speed + (level * 1)
        # ---------------------------------

        # moves: list of {"name": "...", "power": 40, "type": "fire", "category": "damage"}
        self.moves = moves

        # sprite path — this is what React will use
        self.sprite = f"/assets/SVG/{self.id}.svg"

        # -------- EXP & LEVELING --------
        self.exp = 0
        self.exp_to_next_level = self._calc_exp_to_next_level()

    def is_fainted(self) -> bool:
        return self.hp <= 0

    # -----------------------------
    # EXP + LEVELING HELPERS
    # -----------------------------
    def _calc_exp_to_next_level(self) -> int:
        """
        Simple EXP curve (easy for testing).
        You can replace this later with a Gen-accurate formula.
        """
        return self.level * 20

    def gain_exp(self, amount: int) -> bool:
        """
        Adds EXP to this Pokemon.
        Returns True if at least one level-up happened.
        """
        if amount <= 0:
            return False

        self.exp += amount
        leveled_up = False

        # In case a big EXP reward causes multiple level ups
        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level_up()
            leveled_up = True

        return leveled_up

    def level_up(self):
        """
        Increases level and boosts stats.
        """
        self.level += 1
        self.exp_to_next_level = self._calc_exp_to_next_level()

        # Simple stat scaling per level
        self.max_hp += 3
        self.attack += 1
        self.defense += 1
        self.speed += 1

        # Heal on level up (simple + feels good)
        self.hp = self.max_hp

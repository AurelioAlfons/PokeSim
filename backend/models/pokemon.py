## Define pokemon model and stats

# backend/models/pokemon.py

# Main Pokemon class
class Pokemon:
    def __init__(self, name, level, pokemon_type,
                 base_hp, base_attack, base_defense, base_speed,
                 moves):
        self.name = name
        self.level = level
        self.pokemon_type = pokemon_type.lower()

        # ----- Simple level-based scaling -----
        self.max_hp = base_hp + level * 3
        self.hp = self.max_hp
        self.attack = base_attack + level * 1
        self.defense = base_defense + level * 1
        self.speed = base_speed + level * 1
        # --------------------------------------

        # moves: list of (name, power, type, category)
        self.moves = moves

    def is_fainted(self) -> bool:
        return self.hp <= 0

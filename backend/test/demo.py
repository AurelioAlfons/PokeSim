import random
import os

## Colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

## Fixed inner width for all boxes
BOX_WIDTH = 34

## Clear terminal upon running
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

## Define Pokemon attributes
class Pokemon:
    def __init__(self, name, level, pokemon_type, base_hp, base_attack, base_defense, base_speed, moves):
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

        # moves: (name, power, type, category)
        self.moves = moves

    def is_fainted(self):
        return self.hp <= 0

## Damage calculation function
def damage_calc(attacker, defender, power, move_type):
    lvl = (2 * attacker.level) / 5 + 2
    base = (lvl * attacker.attack * power) / defender.defense
    damage = int(base / 50) + 2

    ## STAB (1.5x), If move type matches attacker's type
    if attacker.pokemon_type == move_type.lower():
        damage = int(damage * 1.5)

    return damage

## Execute a turn
def take_turn(user, target, move):
    name, power, move_type, category = move

    # Healing move, If category is "heal"
    if category == "heal":
        old_hp = user.hp
        user.hp = min(user.hp + power, user.max_hp)
        healed = user.hp - old_hp
        print(f"{user.name} used {name}! → healed {healed} HP")
        print(f"{user.name} HP: {user.hp}/{user.max_hp}\n")
        return

    # Damage move
    dmg = damage_calc(user, target, power, move_type)
    target.hp = max(target.hp - dmg, 0)

    stab_text = " (STAB!)" if user.pokemon_type == move_type.lower() else ""

    print(f"{user.name} used {name}!{stab_text} → {dmg} dmg")
    print(f"{target.name} HP: {target.hp}/{target.max_hp}\n")

## Player move selection
def choose_move(pokemon):
    print(f"{RED}┌{'─' * BOX_WIDTH}┐{RESET}")
    title = f"Choose a move for {pokemon.name}"
    print(f"{RED}│{title.center(BOX_WIDTH)}│{RESET}")
    print(f"{RED}├{'─' * BOX_WIDTH}┤{RESET}")

    for i, m in enumerate(pokemon.moves, start=1):
        name, power, move_type, category = m

        if category == "damage":
            row = f"{i}. {name:<10} | {move_type:<7} | {power:<3}"
        else:
            row = f"{i}. {name:<10} | HEAL    | {power:<3}"

        print(f"{RED}│{row.ljust(BOX_WIDTH)}│{RESET}")

    print(f"{RED}└{'─' * BOX_WIDTH}┘{RESET}")

    choice = input("Enter move number (or anything else to quit): ")

    # If player enters non-number → end battle
    if not choice.isdigit():
        return "END"

    # Convert to int and validate range
    choice = int(choice)
    if 1 <= choice <= len(pokemon.moves):
        return pokemon.moves[choice - 1]

    # If number out of range → end battle
    return "END"


def enemy_choose_move(enemy):
    return random.choice(enemy.moves)


def battle(player, enemy):
    print("=== Battle Start ===\n")

    turn = 1

    while True:
        print(f"{BOLD}--- Turn {turn} ---{RESET}\n")

        # HP BOX (GREEN)
        print(f"{GREEN}┌{'─' * BOX_WIDTH}┐{RESET}")

        line1 = f"{player.name:<10} HP: {player.hp:>3}/{player.max_hp:<3}"
        line2 = f"{enemy.name:<10} HP: {enemy.hp:>3}/{enemy.max_hp:<3}"

        print(f"{GREEN}│{line1.ljust(BOX_WIDTH)}│{RESET}")
        print(f"{GREEN}│{line2.ljust(BOX_WIDTH)}│{RESET}")
        print(f"{GREEN}└{'─' * BOX_WIDTH}┘{RESET}\n")

        # PLAYER TURN
        move = choose_move(player)

        if move == "END":
            print("You ended the battle early.")
            break

        take_turn(player, enemy, move)

        if enemy.is_fainted():
            print(f"{enemy.name} fainted! {player.name} wins!")
            break

        # ENEMY TURN
        enemy_move = enemy_choose_move(enemy)
        take_turn(enemy, player, enemy_move)

        if player.is_fainted():
            print(f"{player.name} fainted! {enemy.name} wins!")
            break

        turn += 1


# -----------------------------------------
# Example Pokémon
# -----------------------------------------

chimchar = Pokemon(
    name="Chimchar",
    level=7,
    pokemon_type="fire",
    base_hp=15,
    base_attack=9,
    base_defense=6,
    base_speed=10,
    moves=[
        ("Scratch", 40, "normal", "damage"),
        ("Ember", 40, "fire", "damage"),
    ],
)

bidoof = Pokemon(
    name="Bidoof",
    level=5,
    pokemon_type="normal",
    base_hp=18,
    base_attack=8,
    base_defense=8,
    base_speed=5,
    moves=[
        ("Tackle", 40, "normal", "damage"),
        ("Rest", 5, "normal", "heal"),
    ],
)


if __name__ == "__main__": 
    clear_screen()
    battle(chimchar, bidoof)

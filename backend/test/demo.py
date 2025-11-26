# backend/test/demo.py

import os

from backend.models.pokemon import Pokemon
from backend.services.battle_service import take_turn, enemy_choose_move

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Fixed inner width for all boxes
BOX_WIDTH = 34


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def format_action(result: dict) -> str:
    """Turn the engine result into a printable string for CLI."""
    if result["action"] == "heal":
        if result["healed"] == 0:
            return (
                f"{result['user']} used {result['move_name']}! → HP is already full.\n"
                f"{result['user']} HP: {result['user_hp']}/{result['user_max_hp']}\n"
            )
        return (
            f"{result['user']} used {result['move_name']}! → healed {result['healed']} HP\n"
            f"{result['user']} HP: {result['user_hp']}/{result['user_max_hp']}\n"
        )

    # damage
    stab_text = " (STAB!)" if result.get("stab") else ""
    return (
        f"{result['user']} used {result['move_name']}!{stab_text} → {result['damage']} dmg\n"
        f"{result['target']} HP: {result['target_hp']}/{result['target_max_hp']}\n"
    )


def choose_move(pokemon: Pokemon):
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

    if not choice.isdigit():
        return "END"

    choice = int(choice)
    if 1 <= choice <= len(pokemon.moves):
        return pokemon.moves[choice - 1]

    return "END"


def battle(player: Pokemon, enemy: Pokemon):
    print("=== Battle Start ===\n")
    turn = 1

    while True:
        print(f"{BOLD}--- Turn {turn} ---{RESET}\n")

        # HP BOX (GREEN)
        print(f"{GREEN}┌{'─' * BOX_WIDTH}┐{RESET}")
        line1 = f"Lv {player.level} | {player.name:<10} HP: {player.hp:>3}/{player.max_hp:<3}"
        line2 = f"Lv {enemy.level}  | {enemy.name:<10} HP: {enemy.hp:>3}/{enemy.max_hp:<3}"
        print(f"{GREEN}│{line1.ljust(BOX_WIDTH)}│{RESET}")
        print(f"{GREEN}│{line2.ljust(BOX_WIDTH)}│{RESET}")
        print(f"{GREEN}└{'─' * BOX_WIDTH}┘{RESET}\n")

        # PLAYER TURN
        move = choose_move(player)
        if move == "END":
            print("You ended the battle early.")
            break

        result = take_turn(player, enemy, move)
        print(format_action(result))

        if enemy.is_fainted():
            print(f"{enemy.name} fainted! {player.name} wins!")
            break

        # ENEMY TURN
        enemy_move = enemy_choose_move(enemy)
        enemy_result = take_turn(enemy, player, enemy_move)
        print(format_action(enemy_result))

        if player.is_fainted():
            print(f"{player.name} fainted! {enemy.name} wins!")
            break

        turn += 1


# ---- Dummy Pokémon for the demo ----

chimchar = Pokemon(
    name="Chimchar",
    level=16,
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

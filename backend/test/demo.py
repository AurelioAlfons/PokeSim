# backend/test/demo.py

import os
import random

from backend.models.pokemon import Pokemon
from backend.services.battle_service import take_turn, enemy_choose_move

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[38;2;80;150;255m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Fixed inner width for all boxes
BOX_WIDTH = 40


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def blue_box(text: str):
    """Wrap any text inside a blue box."""
    lines = text.strip().split("\n")
    print(f"{BLUE}┌{'─' * BOX_WIDTH}┐{RESET}")
    for line in lines:
        print(f"{BLUE}│{line.ljust(BOX_WIDTH)}│{RESET}")
    print(f"{BLUE}└{'─' * BOX_WIDTH}┘{RESET}")


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
        name = m["name"]
        power = m["power"]
        move_type = m["type"]
        category = m["category"]

        if category == "damage":
            row = f"{i}. {name:<10} | {move_type:<7} | {power:<3}"
        else:
            row = f"{i}. {name:<10} | HEAL    | {power:<3}"

        print(f"{RED}│{row.ljust(BOX_WIDTH)}│{RESET}")

    print(f"{RED}└{'─' * BOX_WIDTH}┘{RESET}")

    choice = input("\nEnter move number (or anything else to quit run): ")

    if not choice.isdigit():
        return "END"

    choice = int(choice)
    if 1 <= choice <= len(pokemon.moves):
        return pokemon.moves[choice - 1]

    return "END"


# ----------------------------
# Rogue helpers (dummy)
# ----------------------------
def next_alive(team):
    for p in team:
        if p.hp > 0:
            return p
    return None


def team_wiped(team):
    return all(p.hp <= 0 for p in team)


def lowest_alive_level(team):
    alive = [p.level for p in team if p.hp > 0]
    return min(alive) if alive else 1


def make_wild(level: int) -> Pokemon:
    # dummy wild pool
    pool = [
        ("Bidoof", 399, ["normal"], {"hp": 59, "atk": 45, "def": 40, "spd": 31},
         [{"name": "Tackle", "power": 40, "type": "normal", "category": "damage"},
          {"name": "Rest", "power": 5, "type": "normal", "category": "heal"}]),
        ("Starly", 396, ["normal", "flying"], {"hp": 40, "atk": 55, "def": 30, "spd": 60},
         [{"name": "Tackle", "power": 40, "type": "normal", "category": "damage"},
          {"name": "QuickAtk", "power": 40, "type": "normal", "category": "damage"}]),
        ("Shinx", 403, ["electric"], {"hp": 45, "atk": 65, "def": 34, "spd": 45},
         [{"name": "Tackle", "power": 40, "type": "normal", "category": "damage"},
          {"name": "Spark", "power": 40, "type": "electric", "category": "damage"}]),
    ]

    name, dex, types, stats, moves = random.choice(pool)
    return Pokemon(
        pokedex_id=dex,
        name=name,
        level=level,
        types=types,
        base_stats=stats,
        moves=moves,
    )


def green_hp_box(player: Pokemon, enemy: Pokemon):
    print(f"{GREEN}┌{'─' * BOX_WIDTH}┐{RESET}")
    line1 = f"Lv {player.level} | {player.name:<10} HP: {player.hp:>3}/{player.max_hp:<3}"
    line2 = f"Lv {enemy.level}  | {enemy.name:<10} HP: {enemy.hp:>3}/{enemy.max_hp:<3}"
    print(f"{GREEN}│{line1.ljust(BOX_WIDTH)}│{RESET}")
    print(f"{GREEN}│{line2.ljust(BOX_WIDTH)}│{RESET}")
    print(f"{GREEN}└{'─' * BOX_WIDTH}┘{RESET}")


# ----------------------------
# 1v1 battle that returns outcome
# ----------------------------
def battle_once(player: Pokemon, enemy: Pokemon):
    """
    Returns:
      "wild_fainted" or "player_fainted" or "END"
    """
    while True:
        green_hp_box(player, enemy)

        move = choose_move(player)
        if move == "END":
            return "END"

        result = take_turn(player, enemy, move)
        blue_box(format_action(result))

        if enemy.is_fainted():
            print(f"{enemy.name} fainted!")
            return "wild_fainted"

        enemy_move = enemy_choose_move(enemy)
        enemy_result = take_turn(enemy, player, enemy_move)
        blue_box(format_action(enemy_result))

        if player.is_fainted():
            print(f"{player.name} fainted!")
            return "player_fainted"


# ----------------------------
# Rogue loop (endless)
# ----------------------------
def rogue_run(team):
    clear_screen()
    print("=== ROGUE MODE START ===")

    wave = 1
    wins = 0

    while True:
        if team_wiped(team):
            print(f"\n💀 RUN OVER. Wins: {wins}")
            break

        active = next_alive(team)

        # wild level rule: lowest team level - 2, plus a ramp
        base_level = max(1, lowest_alive_level(team) - 2)
        ramp = wave // 3
        wild_level = base_level + ramp

        wild = make_wild(wild_level)

        print(f"\n{BOLD}=== WAVE {wave} ==={RESET}")
        print(f"Wild {wild.name} (Lv {wild.level}) appeared!\n")

        outcome = battle_once(active, wild)

        if outcome == "END":
            print("\nYou ended the run early.")
            break

        if outcome == "wild_fainted":
            wins += 1
            wave += 1
            print(f"{GREEN}✅ Win! Total wins: {wins}{RESET}")

            # tiny heal between fights (15%)
            for p in team:
                if p.hp > 0:
                    heal = max(1, int(p.max_hp * 0.15))
                    p.hp = min(p.max_hp, p.hp + heal)

        elif outcome == "player_fainted":
            # don't change wave; next alive continues the run
            if team_wiped(team):
                print(f"\n💀 RUN OVER. Wins: {wins}")
                break
            else:
                nxt = next_alive(team)
                print(f"{BOLD}➡️  Go! {nxt.name}!{RESET}")
                # continue loop (same wave will spawn a NEW wild next loop)
                # If you want SAME wild to remain, we can change that later.


# ---- Dummy Pokémon for the demo team ----
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

if __name__ == "__main__":
    # team can be 1-6 mons
    team = [chimchar, bidoof]
    rogue_run(team)

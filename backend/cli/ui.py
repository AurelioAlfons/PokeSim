# backend/cli/ui.py
from __future__ import annotations

import os
from typing import Optional

from backend.models.pokemon import Pokemon

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[38;2;80;150;255m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Fixed inner width for all boxes
BOX_WIDTH = 60


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def blue_box(text: str):
    """Wrap any text inside a blue box."""
    lines = text.strip().split("\n")
    print(f"{BLUE}┌{'─' * BOX_WIDTH}┐{RESET}")
    for line in lines:
        print(f"{BLUE}│{line.ljust(BOX_WIDTH)}│{RESET}")
    print(f"{BLUE}└{'─' * BOX_WIDTH}┘{RESET}")


def red_box(title: str, rows: list[str]):
    """Simple red menu box."""
    print(f"{RED}┌{'─' * BOX_WIDTH}┐{RESET}")
    print(f"{RED}│{title.center(BOX_WIDTH)}│{RESET}")
    print(f"{RED}├{'─' * BOX_WIDTH}┤{RESET}")
    for r in rows:
        print(f"{RED}│{r.ljust(BOX_WIDTH)}│{RESET}")
    print(f"{RED}└{'─' * BOX_WIDTH}┘{RESET}")


def green_hp_box(active: Pokemon, enemy: Pokemon):
    print(f"{GREEN}┌{'─' * BOX_WIDTH}┐{RESET}")
    line1 = (
        f"Lv {active.level} | {active.name:<10} "
        f"HP: {active.hp:>3}/{active.max_hp:<3} "
        f"| EXP: {active.exp}/{active.exp_to_next_level}"
    )
    line2 = f"Lv {enemy.level}  | {enemy.name:<10} HP: {enemy.hp:>3}/{enemy.max_hp:<3}"
    print(f"{GREEN}│{line1.ljust(BOX_WIDTH)}│{RESET}")
    print(f"{GREEN}│{line2.ljust(BOX_WIDTH)}│{RESET}")
    print(f"{GREEN}└{'─' * BOX_WIDTH}┘{RESET}")


def format_action(result: dict) -> str:
    """Turn engine result into a printable string for CLI."""
    action = result["action"]

    if action == "heal":
        if result["healed"] == 0:
            return (
                f"{result['user']} used {result['move_name']}! → HP is already full.\n"
                f"{result['user']} HP: {result['user_hp']}/{result['user_max_hp']}\n"
            )
        return (
            f"{result['user']} used {result['move_name']}! → healed {result['healed']} HP\n"
            f"{result['user']} HP: {result['user_hp']}/{result['user_max_hp']}\n"
        )

    if action == "status":
        return f"{result['user']} used {result['move_name']}, but nothing happened.\n"

    if action == "miss":
        return f"{result['user']} used {result['move_name']}! → it missed!\n"

    tags = []
    if result.get("stab"):
        tags.append("STAB!")
    if result.get("crit"):
        tags.append("Critical hit!")
    eff = result.get("effectiveness", 1)
    if eff > 1:
        tags.append("Super effective!")
    elif 0 < eff < 1:
        tags.append("Not very effective...")
    tag_text = f" ({' '.join(tags)})" if tags else ""

    return (
        f"{result['user']} used {result['move_name']}!{tag_text} → {result['damage']} dmg\n"
        f"{result['target']} HP: {result['target_hp']}/{result['target_max_hp']}\n"
    )


def choose_action_menu() -> str:
    rows = ["1. Fight", "2. Pokemon", "3. Bag", "4. Run"]
    red_box("What will you do?", rows)
    return input("\nChoose 1-4: ").strip()


def choose_move(pokemon: Pokemon) -> Optional[dict]:
    rows: list[str] = []
    for i, m in enumerate(pokemon.moves, start=1):
        name = m["name"]
        power = m["power"]
        move_type = m["type"]
        category = m["category"]

        if category == "heal":
            rows.append(f"{i}. {name:<10} | HEAL    | {power:<3}")
        else:
            rows.append(f"{i}. {name:<10} | {move_type:<7} | {power:<3}")

    red_box(f"Choose a move for {pokemon.name}", rows)
    choice = input("\nEnter move number (or anything else to go back): ")

    if not choice.isdigit():
        return None

    idx = int(choice)
    if 1 <= idx <= len(pokemon.moves):
        return pokemon.moves[idx - 1]

    return None


def choose_team_switch(team: list[Pokemon], current_active: Pokemon) -> Optional[Pokemon]:
    """
    Returns a new Pokemon to switch to, or None if cancelled/invalid.
    """
    rows: list[str] = []
    candidates: list[Pokemon] = []

    for idx, p in enumerate(team, start=1):
        status = "FNT" if p.hp <= 0 else "OK "
        tag = "(ACTIVE)" if p is current_active else ""
        row = f"{idx}. {p.name:<10} Lv {p.level:<2} HP {p.hp:>3}/{p.max_hp:<3} [{status}] {tag}"
        rows.append(row)
        candidates.append(p)

    red_box("Choose a Pokemon to switch", rows)
    choice = input("\nEnter number (or anything else to cancel): ")

    if not choice.isdigit():
        return None

    pick = int(choice)
    if not (1 <= pick <= len(candidates)):
        return None

    picked = candidates[pick - 1]

    if picked.hp <= 0:
        blue_box("Can't switch to a fainted Pokemon.")
        return None

    if picked is current_active:
        blue_box("You're already using that Pokemon.")
        return None

    return picked


def use_bag(active: Pokemon, bag: dict) -> bool:
    """
    Returns True if an item was used (consumes your turn).
    """
    potions = bag.get("potion", 0)
    rows = [f"1. Potion (+20 HP)  x{potions}", "2. Back"]
    red_box("Bag", rows)
    choice = input("\nChoose: ").strip()

    if choice != "1":
        return False

    if potions <= 0:
        blue_box("No Potions left!")
        return False

    if active.hp <= 0:
        blue_box("Can't use items on a fainted Pokemon.")
        return False

    if active.hp >= active.max_hp:
        blue_box("HP is already full.")
        return False

    heal = min(20, active.max_hp - active.hp)
    active.hp += heal
    bag["potion"] = potions - 1
    blue_box(f"Used Potion on {active.name}! +{heal} HP")
    return True

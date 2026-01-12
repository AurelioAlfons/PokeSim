# backend/cli/rogue_cli.py
from __future__ import annotations

from backend.models.pokemon import Pokemon
from backend.services.battle_service import take_turn, enemy_choose_move
from backend.services.rogue_service import (
    next_alive,
    team_wiped,
    compute_wave_info,
    between_fight_heal,
)
from backend.services.wild_factory import make_wild
from backend.services.exp_service import award_exp

from backend.cli.ui import (
    BOLD,
    GREEN,
    RESET,
    clear_screen,
    blue_box,
    green_hp_box,
    choose_action_menu,
    choose_move,
    choose_team_switch,
    use_bag,
    format_action,
)


def _print_exp_rows(rows):
    print(f"\n{BOLD}✨ EXP GAINED:{RESET}")
    for r in rows:
        if r.leveled_up:
            print(f"  - {r.name} +{r.gained} EXP → Lv {r.before_level} → Lv {r.after_level} 🎉")
        else:
            print(f"  - {r.name} +{r.gained} EXP")


def battle_vs_wild_cli(team: list[Pokemon], wild: Pokemon, bag: dict) -> str:
    """
    Returns:
      "wild_fainted" or "team_wiped" or "run_away"
    """
    active = next_alive(team)
    if not active:
        return "team_wiped"

    print(f"{BOLD}➡️  Go! {active.name}!{RESET}")

    while True:
        if team_wiped(team):
            return "team_wiped"

        if wild.is_fainted():
            return "wild_fainted"

        # If active fainted, force switch (no enemy free hit here)
        if active.hp <= 0:
            blue_box(f"{active.name} fainted! Choose another Pokemon.")
            forced = None
            while forced is None:
                forced = choose_team_switch(team, current_active=active)
            active = forced
            blue_box(f"Go! {active.name}!")
            continue

        green_hp_box(active, wild)

        choice = choose_action_menu()

        # 1) FIGHT
        if choice == "1":
            move = choose_move(active)
            if move is None:
                continue

            result = take_turn(active, wild, move)
            blue_box(format_action(result))

            if wild.is_fainted():
                blue_box(f"{wild.name} fainted!")
                return "wild_fainted"

            # enemy attacks after your move
            enemy_move = enemy_choose_move(wild)
            enemy_result = take_turn(wild, active, enemy_move)
            blue_box(format_action(enemy_result))
            continue

        # 2) POKEMON (SWITCH)
        if choice == "2":
            picked = choose_team_switch(team, current_active=active)
            if picked is None:
                continue

            active = picked
            blue_box(f"Switched to {active.name}!")

            # switching uses your turn → enemy attacks
            enemy_move = enemy_choose_move(wild)
            enemy_result = take_turn(wild, active, enemy_move)
            blue_box(format_action(enemy_result))
            continue

        # 3) BAG
        if choice == "3":
            used = use_bag(active, bag)
            if not used:
                continue

            # using item uses your turn → enemy attacks
            enemy_move = enemy_choose_move(wild)
            enemy_result = take_turn(wild, active, enemy_move)
            blue_box(format_action(enemy_result))
            continue

        # 4) RUN
        if choice == "4":
            blue_box("You ran away!")
            return "run_away"

        blue_box("Invalid choice. Pick 1-4.")


def rogue_run_cli(team: list[Pokemon]):
    clear_screen()
    print("=== ROGUE MODE START ===")

    wave = 1
    wins = 0

    # simple bag for CLI demo
    bag = {"potion": 3}

    while True:
        if team_wiped(team):
            print(f"\n💀 RUN OVER. Wins: {wins}")
            break

        wave_info = compute_wave_info(team, wave)
        wild = make_wild(wave_info.wild_level)

        print(f"\n{BOLD}=== WAVE {wave} ==={RESET}")
        print(f"Wild {wild.name} (Lv {wild.level}) appeared!\n")

        outcome = battle_vs_wild_cli(team, wild, bag)

        if outcome == "run_away":
            print("\nYou ended the run early.")
            break

        if outcome == "team_wiped":
            print(f"\n💀 RUN OVER. Wins: {wins}")
            break

        if outcome == "wild_fainted":
            wins += 1
            wave += 1
            print(f"{GREEN}✅ Win! Total wins: {wins}{RESET}")

            # EXP (active bonus = first alive for now)
            active_now = next_alive(team)
            if active_now:
                exp_rows = award_exp(team, active_now, wild)
                _print_exp_rows(exp_rows)

            # between-fight heal
            between_fight_heal(team, percent=0.15)

"""
CLI-only battle loop (not used by API/UI).

Kept separate so the API battle logic stays single-source in battle_service.py.
"""

import random
from backend.models.pokemon import Pokemon
from backend.services.battle_service import take_turn, enemy_choose_move


def run_battle(player: Pokemon, enemy: Pokemon) -> str:
    """
    Runs ONE full fight (CLI-ish). Not used by UI.
    Returns: "wild_fainted" | "player_fainted"
    """
    while player.hp > 0 and enemy.hp > 0:
        player_move = random.choice(player.moves)
        enemy_move = enemy_choose_move(enemy)

        player_first = player.speed >= enemy.speed

        if player_first:
            take_turn(player, enemy, player_move)
            if enemy.hp <= 0:
                return "wild_fainted"

            take_turn(enemy, player, enemy_move)
            if player.hp <= 0:
                return "player_fainted"
        else:
            take_turn(enemy, player, enemy_move)
            if player.hp <= 0:
                return "player_fainted"

            take_turn(player, enemy, player_move)
            if enemy.hp <= 0:
                return "wild_fainted"

    return "player_fainted" if player.hp <= 0 else "wild_fainted"

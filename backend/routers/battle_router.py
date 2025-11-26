# backend/routers/battle_router.py

# This file is the BATTLE API.
# React will send requests here when the player:
#   - starts a battle
#   - taps a move button
#
# This file DOES NOT do the damage math itself.
# It simply calls your actual battle engine:
#   - take_turn()
#   - enemy_choose_move()
#   - Pokemon class
#
# Think of this file as the "middle man":
#   React  <--->  battle_router  <--->  battle_service + Pokemon objects
#
# Whatever happens in the battle (HP loss, moves used, winner),
# this file returns the results back to React in JSON format.


from fastapi import APIRouter
from pydantic import BaseModel

# Import your actual battle logic functions + Pokemon class
from backend.services.battle_service import take_turn, enemy_choose_move
from backend.models.pokemon import Pokemon

router = APIRouter()

# -----------------------------
# TEMPORARY BATTLE STATE
# -----------------------------
# We store the current player/enemy Pokemon here for testing.
# Later this will be replaced with a proper system (sessions or database).
current_battle: dict | None = None


def create_default_pokemons():
    """
    Creates two Pokemon for testing.
    Called every time a NEW battle starts.
    """
    player = Pokemon(
        name="Chimchar",
        level=10,
        pokemon_type="fire",
        base_hp=39,
        base_attack=52,
        base_defense=43,
        base_speed=65,
        moves=[
            ("Scratch", 40, "normal", "damage"),
            ("Ember", 40, "fire", "damage"),
        ],
    )

    enemy = Pokemon(
        name="Bidoof",
        level=8,
        pokemon_type="normal",
        base_hp=59,
        base_attack=45,
        base_defense=40,
        base_speed=31,
        moves=[
            ("Tackle", 40, "normal", "damage"),
            ("Rest", 0, "normal", "heal"),
        ],
    )

    return player, enemy


def pokemon_public_view(p: Pokemon) -> dict:
    """
    Converts a Pokemon object into a JSON-friendly dictionary
    that React can read easily.
    """
    return {
        "name": p.name,
        "level": p.level,
        "type": p.pokemon_type,
        "hp": p.hp,
        "max_hp": p.max_hp,
        "moves": [
            {
                "index": i,
                "name": m[0],
                "power": m[1],
                "type": m[2],
                "category": m[3],
            }
            for i, m in enumerate(p.moves)
        ],
    }


# This is the data shape React must send when using a move
class TurnRequest(BaseModel):
    move_index: int  # which move button the user clicked


@router.get("/ping")
def ping():
    """
    Quick test to check if the battle API is alive.
    """
    return {"status": "ok", "message": "Battle API is working"}


@router.post("/start")
def start_battle():
    """
    Starts a NEW battle.
    React should call this when entering the battle screen.
    """
    global current_battle
    player, enemy = create_default_pokemons()

    # Save them into the temporary state
    current_battle = {"player": player, "enemy": enemy}

    return {
        "message": "New battle started",
        "player": pokemon_public_view(player),
        "enemy": pokemon_public_view(enemy),
    }


@router.post("/turn")
def do_turn(req: TurnRequest):
    """
    Runs ONE TURN of the battle.
    React calls this when the user selects a move.
    """
    global current_battle

    # If player didn't start a battle yet, auto-create one
    if current_battle is None:
        player, enemy = create_default_pokemons()
        current_battle = {"player": player, "enemy": enemy}
    else:
        player = current_battle["player"]
        enemy = current_battle["enemy"]

    # ------------------------
    # PLAYER'S TURN
    # ------------------------
    result_player = take_turn(
        attacker=player,
        defender=enemy,
        move_index=req.move_index,
    )

    # If enemy fainted first, battle ends instantly
    if enemy.hp <= 0:
        return {
            "player_action": result_player,
            "enemy_action": None,
            "player": pokemon_public_view(player),
            "enemy": pokemon_public_view(enemy),
            "battle_over": True,
            "winner": "player",
        }

    # ------------------------
    # ENEMY'S TURN
    # ------------------------
    enemy_move_index = enemy_choose_move(enemy)

    result_enemy = take_turn(
        attacker=enemy,
        defender=player,
        move_index=enemy_move_index,
    )

    # ------------------------
    # CHECK WINNER
    # ------------------------
    if player.hp <= 0 and enemy.hp <= 0:
        winner = "draw"
    elif enemy.hp <= 0:
        winner = "player"
    elif player.hp <= 0:
        winner = "enemy"
    else:
        winner = None

    battle_over = winner is not None

    return {
        "player_action": result_player,
        "enemy_action": result_enemy,
        "player": pokemon_public_view(player),
        "enemy": pokemon_public_view(enemy),
        "battle_over": battle_over,
        "winner": winner,
    }

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
# React  <--->  battle_router  <--->  battle_service + Pokemon objects

from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.battle_service import take_turn, enemy_choose_move
from backend.models.pokemon import Pokemon

router = APIRouter()

# -----------------------------
# TEMPORARY BATTLE STATE
# -----------------------------
# Later this will be replaced by sessions / DB.
current_battle: dict | None = None


def create_default_pokemons():
    """
    Creates two Pokemon for testing.
    Called every time a NEW battle starts.
    """

    # --- Player: Chimchar (id 390) ---
    player = Pokemon(
        pokedex_id=390,
        name="Chimchar",
        level=10,
        types=["fire"],
        base_stats={
            "hp": 44,
            "atk": 58,
            "def": 44,
            "spd": 61,
        },
        moves=[
            {"name": "Scratch", "power": 40, "type": "normal", "category": "damage"},
            {"name": "Ember", "power": 40, "type": "fire", "category": "damage"},
        ],
        ability="Blaze",
    )

    # --- Enemy: Bidoof (id 399) ---
    enemy = Pokemon(
        pokedex_id=399,
        name="Bidoof",
        level=8,
        types=["normal"],
        base_stats={
            "hp": 59,
            "atk": 45,
            "def": 40,
            "spd": 31,
        },
        moves=[
            {"name": "Tackle", "power": 40, "type": "normal", "category": "damage"},
            {"name": "Rest", "power": 0, "type": "normal", "category": "heal"},
        ],
        ability="Simple",
    )

    return player, enemy


def pokemon_public_view(p: Pokemon) -> dict:
    """
    Converts a Pokemon object into a JSON-friendly dictionary
    that React can read easily.
    """
    return {
        "id": p.id,
        "name": p.name,
        "level": p.level,
        "types": p.types,
        "hp": p.hp,
        "max_hp": p.max_hp,
        "sprite": p.sprite,  # /assets/SVG/{id}.svg
        "moves": [
            {
                "index": i,
                "name": m["name"],
                "power": m["power"],
                "type": m["type"],
                "category": m["category"],
            }
            for i, m in enumerate(p.moves)
        ],
    }


class TurnRequest(BaseModel):
    move_index: int  # which move button the user clicked


@router.get("/ping")
def ping():
    return {"status": "ok", "message": "Battle API is working"}


@router.post("/start")
def start_battle():
    """
    Starts a NEW battle.
    React should call this when entering the battle screen.
    """
    global current_battle
    player, enemy = create_default_pokemons()

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

    # Auto-create a battle if none exists
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

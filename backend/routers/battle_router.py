# backend/routers/battle_router.py
from fastapi import APIRouter

from backend.models.sample_team import SAMPLE_TEAM

router = APIRouter()


def _poke_to_dict(p):
    """
    Converts your Pokemon class into JSON-safe dict.
    (vars(p) works too, but this is safer + controlled.)
    """
    return {
        "id": p.id,
        "name": p.name,
        "level": p.level,
        "types": p.types,
        "ability": p.ability,
        "hp": p.hp,
        "max_hp": p.max_hp,
        "attack": p.attack,
        "defense": p.defense,
        "speed": p.speed,
        "moves": p.moves,
        "sprite": p.sprite,
        "exp": p.exp,
        "exp_to_next_level": p.exp_to_next_level,
    }


@router.post("/start")
def start_battle():
    """
    For now:
    - player = Chimchar (slot 0)
    - enemy  = Bidoof   (slot 1)
    """
    player = SAMPLE_TEAM.pokemon[0]  # Chimchar
    enemy = SAMPLE_TEAM.pokemon[1]   # Bidoof

    return {
        "team": {
            "id": SAMPLE_TEAM.id,
            "name": SAMPLE_TEAM.name,
            "pokemon": [_poke_to_dict(x) for x in SAMPLE_TEAM.pokemon],
        },
        "player": _poke_to_dict(player),
        "enemy": _poke_to_dict(enemy),
        "log": [
            f"A wild {enemy.name} appeared!",
            f"Go! {player.name}!",
        ],
    }

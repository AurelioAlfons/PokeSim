# backend/routers/battle_router.py
from fastapi import APIRouter
from pydantic import BaseModel

from backend.models.sample_team import SAMPLE_TEAM

router = APIRouter()


def _poke_to_dict(p):
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


# --- simple in-memory battle state (good for local dev) ---
BATTLE_STATE = {
    "active_index": 0,
    "enemy_index": 1,
    "started": False,
}


class SwitchRequest(BaseModel):
    index: int


@router.post("/start")
def start_battle():
    """
    For now:
    - team = SAMPLE_TEAM (3 pokemon)
    - active player = slot 0 (Chimchar)
    - enemy = slot 1 (Bidoof)
    """
    BATTLE_STATE["active_index"] = 0
    BATTLE_STATE["enemy_index"] = 1
    BATTLE_STATE["started"] = True

    player = SAMPLE_TEAM.pokemon[BATTLE_STATE["active_index"]]
    enemy = SAMPLE_TEAM.pokemon[BATTLE_STATE["enemy_index"]]

    return {
        "team": {
            "id": SAMPLE_TEAM.id,
            "name": SAMPLE_TEAM.name,
            "pokemon": [_poke_to_dict(x) for x in SAMPLE_TEAM.pokemon],
        },
        "active_index": BATTLE_STATE["active_index"],
        "player": _poke_to_dict(player),
        "enemy": _poke_to_dict(enemy),
        "log": [
            f"A wild {enemy.name} appeared!",
            f"Go! {player.name}!",
        ],
    }


@router.post("/switch")
def switch_pokemon(body: SwitchRequest):
    """
    Switch active player pokemon to a team slot.
    """
    if not BATTLE_STATE["started"]:
        # if someone calls switch before start
        BATTLE_STATE["active_index"] = 0
        BATTLE_STATE["enemy_index"] = 1
        BATTLE_STATE["started"] = True

    idx = body.index

    if idx < 0 or idx >= len(SAMPLE_TEAM.pokemon):
        return {
            "ok": False,
            "message": "Invalid slot index.",
            "active_index": BATTLE_STATE["active_index"],
            "player": _poke_to_dict(SAMPLE_TEAM.pokemon[BATTLE_STATE["active_index"]]),
            "enemy": _poke_to_dict(SAMPLE_TEAM.pokemon[BATTLE_STATE["enemy_index"]]),
            "team": {
                "id": SAMPLE_TEAM.id,
                "name": SAMPLE_TEAM.name,
                "pokemon": [_poke_to_dict(x) for x in SAMPLE_TEAM.pokemon],
            },
            "log": ["Can't switch: invalid slot."],
        }

    picked = SAMPLE_TEAM.pokemon[idx]
    if picked.hp <= 0:
        return {
            "ok": False,
            "message": "That Pokemon has fainted.",
            "active_index": BATTLE_STATE["active_index"],
            "player": _poke_to_dict(SAMPLE_TEAM.pokemon[BATTLE_STATE["active_index"]]),
            "enemy": _poke_to_dict(SAMPLE_TEAM.pokemon[BATTLE_STATE["enemy_index"]]),
            "team": {
                "id": SAMPLE_TEAM.id,
                "name": SAMPLE_TEAM.name,
                "pokemon": [_poke_to_dict(x) for x in SAMPLE_TEAM.pokemon],
            },
            "log": [f"{picked.name} has fainted!"],
        }

    BATTLE_STATE["active_index"] = idx

    player = SAMPLE_TEAM.pokemon[BATTLE_STATE["active_index"]]
    enemy = SAMPLE_TEAM.pokemon[BATTLE_STATE["enemy_index"]]

    return {
        "ok": True,
        "active_index": BATTLE_STATE["active_index"],
        "player": _poke_to_dict(player),
        "enemy": _poke_to_dict(enemy),
        "team": {
            "id": SAMPLE_TEAM.id,
            "name": SAMPLE_TEAM.name,
            "pokemon": [_poke_to_dict(x) for x in SAMPLE_TEAM.pokemon],
        },
        "log": [f"Go! {player.name}!"],
    }

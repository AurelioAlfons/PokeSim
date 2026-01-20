from fastapi import APIRouter
from pydantic import BaseModel

from backend.models.sample_team import SAMPLE_TEAM
from backend.services.battle_service import BattleSession, reset_team_full
from backend.services.rogue_service import (
    between_fight_heal,
    compute_wave_info,
    team_wiped,
)
from backend.services.wild_factory import make_wild

router = APIRouter()


# -----------------------------
# Helpers
# -----------------------------
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
        "exp": getattr(p, "exp", 0),
        "exp_to_next_level": getattr(p, "exp_to_next_level", 0),
    }


def _team_payload():
    return {
        "id": SAMPLE_TEAM.id,
        "name": SAMPLE_TEAM.name,
        "pokemon": [_poke_to_dict(x) for x in SAMPLE_TEAM.pokemon],
    }


# -----------------------------
# In-memory state
# -----------------------------
SESSION: BattleSession | None = None
WAVE: int = 1


class SwitchRequest(BaseModel):
    index: int


class MoveRequest(BaseModel):
    index: int


# -----------------------------
# Session bootstrap
# -----------------------------
def _ensure_session() -> BattleSession:
    global SESSION, WAVE

    if SESSION is None:
        WAVE = 1
        SESSION = BattleSession(
            team=SAMPLE_TEAM.pokemon,
            active_index=0,
            enemy=make_wild(level=5),
            log=[],
        )

        player = SESSION.player()
        enemy = SESSION.enemy

        SESSION.log = [
            f"Wave {WAVE} begins!",
            f"A wild {enemy.name} appeared!",
            f"Go! {player.name}!",
        ]

    return SESSION


def _state_response(session: BattleSession, ok=True, message=None):
    payload = {
        "ok": ok,
        "active_index": session.active_index,
        "player": _poke_to_dict(session.player()),
        "enemy": _poke_to_dict(session.enemy),
        "team": _team_payload(),
        "log": session.log,
        "wave": WAVE,
    }

    if message is not None:
        payload["message"] = message

    return payload


# -----------------------------
# Routes
# -----------------------------
@router.post("/start")
def start_battle():
    global SESSION, WAVE

    WAVE = 1
    reset_team_full(SAMPLE_TEAM.pokemon)

    SESSION = BattleSession(
        team=SAMPLE_TEAM.pokemon,
        active_index=0,
        enemy=make_wild(level=5),
        log=[],
    )

    player = SESSION.player()
    enemy = SESSION.enemy

    return {
        "team": _team_payload(),
        "active_index": SESSION.active_index,
        "player": _poke_to_dict(player),
        "enemy": _poke_to_dict(enemy),
        "log": [
            f"Wave {WAVE} begins!",
            f"A wild {enemy.name} appeared!",
            f"Go! {player.name}!",
        ],
        "wave": WAVE,
    }


@router.post("/run")
def run_away():
    """
    Run = full reset:
    - wave → 1
    - HP reset
    - EXP reset
    - new wild Pokémon
    """
    global SESSION, WAVE

    WAVE = 1
    reset_team_full(SAMPLE_TEAM.pokemon)

    SESSION = BattleSession(
        team=SAMPLE_TEAM.pokemon,
        active_index=0,
        enemy=make_wild(level=5),
        log=["You ran away!", f"Wave {WAVE} begins!"],
    )

    player = SESSION.player()
    enemy = SESSION.enemy

    SESSION.log.append(f"A wild {enemy.name} appeared!")
    SESSION.log.append(f"Go! {player.name}!")

    return _state_response(SESSION, ok=True)


@router.post("/move")
def use_move(body: MoveRequest):
    global WAVE

    session = _ensure_session()
    session.log = []

    ok, msg = session.apply_move(body.index)

    # -----------------------------
    # Rogue progression
    # -----------------------------
    if msg == "Enemy fainted.":
        # team wiped = force run
        if team_wiped(session.team):
            session.log.append("Your team has been wiped. Run over.")
            return _state_response(session, ok=True, message=msg)

        # small heal between waves
        between_fight_heal(session.team)

        # next wave
        WAVE += 1
        info = compute_wave_info(session.team, WAVE)

        session.enemy = make_wild(level=info.wild_level)
        session.log.append(f"Wave {WAVE} begins!")
        session.log.append(f"A wild {session.enemy.name} appeared!")

    return _state_response(session, ok=ok, message=msg)


@router.post("/switch")
def switch_pokemon(body: SwitchRequest):
    session = _ensure_session()
    session.log = []

    ok, msg = session.apply_switch(body.index)
    return _state_response(session, ok=ok, message=msg)

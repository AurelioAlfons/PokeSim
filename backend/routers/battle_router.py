from fastapi import APIRouter
from pydantic import BaseModel

from models.sample_team import SAMPLE_TEAM
from services.battle_service import BattleSession
from services.team_service import reset_team_full
from services.rogue_service import (
    between_fight_heal,
    compute_wave_info,
    team_wiped,
)
from services.wild_factory import make_wild

router = APIRouter()

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


def _team_payload(team):
    # DB-ready: this payload is based on the session team, not SAMPLE_TEAM
    return {
        "id": getattr(SAMPLE_TEAM, "id", "sample"),   # placeholder until DB team
        "name": getattr(SAMPLE_TEAM, "name", "Sample Team"),
        "pokemon": [_poke_to_dict(x) for x in team],
    }


def _spawn_enemy_for_wave(session: BattleSession, wave: int):
    """
    Always spawn wild using the rogue scaling rules.
    Keeps /start, /run, and wave progression consistent.
    """
    info = compute_wave_info(session.team, wave)
    session.enemy = make_wild(level=info.wild_level)
    return info


def _new_session(*, wave: int, log: list[str] | None = None) -> BattleSession:
    """
    Creates a fresh session:
    - resets team hp/exp/etc (later this should reset only in-memory session team)
    - spawns wave-scaled enemy
    - adds standard intro log
    """
    # For now we reset the sample team in-place.
    # Later: when team comes from DB, you'll build a fresh team list for the session.
    reset_team_full(SAMPLE_TEAM.pokemon)

    session = BattleSession(
        team=SAMPLE_TEAM.pokemon,
        active_index=0,
        enemy=make_wild(level=1),  # placeholder, overwritten below
        log=log or [],
    )

    _spawn_enemy_for_wave(session, wave)

    player = session.player()
    enemy = session.enemy

    session.log += [
        f"Wave {wave} begins!",
        f"A wild {enemy.name} appeared!",
        f"Go! {player.name}!",
    ]

    return session


def _ensure_session() -> BattleSession:
    global SESSION, WAVE
    if SESSION is None:
        WAVE = 1
        SESSION = _new_session(wave=WAVE, log=[])
    return SESSION


def _state_response(session: BattleSession, ok: bool = True, message: str | None = None):
    payload = {
        "ok": ok,
        "active_index": session.active_index,
        "player": _poke_to_dict(session.player()),
        "enemy": _poke_to_dict(session.enemy),
        "team": _team_payload(session.team),
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
    SESSION = _new_session(wave=WAVE, log=[])
    return _state_response(SESSION, ok=True)


@router.post("/run")
def run_away():
    """
    Run = full reset:
    - wave -> 1
    - team reset
    - new wild Pokémon (using wave scaling)
    """
    global SESSION, WAVE
    WAVE = 1
    SESSION = _new_session(wave=WAVE, log=["You ran away!"])
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
        # If team is wiped, just report it (front-end can force a reset/run)
        if team_wiped(session.team):
            session.log.append("Your team has been wiped. Run over.")
            return _state_response(session, ok=True, message=msg)

        # small heal between waves
        between_fight_heal(session.team)

        # next wave
        WAVE += 1
        _spawn_enemy_for_wave(session, WAVE)

        session.log.append(f"Wave {WAVE} begins!")
        session.log.append(f"A wild {session.enemy.name} appeared!")

    return _state_response(session, ok=ok, message=msg)


@router.post("/switch")
def switch_pokemon(body: SwitchRequest):
    session = _ensure_session()
    session.log = []

    ok, msg = session.apply_switch(body.index)
    return _state_response(session, ok=ok, message=msg)

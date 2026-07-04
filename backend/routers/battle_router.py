from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.sample_team import SAMPLE_TEAM
from services import team_repository
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


class StartRequest(BaseModel):
    team_id: Optional[int] = None


# -----------------------------
# Helpers
# -----------------------------
def _poke_to_dict(p):
    return p.to_dict()


def _team_payload(session: BattleSession):
    return {
        "id": session.team_id,
        "name": session.team_name,
        "pokemon": [_poke_to_dict(x) for x in session.team],
    }


def _load_team(team_id: Optional[int]):
    """Returns (pokemon_list, team_name, team_id) for a fresh session."""
    if team_id is not None:
        saved = team_repository.get_team(team_id)
        if saved is None:
            raise HTTPException(status_code=404, detail="Team not found")
        return saved["pokemon"], saved["name"], saved["id"]

    reset_team_full(SAMPLE_TEAM.pokemon)
    return SAMPLE_TEAM.pokemon, SAMPLE_TEAM.name, SAMPLE_TEAM.id


def _spawn_enemy_for_wave(session: BattleSession, wave: int):
    """
    Always spawn wild using the rogue scaling rules.
    Keeps /start, /run, and wave progression consistent.
    """
    info = compute_wave_info(session.team, wave)
    session.enemy = make_wild(level=info.wild_level)
    return info


def _new_session(*, wave: int, team_id: Optional[int] = None, log: list[str] | None = None) -> BattleSession:
    """
    Creates a fresh session:
    - loads the requested team (or falls back to SAMPLE_TEAM)
    - spawns wave-scaled enemy
    - adds standard intro log
    """
    team, team_name, team_ref = _load_team(team_id)

    session = BattleSession(
        team=team,
        active_index=0,
        enemy=make_wild(level=1),  # placeholder, overwritten below
        log=log or [],
        team_id=team_ref,
        team_name=team_name,
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
        "team": _team_payload(session),
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
def start_battle(body: StartRequest = StartRequest()):
    global SESSION, WAVE
    WAVE = 1
    SESSION = _new_session(wave=WAVE, team_id=body.team_id, log=[])
    return _state_response(SESSION, ok=True)


@router.post("/run")
def run_away():
    """
    Run = full reset:
    - wave -> 1
    - team reset (keeps whichever team the session was already using)
    - new wild Pokémon (using wave scaling)
    """
    global SESSION, WAVE
    prev_team_id = SESSION.team_id if SESSION and isinstance(SESSION.team_id, int) else None
    WAVE = 1
    SESSION = _new_session(wave=WAVE, team_id=prev_team_id, log=["You ran away!"])
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

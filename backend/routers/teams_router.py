# backend/routers/teams_router.py
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services import team_repository

router = APIRouter()


class MoveIn(BaseModel):
    name: str
    power: int
    type: str
    category: str
    accuracy: Optional[int] = None


class TeamMemberIn(BaseModel):
    pokedex_id: int
    nickname: Optional[str] = None
    level: int = 50
    ability: Optional[str] = None
    moves: list[MoveIn]


class TeamIn(BaseModel):
    name: str
    pokemon: list[TeamMemberIn]


@router.post("/")
def create_team(body: TeamIn):
    team_id = team_repository.create_team(
        body.name,
        [m.model_dump() for m in body.pokemon],
    )
    return {"id": team_id}


@router.get("/")
def list_teams():
    return team_repository.list_teams()


@router.get("/{team_id}")
def get_team(team_id: int):
    team = team_repository.get_team(team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return {
        "id": team["id"],
        "name": team["name"],
        "pokemon": [p.to_dict() for p in team["pokemon"]],
    }


@router.delete("/{team_id}")
def delete_team(team_id: int):
    if not team_repository.delete_team(team_id):
        raise HTTPException(status_code=404, detail="Team not found")
    return {"ok": True}

# backend/services/team_repository.py
#
# CRUD for user-built teams. PokeAPI has no idea these exist - this is the
# one thing that actually lives in our own SQLite database.

import json
from datetime import datetime, timezone
from typing import Optional

from db import get_connection
from models.pokemon import Pokemon
from services.pokedex_service import get_detail


def _insert_members(conn, team_id: int, pokemon: list) -> None:
    for slot, mon in enumerate(pokemon):
        conn.execute(
            """INSERT INTO team_members
               (team_id, slot, pokedex_id, nickname, level, ability, moves)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                team_id,
                slot,
                mon["pokedex_id"],
                mon.get("nickname"),
                mon.get("level", 50),
                mon.get("ability"),
                json.dumps(mon["moves"]),
            ),
        )


def create_team(name: str, pokemon: list) -> int:
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO teams (name, created_at) VALUES (?, ?)",
        (name, datetime.now(timezone.utc).isoformat()),
    )
    team_id = cur.lastrowid

    _insert_members(conn, team_id, pokemon)

    conn.commit()
    conn.close()
    return team_id


def list_teams() -> list:
    conn = get_connection()
    rows = conn.execute(
        """SELECT teams.id, teams.name, teams.created_at,
                  COUNT(team_members.id) AS pokemon_count
           FROM teams
           LEFT JOIN team_members ON team_members.team_id = teams.id
           GROUP BY teams.id
           ORDER BY teams.id DESC"""
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def _row_to_pokemon(row) -> Pokemon:
    detail = get_detail(row["pokedex_id"])
    return Pokemon(
        pokedex_id=row["pokedex_id"],
        name=row["nickname"] or detail["name"].title(),
        level=row["level"],
        types=detail["types"],
        base_stats=detail["base_stats"],
        moves=json.loads(row["moves"]),
        ability=row["ability"],
    )


def get_team(team_id: int) -> Optional[dict]:
    """Returns {id, name, pokemon: [Pokemon, ...]} or None if not found."""
    conn = get_connection()
    team_row = conn.execute("SELECT * FROM teams WHERE id = ?", (team_id,)).fetchone()
    if team_row is None:
        conn.close()
        return None

    member_rows = conn.execute(
        "SELECT * FROM team_members WHERE team_id = ? ORDER BY slot", (team_id,)
    ).fetchall()
    conn.close()

    return {
        "id": team_row["id"],
        "name": team_row["name"],
        "pokemon": [_row_to_pokemon(row) for row in member_rows],
    }


def update_team(team_id: int, name: str, pokemon: list) -> bool:
    """Full replace: renames the team, wipes its members, re-inserts from scratch."""
    conn = get_connection()
    exists = conn.execute("SELECT id FROM teams WHERE id = ?", (team_id,)).fetchone()
    if exists is None:
        conn.close()
        return False

    conn.execute("UPDATE teams SET name = ? WHERE id = ?", (name, team_id))
    conn.execute("DELETE FROM team_members WHERE team_id = ?", (team_id,))
    _insert_members(conn, team_id, pokemon)

    conn.commit()
    conn.close()
    return True


def delete_team(team_id: int) -> bool:
    conn = get_connection()
    cur = conn.execute("DELETE FROM teams WHERE id = ?", (team_id,))
    conn.commit()
    conn.close()
    return cur.rowcount > 0

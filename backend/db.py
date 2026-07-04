# backend/db.py
#
# Tiny SQLite setup - just enough to save/load custom teams. No ORM, plain
# sqlite3 is plenty at this size.

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "pokesim.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS team_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
            slot INTEGER NOT NULL,
            pokedex_id INTEGER NOT NULL,
            nickname TEXT,
            level INTEGER NOT NULL DEFAULT 50,
            ability TEXT,
            moves TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()

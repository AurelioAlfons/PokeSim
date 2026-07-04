# backend/services/pokeapi_client.py
#
# Thin wrapper around PokeAPI. We call it live (no local copy of the dex),
# but cache every response in memory for the life of the process - Pokemon
# stats/moves never change, so there's no reason to hit the network twice
# for the same id.

import requests

BASE_URL = "https://pokeapi.co/api/v2"

_CACHE = {}


def _get_json(path: str) -> dict:
    if path not in _CACHE:
        res = requests.get(f"{BASE_URL}/{path}", timeout=10)
        res.raise_for_status()
        _CACHE[path] = res.json()
    return _CACHE[path]


def get_pokemon(dex_id: int) -> dict:
    return _get_json(f"pokemon/{dex_id}")


def get_move(name_or_id) -> dict:
    return _get_json(f"move/{name_or_id}")

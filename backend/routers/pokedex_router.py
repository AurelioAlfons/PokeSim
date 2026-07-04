# backend/routers/pokedex_router.py
from fastapi import APIRouter, HTTPException

from services.pokedex_service import GEN4_DEX_RANGE, get_detail, list_summary

router = APIRouter()


@router.get("/")
def get_pokedex():
    return list_summary()


@router.get("/{dex_id}")
def get_pokemon_detail(dex_id: int):
    if dex_id not in GEN4_DEX_RANGE:
        raise HTTPException(status_code=404, detail="Not a Gen 4 Pokemon")
    return get_detail(dex_id)

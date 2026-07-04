// src/api/pokedex.js
import { get } from "./client";

export function fetchPokedexList() {
  return get("/pokedex/");
}

export function fetchPokemonDetail(dexId) {
  return get(`/pokedex/${dexId}`);
}

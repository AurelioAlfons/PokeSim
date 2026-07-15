// src/utils/pokemonDefaults.js
const DEFAULT_LEVEL = 50;

export function titleCase(s = "") {
  return s.replace(/(^|-)([a-z])/g, (_, sep, c) => (sep ? " " : "") + c.toUpperCase());
}

export function pickDefaultMoves(moves, level) {
  const learnable = moves.filter((m) => m.level_learned_at <= level);
  const pool = learnable.length ? learnable : moves;
  const chosen = pool.slice(-4);
  const slots = [null, null, null, null];
  chosen.forEach((m, i) => {
    slots[i] = m;
  });
  return slots;
}

export function buildDefaultSlotData(detail) {
  const ability =
    detail.abilities.find((a) => !a.hidden)?.name || detail.abilities[0]?.name || "";

  const moves = pickDefaultMoves(detail.moves, DEFAULT_LEVEL)
    .filter(Boolean)
    .map((m) => ({
      name: m.name,
      power: m.power,
      type: m.type,
      category: m.category,
      accuracy: m.accuracy,
    }));

  return {
    pokedex_id: detail.id,
    name: titleCase(detail.name),
    nickname: null,
    sprite: detail.sprite,
    types: detail.types,
    level: DEFAULT_LEVEL,
    ability,
    moves,
  };
}

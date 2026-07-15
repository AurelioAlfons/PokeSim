// src/components/PokemonDetailModal.jsx
import React, { useEffect, useState } from "react";
import PokemonSprite from "./PokemonSprite";
import TypeBadge from "./TypeBadge";
import { fetchPokemonDetail } from "../api/pokedex";
import { titleCase, pickDefaultMoves } from "../utils/pokemonDefaults";

export default function PokemonDetailModal({ open, pokedexId, initial, onConfirm, onClose }) {
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [level, setLevel] = useState(50);
  const [ability, setAbility] = useState("");
  const [nickname, setNickname] = useState("");
  const [moveSlots, setMoveSlots] = useState([null, null, null, null]);

  useEffect(() => {
    if (!open || !pokedexId) return;

    let cancelled = false;
    setLoading(true);
    setError(null);
    setDetail(null);

    fetchPokemonDetail(pokedexId)
      .then((data) => {
        if (cancelled) return;
        setDetail(data);

        const initLevel = initial?.level || 50;
        setLevel(initLevel);
        setNickname(initial?.nickname || "");

        const abilityNames = data.abilities.map((a) => a.name);
        setAbility(
          initial?.ability && abilityNames.includes(initial.ability)
            ? initial.ability
            : data.abilities.find((a) => !a.hidden)?.name || data.abilities[0]?.name || ""
        );

        if (initial?.moves?.length) {
          const byName = Object.fromEntries(data.moves.map((m) => [m.name, m]));
          const slots = [0, 1, 2, 3].map((i) => {
            const saved = initial.moves[i];
            if (!saved) return null;
            return byName[saved.name] || saved;
          });
          setMoveSlots(slots);
        } else {
          setMoveSlots(pickDefaultMoves(data.moves, initLevel));
        }
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [open, pokedexId, initial]);

  if (!open) return null;

  const usedMoveNames = moveSlots.filter(Boolean).map((m) => m.name);

  const setMoveSlot = (idx, moveName) => {
    setMoveSlots((prev) => {
      const next = [...prev];
      if (!moveName) {
        next[idx] = null;
      } else {
        next[idx] = detail.moves.find((m) => m.name === moveName) || null;
      }
      return next;
    });
  };

  const handleConfirm = () => {
    if (!detail || !ability) return;
    onConfirm({
      pokedex_id: detail.id,
      name: nickname.trim() || titleCase(detail.name),
      nickname: nickname.trim() || null,
      sprite: detail.sprite,
      types: detail.types,
      level: Math.max(1, Math.min(100, Number(level) || 1)),
      ability,
      moves: moveSlots.filter(Boolean).map((m) => ({
        name: m.name,
        power: m.power,
        type: m.type,
        category: m.category,
        accuracy: m.accuracy,
        ailment: m.ailment,
      })),
    });
  };

  return (
    <div style={styles.overlay} onClick={onClose}>
      <div style={styles.card} onClick={(e) => e.stopPropagation()}>
        {loading && <div style={styles.centerMsg}>Loading...</div>}
        {error && !loading && (
          <div style={{ ...styles.centerMsg, color: "#e44848" }}>
            Failed to load: {error}
          </div>
        )}

        {detail && !loading && (
          <>
            <div style={styles.header}>
              <PokemonSprite src={detail.sprite} alt={detail.name} size={84} />
              <div>
                <div style={styles.name}>{titleCase(detail.name)}</div>
                <div style={{ display: "flex", gap: 6, marginTop: 4 }}>
                  {detail.types.map((t) => (
                    <TypeBadge key={t} type={t} />
                  ))}
                </div>
              </div>
              <button style={styles.closeBtn} onClick={onClose}>
                ×
              </button>
            </div>

            <div style={styles.row}>
              <label style={styles.label}>Nickname</label>
              <input
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
                placeholder={titleCase(detail.name)}
                style={styles.input}
              />
            </div>

            <div style={styles.row}>
              <label style={styles.label}>Level</label>
              <input
                type="number"
                min={1}
                max={100}
                value={level}
                onChange={(e) => setLevel(e.target.value)}
                style={{ ...styles.input, width: 90 }}
              />
            </div>

            <div style={styles.row}>
              <label style={styles.label}>Ability</label>
              <select
                value={ability}
                onChange={(e) => setAbility(e.target.value)}
                style={styles.select}
              >
                {detail.abilities.map((a) => (
                  <option key={a.name} value={a.name}>
                    {titleCase(a.name)}
                    {a.hidden ? " (Hidden)" : ""}
                  </option>
                ))}
              </select>
            </div>

            <div style={{ marginTop: 4 }}>
              <label style={styles.label}>Moves</label>
              <div style={styles.movesGrid}>
                {[0, 1, 2, 3].map((i) => {
                  const current = moveSlots[i];
                  return (
                    <select
                      key={i}
                      value={current?.name || ""}
                      onChange={(e) => setMoveSlot(i, e.target.value)}
                      style={styles.select}
                    >
                      <option value="">— Empty —</option>
                      {detail.moves.map((m) => {
                        const usedElsewhere =
                          usedMoveNames.includes(m.name) && current?.name !== m.name;
                        return (
                          <option key={m.name} value={m.name} disabled={usedElsewhere}>
                            {m.name} (Lv {m.level_learned_at}, {m.type})
                          </option>
                        );
                      })}
                    </select>
                  );
                })}
              </div>
            </div>

            <div style={styles.actions}>
              <button style={styles.cancelBtn} onClick={onClose}>
                Cancel
              </button>
              <button style={styles.confirmBtn} onClick={handleConfirm} disabled={!ability}>
                {initial ? "Update Pokemon" : "Add to Team"}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

const styles = {
  overlay: {
    position: "fixed",
    inset: 0,
    background: "rgba(0,0,0,0.6)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 1000,
    padding: 20,
  },
  card: {
    width: "100%",
    maxWidth: 480,
    maxHeight: "90vh",
    overflowY: "auto",
    background: "#fff",
    borderRadius: 16,
    border: "3px solid rgba(0,0,0,0.85)",
    boxShadow: "0 12px 0 rgba(0,0,0,0.85)",
    padding: 24,
  },
  centerMsg: {
    padding: 40,
    textAlign: "center",
    fontWeight: 700,
    color: "#666",
  },
  header: {
    display: "flex",
    alignItems: "center",
    gap: 12,
    marginBottom: 16,
    position: "relative",
  },
  name: {
    fontSize: 22,
    fontWeight: 900,
    textTransform: "capitalize",
  },
  closeBtn: {
    marginLeft: "auto",
    width: 32,
    height: 32,
    borderRadius: 8,
    border: "2px solid #111",
    background: "#f3f3f3",
    fontSize: 18,
    fontWeight: 900,
    cursor: "pointer",
    lineHeight: 1,
  },
  row: {
    display: "flex",
    alignItems: "center",
    gap: 12,
    marginBottom: 12,
  },
  label: {
    minWidth: 80,
    fontWeight: 800,
    fontSize: 13,
    color: "#333",
  },
  input: {
    flex: 1,
    height: 36,
    borderRadius: 8,
    border: "2px solid #ddd",
    padding: "0 10px",
    outline: "none",
    fontSize: 14,
  },
  select: {
    height: 36,
    borderRadius: 8,
    border: "2px solid #ddd",
    padding: "0 8px",
    outline: "none",
    fontSize: 13,
    flex: 1,
    minWidth: 0,
  },
  movesGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 8,
    marginTop: 6,
  },
  actions: {
    display: "flex",
    gap: 10,
    marginTop: 20,
    justifyContent: "flex-end",
  },
  cancelBtn: {
    height: 40,
    padding: "0 16px",
    borderRadius: 8,
    border: "2px solid #111",
    background: "#fff",
    fontWeight: 800,
    cursor: "pointer",
  },
  confirmBtn: {
    height: 40,
    padding: "0 18px",
    borderRadius: 8,
    border: "2px solid #111",
    background: "#ff2d2d",
    color: "#000",
    fontWeight: 800,
    cursor: "pointer",
    boxShadow: "3px 3px 0 rgba(0,0,0,0.25)",
  },
};

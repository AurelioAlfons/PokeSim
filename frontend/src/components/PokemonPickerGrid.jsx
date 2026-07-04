// src/components/PokemonPickerGrid.jsx
import React, { useEffect, useMemo, useState } from "react";
import PokemonSprite from "./PokemonSprite";
import TypeBadge from "./TypeBadge";
import { TYPE_COLORS } from "../constants/types";
import { fetchPokedexList } from "../api/pokedex";

const ALL_TYPES = Object.keys(TYPE_COLORS);

export default function PokemonPickerGrid({ onSelect, teamFull }) {
  const [pokedex, setPokedex] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetchPokedexList()
      .then((data) => {
        if (!cancelled) setPokedex(data);
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
  }, []);

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    return pokedex.filter((p) => {
      const matchesSearch = !q || p.name.toLowerCase().includes(q);
      const matchesType = !typeFilter || p.types.includes(typeFilter);
      return matchesSearch && matchesType;
    });
  }, [pokedex, search, typeFilter]);

  return (
    <div style={styles.wrap}>
      <div style={styles.filters}>
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search Pokemon..."
          style={styles.searchInput}
        />

        <div style={styles.typeRow}>
          <TypeChip
            label="All"
            active={typeFilter === null}
            onClick={() => setTypeFilter(null)}
          />
          {ALL_TYPES.map((t) => (
            <TypeChip
              key={t}
              label={t}
              type={t}
              active={typeFilter === t}
              onClick={() => setTypeFilter(typeFilter === t ? null : t)}
            />
          ))}
        </div>
      </div>

      <div style={styles.gridBox}>
        {loading && (
          <div style={styles.centerMsg}>
            Loading Pokedex... (first load can take a moment)
          </div>
        )}

        {error && !loading && (
          <div style={{ ...styles.centerMsg, color: "#e44848" }}>
            Failed to load Pokedex: {error}
          </div>
        )}

        {!loading && !error && filtered.length === 0 && (
          <div style={styles.centerMsg}>No Pokemon match your search.</div>
        )}

        {!loading && !error && filtered.length > 0 && (
          <div style={styles.grid}>
            {filtered.map((p) => (
              <PokemonCard
                key={p.id}
                pokemon={p}
                disabled={teamFull}
                onClick={() => !teamFull && onSelect(p)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function TypeChip({ label, type, active, onClick }) {
  const style = type ? TYPE_COLORS[type] : { bg: "#111", text: "#f7e733" };

  return (
    <button
      onClick={onClick}
      style={{
        border: "2px solid rgba(0,0,0,0.85)",
        borderRadius: 8,
        padding: "4px 10px",
        fontSize: 12,
        fontWeight: 800,
        textTransform: "capitalize",
        cursor: "pointer",
        background: active ? style.bg : "#f3f3f3",
        color: active ? style.text : "#555",
        opacity: active ? 1 : 0.85,
        transition: "all 120ms ease",
      }}
    >
      {label}
    </button>
  );
}

function PokemonCard({ pokemon, disabled, onClick }) {
  const [hover, setHover] = useState(false);

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 4,
        padding: 8,
        borderRadius: 10,
        border: "3px solid rgba(0,0,0,0.85)",
        background: "#f7f7f7",
        cursor: disabled ? "not-allowed" : "pointer",
        opacity: disabled ? 0.45 : 1,
        boxShadow: hover && !disabled ? "0 6px 0 rgba(0,0,0,0.85)" : "0 3px 0 rgba(0,0,0,0.85)",
        transform: hover && !disabled ? "translateY(-2px)" : "translateY(0)",
        transition: "transform 120ms ease, box-shadow 120ms ease",
      }}
    >
      <PokemonSprite src={pokemon.sprite} alt={pokemon.name} size={64} />
      <div style={{ fontWeight: 800, fontSize: 13, textTransform: "capitalize" }}>
        {pokemon.name}
      </div>
      <div style={{ display: "flex", gap: 4 }}>
        {pokemon.types.map((t) => (
          <TypeBadge key={t} type={t} size="sm" />
        ))}
      </div>
    </button>
  );
}

const styles = {
  wrap: {
    flex: 1,
    minWidth: 0,
    display: "flex",
    flexDirection: "column",
    gap: 12,
  },
  filters: {
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },
  searchInput: {
    height: 38,
    borderRadius: 8,
    border: "2px solid #111",
    padding: "0 12px",
    outline: "none",
    fontSize: 14,
    background: "#fff",
  },
  typeRow: {
    display: "flex",
    flexWrap: "wrap",
    gap: 6,
  },
  gridBox: {
    border: "3px solid rgba(0,0,0,0.85)",
    borderRadius: 12,
    background: "rgba(255,255,255,0.9)",
    padding: 14,
    height: 420,
    overflowY: "auto",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(96px, 1fr))",
    gap: 10,
  },
  centerMsg: {
    height: "100%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
    color: "#666",
    fontWeight: 700,
    padding: 20,
  },
};

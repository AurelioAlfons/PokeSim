// src/components/SavedTeamViewModal.jsx
import React, { useEffect, useState } from "react";
import PokemonSprite from "./PokemonSprite";
import TypeBadge from "./TypeBadge";
import { fetchTeam } from "../api/teams";

export default function SavedTeamViewModal({ teamId, onClose }) {
  const [team, setTeam] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!teamId) return;

    let cancelled = false;
    setLoading(true);
    setError(null);
    setTeam(null);

    fetchTeam(teamId)
      .then((data) => {
        if (!cancelled) setTeam(data);
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
  }, [teamId]);

  if (!teamId) return null;

  return (
    <div style={styles.overlay} onClick={onClose}>
      <div style={styles.card} onClick={(e) => e.stopPropagation()}>
        <div style={styles.header}>
          <div style={styles.title}>{team ? team.name : "Team"}</div>
          <button style={styles.closeBtn} onClick={onClose}>
            ×
          </button>
        </div>

        {loading && <div style={styles.centerMsg}>Loading...</div>}
        {error && !loading && (
          <div style={{ ...styles.centerMsg, color: "#e44848" }}>
            Failed to load: {error}
          </div>
        )}

        {team && !loading && team.pokemon.length === 0 && (
          <div style={styles.centerMsg}>This team has no Pokemon.</div>
        )}

        {team && !loading && team.pokemon.length > 0 && (
          <div style={styles.grid}>
            {team.pokemon.map((p, i) => (
              <div key={i} style={styles.mon}>
                <PokemonSprite src={p.sprite} alt={p.name} size={64} />
                <div style={styles.monName}>{p.name}</div>
                <div style={styles.monLevel}>Lv {p.level}</div>
                <div style={styles.typeRow}>
                  {p.types.map((t) => (
                    <TypeBadge key={t} type={t} size="sm" />
                  ))}
                </div>
                <div style={styles.moveList}>
                  {p.moves.map((m) => (
                    <div key={m.name} style={styles.moveRow}>
                      {m.name}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
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
    maxWidth: 640,
    maxHeight: "90vh",
    overflowY: "auto",
    background: "#fff",
    borderRadius: 16,
    border: "3px solid rgba(0,0,0,0.85)",
    boxShadow: "0 12px 0 rgba(0,0,0,0.85)",
    padding: 24,
  },
  header: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 16,
  },
  title: {
    fontSize: 22,
    fontWeight: 900,
  },
  closeBtn: {
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
  centerMsg: {
    padding: 40,
    textAlign: "center",
    fontWeight: 700,
    color: "#666",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(140px, 1fr))",
    gap: 14,
  },
  mon: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 4,
    padding: "10px 8px",
    borderRadius: 10,
    border: "3px solid rgba(0,0,0,0.85)",
    background: "#f7f7f7",
  },
  monName: {
    fontWeight: 800,
    fontSize: 13,
    textTransform: "capitalize",
    textAlign: "center",
  },
  monLevel: {
    fontSize: 11,
    opacity: 0.75,
  },
  typeRow: {
    display: "flex",
    flexWrap: "wrap",
    justifyContent: "center",
    gap: 3,
  },
  moveList: {
    marginTop: 6,
    width: "100%",
    display: "flex",
    flexDirection: "column",
    gap: 2,
  },
  moveRow: {
    fontSize: 11,
    color: "#444",
    textAlign: "center",
    whiteSpace: "nowrap",
    overflow: "hidden",
    textOverflow: "ellipsis",
  },
};

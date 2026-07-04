// src/components/SavedTeamsBar.jsx
import React, { useEffect, useState } from "react";
import { fetchTeams, fetchTeam, deleteTeam } from "../api/teams";

export default function SavedTeamsBar({ refreshToken, onLoad }) {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState(null);

  const refresh = () => {
    setLoading(true);
    fetchTeams()
      .then(setTeams)
      .catch(() => setTeams([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refreshToken]);

  const handleLoad = async (id) => {
    setBusyId(id);
    try {
      const team = await fetchTeam(id);
      onLoad(team);
    } catch (err) {
      alert(`Failed to load team: ${err.message}`);
    } finally {
      setBusyId(null);
    }
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Delete "${name}"? This cannot be undone.`)) return;
    setBusyId(id);
    try {
      await deleteTeam(id);
      refresh();
    } catch (err) {
      alert(`Failed to delete team: ${err.message}`);
    } finally {
      setBusyId(null);
    }
  };

  return (
    <div style={styles.wrap}>
      <div style={styles.title}>Saved Teams</div>

      {loading ? (
        <div style={styles.muted}>Loading...</div>
      ) : teams.length === 0 ? (
        <div style={styles.muted}>No saved teams yet — build one and hit Save Team!</div>
      ) : (
        <div style={styles.row}>
          {teams.map((t) => (
            <div key={t.id} style={styles.chip}>
              <div style={styles.chipName}>{t.name}</div>
              <div style={styles.chipMeta}>{t.pokemon_count} / 6</div>
              <div style={styles.chipActions}>
                <button
                  style={styles.loadBtn}
                  disabled={busyId === t.id}
                  onClick={() => handleLoad(t.id)}
                >
                  {busyId === t.id ? "..." : "Load"}
                </button>
                <button
                  style={styles.deleteBtn}
                  disabled={busyId === t.id}
                  onClick={() => handleDelete(t.id, t.name)}
                  title="Delete team"
                >
                  ×
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  wrap: {
    marginTop: 28,
  },
  title: {
    fontSize: 18,
    fontWeight: 800,
    marginBottom: 10,
    color: "#111",
  },
  muted: {
    color: "#666",
    fontSize: 14,
    fontWeight: 600,
  },
  row: {
    display: "flex",
    flexWrap: "wrap",
    gap: 10,
  },
  chip: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "8px 12px",
    borderRadius: 10,
    border: "2px solid rgba(0,0,0,0.85)",
    background: "rgba(255,255,255,0.9)",
  },
  chipName: {
    fontWeight: 800,
    fontSize: 14,
  },
  chipMeta: {
    fontSize: 12,
    color: "#666",
  },
  chipActions: {
    display: "flex",
    gap: 6,
  },
  loadBtn: {
    height: 28,
    padding: "0 10px",
    borderRadius: 6,
    border: "2px solid #111",
    background: "#f7e733",
    color: "#111",
    fontWeight: 800,
    fontSize: 12,
    cursor: "pointer",
  },
  deleteBtn: {
    width: 24,
    height: 24,
    borderRadius: "50%",
    border: "2px solid #111",
    background: "#ff2d2d",
    color: "#fff",
    fontWeight: 900,
    fontSize: 13,
    lineHeight: 1,
    cursor: "pointer",
    display: "grid",
    placeItems: "center",
  },
};

// src/components/SavedTeamsBar.jsx
import React, { useEffect, useState } from "react";
import { fetchTeams, fetchTeam, deleteTeam } from "../api/teams";
import SavedTeamViewModal from "./SavedTeamViewModal";

export default function SavedTeamsBar({ refreshToken, onLoad }) {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState(null);
  const [viewingId, setViewingId] = useState(null);
  const [isOpen, setIsOpen] = useState(false);

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
      setIsOpen(false);
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
    <>
      <button style={styles.tab} onClick={() => setIsOpen((o) => !o)}>
        Saved Teams
      </button>

      {isOpen && <div style={styles.backdrop} onClick={() => setIsOpen(false)} />}

      <div
        style={{
          ...styles.panel,
          transform: isOpen ? "translateX(0)" : "translateX(100%)",
        }}
      >
        <div style={styles.title}>Saved Teams</div>

        {loading ? (
          <div style={styles.muted}>Loading...</div>
        ) : teams.length === 0 ? (
          <div style={styles.muted}>No saved teams yet — build one and hit Save Team!</div>
        ) : (
          <div style={styles.list}>
            {teams.map((t) => (
              <div key={t.id} style={styles.chip}>
                <div style={styles.chipInfo}>
                  <div style={styles.chipName}>{t.name}</div>
                  <div style={styles.chipMeta}>{t.pokemon_count} / 6</div>
                </div>
                <div style={styles.chipActions}>
                  <button
                    style={styles.viewBtn}
                    disabled={busyId === t.id}
                    onClick={() => setViewingId(t.id)}
                  >
                    View
                  </button>
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

      <SavedTeamViewModal teamId={viewingId} onClose={() => setViewingId(null)} />
    </>
  );
}

const styles = {
  tab: {
    position: "fixed",
    top: "50%",
    right: 0,
    transform: "translateY(-50%)",
    writingMode: "vertical-rl",
    padding: "16px 8px",
    borderRadius: "8px 0 0 8px",
    border: "2px solid rgba(0,0,0,0.85)",
    borderRight: "none",
    background: "#f7e733",
    color: "#111",
    fontWeight: 800,
    fontSize: 13,
    letterSpacing: 0.5,
    cursor: "pointer",
    boxShadow: "-3px 0 0 rgba(0,0,0,0.25)",
    zIndex: 902,
  },
  backdrop: {
    position: "fixed",
    inset: 0,
    background: "rgba(0,0,0,0.55)",
    zIndex: 900,
  },
  panel: {
    position: "fixed",
    top: 0,
    right: 0,
    height: "100vh",
    width: 340,
    maxWidth: "90vw",
    boxSizing: "border-box",
    background: "#fff",
    borderLeft: "3px solid rgba(0,0,0,0.85)",
    boxShadow: "-6px 0 0 rgba(0,0,0,0.15)",
    padding: 20,
    overflowY: "auto",
    transition: "transform 250ms ease",
    zIndex: 901,
  },
  title: {
    fontSize: 18,
    fontWeight: 800,
    marginBottom: 14,
    color: "#111",
  },
  muted: {
    color: "#666",
    fontSize: 14,
    fontWeight: 600,
  },
  list: {
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },
  chip: {
    display: "flex",
    flexDirection: "column",
    gap: 8,
    padding: "10px 12px",
    borderRadius: 10,
    border: "2px solid rgba(0,0,0,0.85)",
    background: "rgba(255,255,255,0.9)",
  },
  chipInfo: {
    display: "flex",
    alignItems: "baseline",
    justifyContent: "space-between",
    gap: 10,
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
  viewBtn: {
    flex: 1,
    height: 28,
    padding: "0 10px",
    borderRadius: 6,
    border: "2px solid #111",
    background: "#fff",
    color: "#111",
    fontWeight: 800,
    fontSize: 12,
    cursor: "pointer",
  },
  loadBtn: {
    flex: 1,
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
    width: 28,
    height: 28,
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
    flexShrink: 0,
  },
};

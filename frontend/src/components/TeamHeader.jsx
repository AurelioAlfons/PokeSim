// src/components/TeamHeader.jsx
import React from "react";

/* ---------- Hover helpers ---------- */
const hoverOnSave = (e) => {
  e.currentTarget.style.background = "#fff";
  e.currentTarget.style.color = "#ff2d2d";
};

const hoverOffSave = (e) => {
  e.currentTarget.style.background = "#ff2d2d";
  e.currentTarget.style.color = "#000";
};

const hoverOnCancel = (e) => {
  e.currentTarget.style.background = "#ff2d2d";
  e.currentTarget.style.color = "#fff";
};

const hoverOffCancel = (e) => {
  e.currentTarget.style.background = "#fff";
  e.currentTarget.style.color = "#000";
};

/* ---------- Component ---------- */
export default function TeamHeader({
  teamName = "",
  onTeamNameChange = () => {},
  description = "",
  onDescriptionChange = () => {},
  onCancel = () => {},
  onSave = () => {},
}) {
  return (
    <div style={styles.wrap}>
      {/* LEFT */}
      <div style={styles.left}>
        <input
          value={teamName || ""}
          placeholder="New Team"
          onChange={(e) => onTeamNameChange(e.target.value)}
          onBlur={() => {
            if (!teamName.trim()) onTeamNameChange("");
          }}
          style={styles.teamNameInput}
        />

        <input
          value={description}
          onChange={(e) => onDescriptionChange(e.target.value)}
          placeholder="Add a description..."
          style={styles.descInput}
        />
      </div>

      {/* RIGHT */}
      <div style={styles.right}>
        {/* SAVE */}
        <button
          onClick={onSave}
          style={styles.saveBtn}
          onMouseEnter={hoverOnSave}
          onMouseLeave={hoverOffSave}
        >
          <span style={styles.saveIcon} aria-hidden>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M17 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V7l-4-4ZM12 19a3 3 0 1 1 0-6 3 3 0 0 1 0 6ZM6 5h9v4H6V5Z" />
            </svg>
          </span>
          Save Team
        </button>

        {/* CANCEL */}
        <button
          onClick={onCancel}
          style={styles.cancelBtn}
          onMouseEnter={hoverOnCancel}
          onMouseLeave={hoverOffCancel}
        >
          Cancel
        </button>
      </div>
    </div>
  );
}

/* ---------- Styles ---------- */
const styles = {
  wrap: {
    display: "flex",
    alignItems: "flex-start",
    justifyContent: "space-between",
    gap: 16,
    width: "100%",
  },

  left: {
    flex: 1,
    minWidth: 280,
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },

  teamNameInput: {
    width: "95%",
    height: 42,
    borderRadius: 8,
    border: "1px solid #eee",
    padding: "0 12px",
    outline: "none",
    fontSize: 26,
    fontWeight: 900,
    letterSpacing: 1,
    background: "#f3f3f3",
  },

  descInput: {
    width: "95%",
    height: 38,
    borderRadius: 8,
    border: "1px solid #e7e7e7",
    padding: "0 12px",
    outline: "none",
    fontSize: 14,
    background: "#f7f7f7",
  },

  right: {
    display: "flex",
    flexDirection: "column",
    gap: 10,
    marginTop: 0,
  },

  saveBtn: {
    height: 42,
    width: 140,
    borderRadius: 8,
    border: "2px solid #111",
    background: "#ff2d2d",
    color: "#000",
    fontWeight: 800,
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    boxShadow: "3px 3px 0 rgba(0,0,0,0.25)",
    transition: "background 0.15s ease, color 0.15s ease",
  },

  cancelBtn: {
    height: 42,
    width: 140,
    borderRadius: 8,
    border: "2px solid #111",
    background: "#fff",
    color: "#000",
    fontWeight: 700,
    cursor: "pointer",
    transition: "background 0.15s ease, color 0.15s ease",
  },

  saveIcon: {
    display: "inline-flex",
    alignItems: "center",
  },
};

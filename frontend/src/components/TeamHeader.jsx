// src/components/TeamHeader.jsx
import React from "react";

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
      {/* LEFT: two equal-width inputs */}
      <div style={styles.left}>
        <input
          value={teamName || ""}
          placeholder="New Team"
          onChange={(e) => onTeamNameChange(e.target.value)}
          onBlur={() => {
            if (!teamName.trim()) {
              onTeamNameChange("");
            }
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

      {/* RIGHT: buttons */}
      <div style={styles.right}>
        <button onClick={onCancel} style={styles.cancelBtn}>
          Cancel
        </button>

        <button onClick={onSave} style={styles.saveBtn}>
          <span style={styles.saveIcon} aria-hidden>
            💾
          </span>
          Save Team
        </button>
      </div>
    </div>
  );
}

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

  // SAME WIDTH as description because both are 100%
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
    alignItems: "center",
    gap: 12,
    marginTop: 6,
  },

  cancelBtn: {
    height: 38,
    padding: "0 16px",
    borderRadius: 8,
    border: "2px solid #111",
    background: "#fff",
    fontWeight: 700,
    cursor: "pointer",
  },

  saveBtn: {
    height: 38,
    padding: "0 16px",
    borderRadius: 8,
    border: "2px solid #111",
    background: "#f3a2a2",
    fontWeight: 800,
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    gap: 10,
    boxShadow: "3px 3px 0 rgba(0,0,0,0.25)",
  },

  saveIcon: {
    fontSize: 16,
    lineHeight: 1,
  },
};

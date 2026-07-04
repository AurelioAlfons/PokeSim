// src/components/TeamSlotsPanel.jsx
import React from "react";
import PokemonSprite from "./PokemonSprite";
import TypeBadge from "./TypeBadge";

export default function TeamSlotsPanel({ slots, onSlotClick, onRemove }) {
  const filledCount = slots.filter(Boolean).length;

  return (
    <div style={styles.wrap}>
      <div style={styles.headerRow}>
        <div style={styles.title}>Your Team</div>
        <div style={styles.count}>Members: {filledCount} / 6</div>
      </div>

      <div style={styles.grid}>
        {slots.map((slot, i) =>
          slot ? (
            <FilledSlot
              key={i}
              slot={slot}
              onClick={() => onSlotClick(i)}
              onRemove={(e) => {
                e.stopPropagation();
                onRemove(i);
              }}
            />
          ) : (
            <EmptySlot key={i} />
          )
        )}
      </div>

      <div style={styles.tip}>
        <strong>Tip:</strong>
        <br />
        A balanced team needs both Physical and Special attackers, plus
        defensive pivots!
      </div>
    </div>
  );
}

function FilledSlot({ slot, onClick, onRemove }) {
  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") onClick();
      }}
      style={styles.filledSlot}
    >
      <button style={styles.removeBtn} onClick={onRemove} title="Remove">
        ×
      </button>
      <PokemonSprite src={slot.sprite} alt={slot.name} size={56} />
      <div
        style={{
          fontWeight: 800,
          fontSize: 13,
          textTransform: "capitalize",
          width: "100%",
          textAlign: "center",
          whiteSpace: "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis",
        }}
      >
        {slot.name}
      </div>
      <div style={{ fontSize: 11, opacity: 0.75 }}>Lv {slot.level}</div>
      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: 3 }}>
        {slot.types.map((t) => (
          <TypeBadge key={t} type={t} size="sm" />
        ))}
      </div>
    </div>
  );
}

function EmptySlot() {
  return (
    <div style={styles.emptySlot}>
      <span style={{ fontSize: 24, color: "#bbb" }}>+</span>
      <span style={{ fontSize: 11, color: "#999", fontWeight: 700 }}>Empty</span>
    </div>
  );
}

const styles = {
  wrap: {
    width: "100%",
    boxSizing: "border-box",
    border: "2px solid black",
    borderRadius: 12,
    padding: 20,
  },
  headerRow: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "baseline",
    marginBottom: 14,
  },
  title: {
    fontSize: 22,
    fontWeight: 800,
    color: "#ff2d2d",
  },
  count: {
    fontSize: 13,
    fontWeight: 700,
    color: "#555",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(6, 1fr)",
    gap: 14,
    marginBottom: 16,
  },
  filledSlot: {
    position: "relative",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "flex-start",
    gap: 5,
    padding: "10px 6px",
    minHeight: 140,
    boxSizing: "border-box",
    borderRadius: 10,
    border: "3px solid rgba(0,0,0,0.85)",
    background: "#f7f7f7",
    cursor: "pointer",
  },
  removeBtn: {
    position: "absolute",
    top: -8,
    right: -8,
    width: 20,
    height: 20,
    borderRadius: "50%",
    border: "2px solid #111",
    background: "#ff2d2d",
    color: "#fff",
    fontSize: 13,
    fontWeight: 900,
    lineHeight: 1,
    cursor: "pointer",
    display: "grid",
    placeItems: "center",
  },
  emptySlot: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    gap: 2,
    minHeight: 140,
    boxSizing: "border-box",
    borderRadius: 10,
    border: "2px dashed #cfcfcf",
  },
  tip: {
    background: "#eef5ff",
    border: "1px solid #c6dbff",
    borderRadius: 6,
    padding: 12,
    fontSize: 14,
  },
};

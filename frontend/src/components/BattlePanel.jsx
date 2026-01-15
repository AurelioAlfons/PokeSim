import React from "react";

export default function BattlePanel({ log, onFight, onPokemon, onBag, onRun }) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "1.4fr 1fr",
        gap: 14,
        marginTop: 16,
      }}
    >
      {/* Log box */}
      <div
        style={{
          height: 180,
          borderRadius: 12,
          border: "3px solid rgba(0,0,0,0.85)",
          background: "rgba(0,0,0,0.85)",
          color: "#fff",
          padding: 14,
          fontWeight: 800,
          overflow: "auto",
        }}
      >
        {log.map((l, i) => (
          <div key={i} style={{ marginBottom: 6, opacity: i === 0 ? 1 : 0.85 }}>
            {l}
          </div>
        ))}
      </div>

      {/* Menu buttons */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        <MenuBtn label="FIGHT" bg="#e44848" onClick={onFight} />
        <MenuBtn label="POKEMON" bg="#25c05a" onClick={onPokemon} />
        <MenuBtn label="BAG" bg="#e1b200" onClick={onBag} />
        <MenuBtn label="RUN" bg="#3a7ff0" onClick={onRun} />
      </div>
    </div>
  );
}

function MenuBtn({ label, bg, onClick }) {
  const base = {
    height: 92,
    borderRadius: 10,
    border: "3px solid rgba(0,0,0,0.85)",
    boxShadow: "0 8px 0 rgba(0,0,0,0.85)",
    color: "#fff",
    fontWeight: 900,
    fontSize: 22,
    letterSpacing: 1,
    cursor: "pointer",
    transition: "transform 120ms ease, box-shadow 120ms ease",
    background: bg,
  };

  return (
    <button
      style={base}
      onClick={onClick}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "translateY(-2px)";
        e.currentTarget.style.boxShadow = "0 10px 0 rgba(0,0,0,0.85)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "translateY(0px)";
        e.currentTarget.style.boxShadow = "0 8px 0 rgba(0,0,0,0.85)";
      }}
      onMouseDown={(e) => {
        e.currentTarget.style.transform = "translateY(3px)";
        e.currentTarget.style.boxShadow = "0 4px 0 rgba(0,0,0,0.85)";
      }}
      onMouseUp={(e) => {
        e.currentTarget.style.transform = "translateY(-2px)";
        e.currentTarget.style.boxShadow = "0 10px 0 rgba(0,0,0,0.85)";
      }}
    >
      {label}
    </button>
  );
}

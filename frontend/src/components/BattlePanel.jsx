import React from "react";
import { TYPE_COLORS, DEFAULT_TYPE_STYLE } from "../constants/types";

export default function BattlePanel({
  log,
  mode = "main", // "main" | "moves" | "pokemon"
  moves = [], // array of move objects
  team = [], // array of pokemon objects (up to 6)
  activeIndex = 0,

  onFight,
  onPokemon,
  onBag,
  onRun,

  onBack,
  onPickMove, // (index) => void
  onPickPokemon, // (index) => void
}) {
  // Pokemon menu takes over the whole panel (no log)
  if (mode === "pokemon") {
    return (
      <div style={{ marginTop: 16 }}>
        <PokemonMenu
          team={team}
          activeIndex={activeIndex}
          onPickPokemon={onPickPokemon}
          onBack={onBack}
        />
      </div>
    );
  }

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

      {/* Right side */}
      {mode === "moves" ? (
        <MovesMenu moves={moves} onBack={onBack} onPickMove={onPickMove} />
      ) : (
        <MainMenu
          onFight={onFight}
          onPokemon={onPokemon}
          onBag={onBag}
          onRun={onRun}
        />
      )}
    </div>
  );
}

/* ------------------ MAIN MENU ------------------ */

function MainMenu({ onFight, onPokemon, onBag, onRun }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
      <MenuBtn label="FIGHT" bg="#e44848" onClick={onFight} />
      <MenuBtn label="POKEMON" bg="#25c05a" onClick={onPokemon} />
      <MenuBtn label="BAG" bg="#e1b200" onClick={onBag} />
      <MenuBtn label="RUN" bg="#3a7ff0" onClick={onRun} />
    </div>
  );
}

/* ------------------ MOVES MENU ------------------ */

function MovesMenu({ moves, onBack, onPickMove }) {
  return (
    <div style={{ display: "grid", gridTemplateRows: "1fr auto", gap: 12 }}>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        {[0, 1, 2, 3].map((i) => {
          const m = moves[i];
          return (
            <MoveBtn
              key={i}
              label={m ? formatMoveName(m.name) : "—"}
              type={m?.type}
              disabled={!m}
              onClick={() => m && onPickMove?.(i)}
            />
          );
        })}
      </div>

      <BackBtn label="BACK" onClick={onBack} />
    </div>
  );
}

/* ------------------ POKEMON MENU (FULL PANEL) ------------------ */

function PokemonMenu({ team, activeIndex, onPickPokemon, onBack }) {
  return (
    <div
      style={{
        borderRadius: 12,
        border: "3px solid rgba(0,0,0,0.85)",
        background: "rgba(0,0,0,0.20)",
        boxShadow: "0 10px 0 rgba(0,0,0,0.85)",
        padding: 9,
        display: "grid",
        gridTemplateColumns: "3fr 1fr", // 👈 grid + back button
        gap: 12,
      }}
    >
      {/* Pokémon grid (3x2) */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr 1fr", // 👈 3 columns
          gridTemplateRows: "1fr 1fr",        // 👈 2 rows
          gap: 12,
        }}
      >
        {[0, 1, 2, 3, 4, 5].map((i) => {
          const p = team[i];

          if (!p) {
            return (
              <PokemonSlot
                key={i}
                name="—"
                hpText=""
                isActive={false}
                disabled
                onClick={() => {}}
              />
            );
          }

          const pct = calcHpPct(p);
          const hpText = `HP: ${pct}%`;

          return (
            <PokemonSlot
              key={i}
              name={p.name}
              hpText={hpText}
              isActive={i === activeIndex}
              disabled={p.hp <= 0}
              onClick={() => onPickPokemon?.(i)}
            />
          );
        })}
      </div>

      {/* Back button on the right */}
      <BackBtn
        label="BACK"
        onClick={onBack}
        style={{ height: "100%" }}
      />
    </div>
  );
}


function PokemonSlot({ name, hpText, isActive, disabled, onClick }) {
  const base = {
    height: 92,
    borderRadius: 10,
    border: "3px solid rgba(0,0,0,0.85)",
    boxShadow: "0 8px 0 rgba(0,0,0,0.85)",
    background: "#f3f3f3",
    color: "#111",
    fontWeight: 900,
    cursor: disabled ? "not-allowed" : "pointer",
    opacity: disabled ? 0.55 : 1,
    display: "grid",
    placeItems: "center",
    textAlign: "center",
    padding: 10,
    transition: "transform 120ms ease, box-shadow 120ms ease",
    outline: isActive ? "4px solid rgba(0,0,0,0.35)" : "none",
  };

  return (
    <button
      style={base}
      disabled={disabled}
      onClick={onClick}
      onMouseEnter={(e) => {
        if (disabled) return;
        e.currentTarget.style.transform = "translateY(-2px)";
        e.currentTarget.style.boxShadow = "0 10px 0 rgba(0,0,0,0.85)";
      }}
      onMouseLeave={(e) => {
        if (disabled) return;
        e.currentTarget.style.transform = "translateY(0px)";
        e.currentTarget.style.boxShadow = "0 8px 0 rgba(0,0,0,0.85)";
      }}
      onMouseDown={(e) => {
        if (disabled) return;
        e.currentTarget.style.transform = "translateY(3px)";
        e.currentTarget.style.boxShadow = "0 4px 0 rgba(0,0,0,0.85)";
      }}
      onMouseUp={(e) => {
        if (disabled) return;
        e.currentTarget.style.transform = "translateY(-2px)";
        e.currentTarget.style.boxShadow = "0 10px 0 rgba(0,0,0,0.85)";
      }}
    >
      <div style={{ fontSize: 20, letterSpacing: 1 }}>{name}</div>
      <div style={{ fontSize: 14, opacity: 0.75, marginTop: 6 }}>{hpText}</div>
    </button>
  );
}

/* ------------------ BUTTONS ------------------ */

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

function MoveBtn({ label, type, disabled, onClick }) {
  const t = (type || "").toLowerCase();
  const style = TYPE_COLORS[t] || DEFAULT_TYPE_STYLE;

  const base = {
    height: 72,
    borderRadius: 10,
    border: "3px solid rgba(0,0,0,0.85)",
    boxShadow: "0 8px 0 rgba(0,0,0,0.85)",
    background: style.bg,
    color: style.text,
    fontWeight: 900,
    fontSize: 20,
    letterSpacing: 1,
    cursor: disabled ? "not-allowed" : "pointer",
    opacity: disabled ? 0.55 : 1,
    transition: "transform 120ms ease, box-shadow 120ms ease",
  };

  return (
    <button style={base} disabled={disabled} onClick={onClick}>
      {label}
    </button>
  );
}

function BackBtn({ label, onClick, style }) {
  const base = {
    width: "100%",
    height: 40,
    borderRadius: 10,
    border: "3px solid rgba(0,0,0,0.85)",
    boxShadow: "0 8px 0 rgba(0,0,0,0.85)",
    background: "#e9e9e9",
    color: "#111",
    fontWeight: 900,
    fontSize: 18,
    letterSpacing: 1,
    cursor: "pointer",
    transition: "transform 120ms ease, box-shadow 120ms ease",
    textTransform: "uppercase",
    ...style,
  };

  return (
    <button style={base} onClick={onClick}>
      {label}
    </button>
  );
}

/* ------------------ helpers ------------------ */

function formatMoveName(name = "") {
  return name.trim().replace(/\s+/g, "-");
}

function calcHpPct(p) {
  if (!p || !p.max_hp) return 0;
  const pct = (p.hp / p.max_hp) * 100;
  return Math.max(0, Math.min(100, Math.round(pct)));
}

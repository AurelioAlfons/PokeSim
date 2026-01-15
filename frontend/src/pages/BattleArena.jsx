// src/pages/BattleArena.jsx
import React, { useState } from "react";

export default function BattleArena() {
  const [log, setLog] = useState(["A wild Bidoof appeared!", "Go! Chimchar!"]);

  return (
    <div
      style={{
        marginTop: 25,
        display: "flex",
        justifyContent: "center",
        padding: "0 16px 40px",
      }}
    >
      <div style={{ width: "100%", maxWidth: 880 }}>
        {/* Arena Box */}
        <div
          style={{
            height: 580,
            borderRadius: 12,
            border: "4px solid rgba(0,0,0,0.9)",
            background:
              "linear-gradient(180deg, rgba(170,210,255,0.9), rgba(200,255,220,0.85))",
            position: "relative",
            overflow: "hidden",
            boxShadow: "0 10px 0 rgba(0,0,0,0.85)",
          }}
        >
          {/* Enemy HUD */}
          <div
            style={{
              position: "absolute",
              top: 18,
              left: 18,
              background: "rgba(255,255,255,0.95)",
              border: "2px solid rgba(0,0,0,0.85)",
              borderRadius: 10,
              padding: "10px 12px",
              width: 210,
              fontWeight: 900,
            }}
          >
            <div style={{ fontSize: 16 }}>Bidoof Lv.5</div>
            <div
              style={{
                marginTop: 8,
                height: 10,
                borderRadius: 999,
                background: "rgba(0,0,0,0.15)",
                overflow: "hidden",
              }}
            >
              <div style={{ width: "90%", height: "100%", background: "#e44848" }} />
            </div>
          </div>

          {/* Enemy sprite */}
          <div
            style={{
              position: "absolute",
              top: 110,
              right: 90,
              width: 200,
              height: 200,
              display: "grid",
              placeItems: "center",
              opacity: 0.98,
            }}
          >
            <img
              src="/assets/SVG/399.svg"
              alt="Bidoof"
              width={190}
              style={{
                imageRendering: "pixelated",
                transform: "scaleX(-1)", // face player
              }}
            />
          </div>

          {/* Player HUD */}
          <div
            style={{
              position: "absolute",
              bottom: 120,
              right: 18,
              background: "rgba(255,255,255,0.95)",
              border: "2px solid rgba(0,0,0,0.85)",
              borderRadius: 10,
              padding: "10px 12px",
              width: 220,
              fontWeight: 900,
              textAlign: "right",
            }}
          >
            <div style={{ fontSize: 16 }}>Chimchar Lv.5</div>
            <div
              style={{
                marginTop: 8,
                height: 10,
                borderRadius: 999,
                background: "rgba(0,0,0,0.15)",
                overflow: "hidden",
              }}
            >
              <div style={{ width: "100%", height: "100%", background: "#25c05a" }} />
            </div>
            <div style={{ marginTop: 6, fontSize: 14 }}>20/20</div>
          </div>

          {/* Player sprite */}
          <div
            style={{
              position: "absolute",
              bottom: 150,
              left: 100,
              width: 200,
              height: 200,
              display: "grid",
              placeItems: "center",
              opacity: 0.98,
            }}
          >
            <img
              src="/assets/SVG/390.svg"
              alt="Chimchar"
              width={190}
              style={{
                imageRendering: "pixelated",
              }}
            />
          </div>
        </div>

        {/* Bottom UI */}
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
            <MenuBtn
              label="FIGHT"
              bg="#e44848"
              onClick={() => setLog((p) => ["Chimchar used Scratch!", ...p])}
            />
            <MenuBtn
              label="POKEMON"
              bg="#25c05a"
              onClick={() => setLog((p) => ["Choose a Pokémon.", ...p])}
            />
            <MenuBtn
              label="BAG"
              bg="#e1b200"
              onClick={() => setLog((p) => ["Opened the bag.", ...p])}
            />
            <MenuBtn
              label="RUN"
              bg="#3a7ff0"
              onClick={() => setLog((p) => ["Got away safely!", ...p])}
            />
          </div>
        </div>
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

// src/pages/BattleArena.jsx
import React, { useEffect, useState } from "react";

export default function BattleArena() {
  const [log, setLog] = useState(["Loading battle..."]);
  const [player, setPlayer] = useState(null);
  const [enemy, setEnemy] = useState(null);

  useEffect(() => {
    const start = async () => {
      try {
        const res = await fetch("http://127.0.0.1:5000/battle/start", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });

        if (!res.ok) throw new Error("Battle start failed");

        const data = await res.json();

        setPlayer(data.player);
        setEnemy(data.enemy);
        setLog(data.log || []);
      } catch (err) {
        setLog([
          "Could not connect to backend.",
          "Make sure FastAPI is running on http://127.0.0.1:5000",
        ]);
      }
    };

    start();
  }, []);

  const hpPct = (p) => {
    if (!p) return "0%";
    const pct = (p.hp / p.max_hp) * 100;
    return `${Math.max(0, Math.min(100, pct))}%`;
  };

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
              width: 240,
              fontWeight: 900,
            }}
          >
            <div style={{ fontSize: 16 }}>
              {enemy ? `${enemy.name} Lv.${enemy.level}` : "Enemy..."}
            </div>

            <div
              style={{
                marginTop: 8,
                height: 10,
                borderRadius: 999,
                background: "rgba(0,0,0,0.15)",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: hpPct(enemy),
                  height: "100%",
                  background: "#e44848",
                }}
              />
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
            {enemy ? (
              <img
                src={enemy.sprite}
                alt={enemy.name}
                width={190}
                style={{
                  imageRendering: "pixelated",
                  transform: "scaleX(-1)",
                }}
              />
            ) : (
              <div style={{ fontWeight: 900 }}>(Loading...)</div>
            )}
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
              width: 240,
              fontWeight: 900,
              textAlign: "right",
            }}
          >
            <div style={{ fontSize: 16 }}>
              {player ? `${player.name} Lv.${player.level}` : "Player..."}
            </div>

            <div
              style={{
                marginTop: 8,
                height: 10,
                borderRadius: 999,
                background: "rgba(0,0,0,0.15)",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: hpPct(player),
                  height: "100%",
                  background: "#25c05a",
                }}
              />
            </div>

            <div style={{ marginTop: 6, fontSize: 14 }}>
              {player ? `${player.hp}/${player.max_hp}` : ""}
            </div>
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
            {player ? (
              <img
                src={player.sprite}
                alt={player.name}
                width={190}
                style={{ imageRendering: "pixelated" }}
              />
            ) : (
              <div style={{ fontWeight: 900 }}>(Loading...)</div>
            )}
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
              <div
                key={i}
                style={{ marginBottom: 6, opacity: i === 0 ? 1 : 0.85 }}
              >
                {l}
              </div>
            ))}
          </div>

          {/* Menu buttons (still placeholder actions) */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            <MenuBtn
              label="FIGHT"
              bg="#e44848"
              onClick={() => setLog((p) => ["(Next) Open move menu", ...p])}
            />
            <MenuBtn
              label="POKEMON"
              bg="#25c05a"
              onClick={() => setLog((p) => ["(Next) Show team list", ...p])}
            />
            <MenuBtn
              label="BAG"
              bg="#e1b200"
              onClick={() => setLog((p) => ["(Next) Bag items", ...p])}
            />
            <MenuBtn
              label="RUN"
              bg="#3a7ff0"
              onClick={() => setLog((p) => ["(Next) Run attempt", ...p])}
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

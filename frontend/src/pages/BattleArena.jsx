// src/pages/BattleArena.jsx
import React, { useEffect, useState } from "react";
import BattlePanel from "../components/BattlePanel";

export default function BattleArena() {
  const [log, setLog] = useState(["Loading battle..."]);
  const [player, setPlayer] = useState(null);
  const [enemy, setEnemy] = useState(null);
  const [team, setTeam] = useState([]); // ✅ NEW
  const [panelMode, setPanelMode] = useState("main"); // main | moves | pokemon

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
        setTeam(data.team?.pokemon || []); // ✅ NEW (this is the real team)
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

  // Moves for the current player pokemon (based on your current API shape)
  const moves = player?.moves || [];

  // ✅ We now use the real team from API (data.team.pokemon)
  const activeIndex = 0; // Chimchar is slot 0 for now

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
            backgroundImage: "url('/assets/backgrounds/1.jpg')",
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
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

        {/* Bottom Panel */}
        <BattlePanel
          log={log}
          mode={panelMode}
          moves={moves}
          team={team}                 // ✅ now real team from API
          activeIndex={activeIndex}   // ✅ fixed index for now
          onFight={() => setPanelMode("moves")}
          onPokemon={() => setPanelMode("pokemon")}
          onBack={() => setPanelMode("main")}
          onPickMove={(i) => {
            const chosen = moves[i];
            if (!chosen) return;

            setLog((p) => [
              `${player?.name || "Pokemon"} used ${chosen.name}!`,
              ...p,
            ]);

            setPanelMode("main");
          }}
          onPickPokemon={(i) => {
            const picked = team[i];
            if (!picked) return;

            setLog((p) => [`(Soon) Switch to ${picked.name}`, ...p]);
            setPanelMode("main");
          }}
          onBag={() => setLog((p) => ["(Next) Bag items", ...p])}
          onRun={() => setLog((p) => ["(Next) Run attempt", ...p])}
        />
      </div>
    </div>
  );
}

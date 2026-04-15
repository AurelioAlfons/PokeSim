// src/pages/BattleArena.jsx
import React, { useEffect, useState } from "react";
import BattlePanel from "../components/BattlePanel";
import PokemonSprite from "../components/PokemonSprite";

export default function BattleArena() {
  const API_URL = process.env.REACT_APP_API_URL;

  const [log, setLog] = useState(["Loading battle..."]);
  const [player, setPlayer] = useState(null);
  const [enemy, setEnemy] = useState(null);
  const [team, setTeam] = useState([]);
  const [activeIndex, setActiveIndex] = useState(0);
  const [panelMode, setPanelMode] = useState("main"); // main | moves | pokemon
  const [forceSwitch, setForceSwitch] = useState(false);

  useEffect(() => {
    const start = async () => {
      try {
        const res = await fetch(`${API_URL}/battle/start`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });

        if (!res.ok) throw new Error("Battle start failed");

        const data = await res.json();
        setPlayer(data.player);
        setEnemy(data.enemy);
        setLog(data.log || []);
        setTeam(data.team?.pokemon || []);
        setActiveIndex(data.active_index ?? 0);
        setForceSwitch(false);
        setPanelMode("main");
      } catch (err) {
        setLog([
          "Could not connect to backend.",
          `Make sure backend is running at ${API_URL}`,
        ]);
      }
    };

    start();
  }, [API_URL]);

  const hpPct = (p) => {
    if (!p) return "0%";
    const pct = (p.hp / p.max_hp) * 100;
    return `${Math.max(0, Math.min(100, pct))}%`;
  };

  const expPct = (p) => {
    if (!p || !p.exp_to_next_level) return "0%";
    const pct = (p.exp / p.exp_to_next_level) * 100;
    return `${Math.max(0, Math.min(100, pct))}%`;
  };

  const moves = player?.moves || [];

  const doRun = async () => {
    try {
      const res = await fetch(`${API_URL}/battle/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });

      if (!res.ok) throw new Error("Run failed");
      const data = await res.json();

      setPlayer(data.player);
      setEnemy(data.enemy);
      setTeam(data.team?.pokemon || []);
      setActiveIndex(data.active_index ?? 0);

      if (data.log?.length) setLog((p) => [...data.log, ...p]);

      setForceSwitch(false);
      setPanelMode("main");
    } catch (e) {
      setLog((p) => ["Could not run (backend not reachable).", ...p]);
    }
  };

  const switchTo = async (index) => {
    try {
      const res = await fetch(`${API_URL}/battle/switch`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ index }),
      });

      if (!res.ok) throw new Error("Switch failed");
      const data = await res.json();

      setPlayer(data.player);
      setEnemy(data.enemy);
      setTeam(data.team?.pokemon || []);
      setActiveIndex(data.active_index ?? 0);

      if (data.log?.length) setLog((p) => [...data.log, ...p]);

      setForceSwitch(false);
      setPanelMode("main");
    } catch (e) {
      setLog((p) => ["Could not switch Pokemon (backend not reachable).", ...p]);
      setPanelMode("main");
    }
  };

  const doMove = async (index) => {
    try {
      const res = await fetch(`${API_URL}/battle/move`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ index }),
      });

      if (!res.ok) throw new Error("Move failed");
      const data = await res.json();

      setPlayer(data.player);
      setEnemy(data.enemy);
      setTeam(data.team?.pokemon || []);
      setActiveIndex(data.active_index ?? 0);

      if (data.log?.length) setLog((p) => [...data.log, ...p]);

      if (data.message === "Active Pokémon fainted.") {
        setForceSwitch(true);
        setPanelMode("pokemon");
        return;
      }

      setPanelMode("main");
    } catch (e) {
      setLog((p) => ["Could not use move (backend not reachable).", ...p]);
      setPanelMode("main");
    }
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

          <div style={{ position: "absolute", top: 110, right: 90 }}>
            <PokemonSprite
              src={enemy?.sprite}
              alt={enemy?.name || "Enemy"}
              size={210}
              flip={true}
            />
          </div>

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

            <div
              style={{
                marginTop: 6,
                height: 6,
                borderRadius: 999,
                background: "rgba(0,0,0,0.15)",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: expPct(player),
                  height: "100%",
                  background: "#4aa3ff",
                }}
              />
            </div>

            <div style={{ marginTop: 6, fontSize: 14 }}>
              {player ? `${player.hp}/${player.max_hp}` : ""}
            </div>
          </div>

          <div style={{ position: "absolute", bottom: 150, left: 100 }}>
            <PokemonSprite
              src={player?.sprite}
              alt={player?.name || "Player"}
              size={220}
              flip={false}
            />
          </div>
        </div>

        <BattlePanel
          log={log}
          mode={panelMode}
          moves={moves}
          team={team}
          activeIndex={activeIndex}
          onFight={() => (forceSwitch ? null : setPanelMode("moves"))}
          onPokemon={() => setPanelMode("pokemon")}
          onBack={() => setPanelMode("main")}
          onPickMove={(i) => doMove(i)}
          onPickPokemon={(i) => switchTo(i)}
          onBag={() => setLog((p) => ["(Next) Bag items", ...p])}
          onRun={() => doRun()}
        />
      </div>
    </div>
  );
}
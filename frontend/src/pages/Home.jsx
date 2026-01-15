// src/pages/Home.jsx
import React, { useState, useEffect, useRef } from "react";
import TeamHeader from "../components/TeamHeader";

export default function Home() {
  // ✅ divider logic
  const dividerRef = useRef(null);
  const [splitX, setSplitX] = useState("50%");

  useEffect(() => {
    const updateSplit = () => {
      if (!dividerRef.current) return;

      const rect = dividerRef.current.getBoundingClientRect();

      // y position of divider in the viewport
      const APP_TOP_PADDING = -15;
      const y = rect.top - APP_TOP_PADDING;

      const W = window.innerWidth;
      const H = window.innerHeight;

      // where the diagonal boundary is (in viewport coordinates)
      const boundaryX = (W + H) / 2 - y;

      // convert boundaryX into divider-local coordinates
      const localX = boundaryX - rect.left;

      // turn it into a % of the divider's own width
      const pct = Math.max(0, Math.min(100, (localX / rect.width) * 100));

      setSplitX(`${pct}%`);
    };

    updateSplit();
    window.addEventListener("resize", updateSplit);
    window.addEventListener("scroll", updateSplit, { passive: true });

    return () => {
      window.removeEventListener("resize", updateSplit);
      window.removeEventListener("scroll", updateSplit);
    };
  }, []);

  // ✅ header state
  const [teamName, setTeamName] = useState("");
  const [description, setDescription] = useState("");

  return (
    <div
      style={{
        marginTop: 25,
        padding: "0 20px",
      }}
    >
      {/* Top header */}
      <TeamHeader
        teamName={teamName}
        onTeamNameChange={setTeamName}
        description={description}
        onDescriptionChange={setDescription}
        onCancel={() => {
          setTeamName("");
          setDescription("");
        }}
        onSave={() => console.log("Save team:", { teamName, description })}
      />

      {/* Adaptive Divider */}
      <div
        ref={dividerRef}
        style={{
          marginTop: 20,
          height: 3,
          width: "100%",
          // position: "relative",
          // left: "50%",
          // transform: "translateX(-50%)",
          background: `linear-gradient(
            90deg,
            #f7e733 ${splitX},
            #111 ${splitX}
          )`,
        }}
      />

      {/* Main content */}
      <div
        style={{
          marginTop: 30,
          display: "flex",
          gap: 40,
          alignItems: "flex-start",
        }}
      >
        {/* Left: Add Pokémon area */}
        <div
          style={{
            flex: 1,
            maxWidth: 520,
            border: "2px dashed #cfcfcf",
            borderRadius: 12,
            height: 220,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#999",
            fontWeight: 600,
          }}
        >
          + Add Pokémon
        </div>

        {/* Right: Team stats */}
        <div
          style={{
            width: 360,
            border: "2px solid black",
            borderRadius: 12,
            padding: 20,
          }}
        >
          <div
            style={{
              fontSize: 22,
              fontWeight: 800,
              color: "#e53935",
              marginBottom: 12,
            }}
          >
            Team Stats
          </div>

          <div style={{ marginBottom: 12 }}>Members: 0 / 6</div>

          <div
            style={{
              background: "#eef5ff",
              border: "1px solid #c6dbff",
              borderRadius: 6,
              padding: 12,
              fontSize: 14,
            }}
          >
            <strong>Tip:</strong>
            <br />
            A balanced team needs both Physical and Special attackers, plus
            defensive pivots!
          </div>
        </div>
      </div>
    </div>
  );
}

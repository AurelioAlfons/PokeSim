// src/pages/Home.jsx
import React, { useState } from "react";
import TeamHeader from "../components/TeamHeader";

export default function Home() {
  const [description, setDescription] = useState("");

  return (
    <div
      style={{
        marginTop: 40,
        padding: "0 20px",
      }}
    >
      {/* Top header */}
      <TeamHeader
        description={description}
        onDescriptionChange={setDescription}
        onCancel={() => setDescription("")}
        onSave={() => console.log("Save team:", description)}
      />

      {/* Divider */}
      <div
        style={{
          marginTop: 20,
          borderBottom: "3px solid black",
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

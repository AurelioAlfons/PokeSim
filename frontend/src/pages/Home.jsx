// src/pages/Home.jsx
import React from "react";

export default function Home() {
  return (
    <div
      style={{
        marginTop: 40,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          background: "rgba(255, 255, 255, 0.25)",     // stronger white
          backdropFilter: "blur(18px) saturate(150%)", // MUCH clearer glass
          WebkitBackdropFilter: "blur(18px) saturate(150%)",
          padding: "40px 60px",
          borderRadius: 20,
          border: "1px solid rgba(255,255,255,0.45)", // stronger border
          color: "white",
          fontSize: 26,
          fontWeight: 600,
          textAlign: "center",
          width: "90%",
          maxWidth: "10000px",
          height: "500px",
          maxHeight: "800px",

          // adds separation from background
          boxShadow: "0 8px 30px rgba(0,0,0,0.2)",
        }}
      >
        Welcome to Poké Simulator
        <br />
        <span style={{ fontSize: 18, opacity: 0.9 }}>
          Ad Astra
        </span>
      </div>
    </div>
  );
}

// src/pages/Challenge.jsx
import React from "react";

export default function Challenge() {
  return (
    <div
      style={{
        marginTop: 80,
        display: "flex",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          maxWidth: 600,
          padding: 32,
          borderRadius: 24,
          background: "rgba(255,255,255,0.12)",
          border: "1px solid rgba(255,255,255,0.2)",
          backdropFilter: "blur(18px)",
          color: "#fff",
        }}
      >
        <h1 style={{ margin: 0, marginBottom: 12 }}>Challenge Mode</h1>
        <p style={{ margin: 0, opacity: 0.8 }}>
          Battle simulations will go here later.
        </p>
      </div>
    </div>
  );
}

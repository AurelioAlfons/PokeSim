// src/components/Navbar.jsx
import React from "react";

export default function Navbar() {
  const linkStyle = {
    padding: "6px 18px",
    borderRadius: 9999,
    border: "1px solid transparent",
    backgroundColor: "transparent",
    fontSize: 12,
    fontWeight: 500,
    letterSpacing: "0.08em",
    textTransform: "uppercase",
    cursor: "pointer",
  };

  return (
    <div
      style={{
        width: "100%",
        maxWidth: 1400,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        margin: "0 auto",
        paddingTop: 20,
        position: "relative",
      }}
    >

      {/* LEFT SIDE — logo + title (OUTSIDE the navbar pill) */}
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <img
          src="/assets/SVG/387.svg"
          alt="logo"
          style={{ width: 60, height: 60 }}
        />
        <span style={{ fontWeight: 700, fontSize: 18, color: "#ffffffff" }}>Poké Simulator</span>
      </div>

      {/* CENTER — actual pill-shaped navbar */}
      <div
        style={{
          position: "absolute",
          left: "50%",
          transform: "translateX(-50%)",
          display: "flex",
          alignItems: "center",
          gap: 12,
          padding: "10px 24px",
          borderRadius: 9999,
          backgroundColor: "#ffffff",
          border: "1px solid #eee",
          boxShadow: "0 12px 30px rgba(0,0,0,0.06)",
        }}
      >
        <button style={linkStyle}>Builder</button>
        <button style={linkStyle}>Challenge</button>
      </div>

      {/* RIGHT SIDE — empty for balance (future Log In, etc.) */}
      <div style={{ width: 80 }}></div>

    </div>
  );
}

// src/components/Navbar.jsx
import React from "react";
import { useNavigate, useLocation } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [hovered, setHovered] = React.useState(null);

  const baseLinkStyle = {
    padding: "6px 18px",
    borderRadius: 9999,
    border: "1px solid transparent",
    backgroundColor: "transparent",
    fontSize: 12,
    fontWeight: 500,
    letterSpacing: "0.08em",
    textTransform: "uppercase",
    cursor: "pointer",
    transition: "background-color 0.18s ease, color 0.18s ease",
  };

  const getButtonStyle = (name, isActive) => {
    const isHovered = hovered === name;
    const activeOrHover = isHovered || isActive;

    return {
      ...baseLinkStyle,
      backgroundColor: activeOrHover ? "#f7e733" : "transparent",
      color: activeOrHover ? "#ffffff" : "#333333",
    };
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
      {/* LEFT SIDE — logo + title */}
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <img
          src="/assets/SVG/398.svg"
          alt="logo"
          style={{ width: 60, height: 60 }}
        />
        <span
          style={{
            fontWeight: 700,
            fontSize: 18,
            color: "#ffffffff",
          }}
        >
          Poké Simulator
        </span>
      </div>

      {/* CENTER — pill navbar */}
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
        <button
          style={getButtonStyle("builder", location.pathname === "/")}
          onClick={() => navigate("/")}
          onMouseEnter={() => setHovered("builder")}
          onMouseLeave={() => setHovered(null)}
        >
          Builder
        </button>

        <button
          style={getButtonStyle("challenge", location.pathname === "/challenge")}
          onClick={() => navigate("/challenge")}
          onMouseEnter={() => setHovered("challenge")}
          onMouseLeave={() => setHovered(null)}
        >
          Challenge
        </button>
      </div>

      {/* RIGHT — user avatar */}
      <div
        style={{
          width: 46,
          height: 46,
          borderRadius: "50%",
          overflow: "hidden",
          backgroundColor: "#ffffff",
          boxShadow: "0 6px 18px rgba(0,0,0,0.14)",
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <img
          src="/assets/SVG/445.svg"
          alt="user"
          style={{ width: "100%", height: "100%", borderRadius: "50%" }}
        />
      </div>
    </div>
  );
}

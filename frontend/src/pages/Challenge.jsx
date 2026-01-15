// src/pages/Challenge.jsx
import React, { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Challenge() {
  const [selectedTeam, setSelectedTeam] = useState(null);
  const canStart = !!selectedTeam;
  const navigate = useNavigate();

  const teams = useMemo(
    () => [
      {
        id: "sample",
        name: "Sample Team (Sample)",
        members: "chimchar, bidoof, starly",
      },
    ],
    []
  );

  const cardStyle = {
    maxWidth: 680,
    width: "100%",
    padding: 34,
    borderRadius: 18,
    border: "3px solid rgba(0,0,0,0.85)",
    boxShadow: "0 10px 0 rgba(0,0,0,0.85)",
    color: "#111",
  };

  const startBtnBase = {
    width: "100%",
    marginTop: 22,
    padding: "14px 16px",
    borderRadius: 10,
    border: "3px solid rgba(0,0,0,0.85)",
    boxShadow: "0 6px 0 rgba(0,0,0,0.85)",
    fontWeight: 900,
    letterSpacing: 1,
    fontSize: 18,
    transition: "transform 120ms ease, box-shadow 120ms ease, filter 120ms ease",
  };

  const onStart = () => {
    if (!canStart) return;
    navigate("/battle");
  };

  return (
    <div
      style={{
        marginTop: 25,
        display: "flex",
        justifyContent: "center",
        padding: "0 16px",
      }}
    >
      <div style={cardStyle}>
        <h1
          style={{
            margin: 0,
            marginBottom: 18,
            textAlign: "center",
            color: "#e44848",
            fontSize: 44,
            fontWeight: 900,
            letterSpacing: 2,
            textShadow: "0 3px 0 rgba(0,0,0,0.35)",
          }}
        >
          Select Your Team
        </h1>

        {/* Team options (only 1 for now) */}
        <div style={{ display: "grid", gap: 14 }}>
          {teams.map((t) => {
            const isSelected = selectedTeam === t.id;

            const teamStyle = {
              background: "rgba(255,255,255,0.95)",
              borderRadius: 14,
              padding: 18,
              cursor: "pointer",
              userSelect: "none",
              border: isSelected
                ? "2px solid #ff3b3b"
                : "2px solid rgba(0,0,0,0.25)",
              boxShadow: isSelected
                ? "0 0 0 4px rgba(255,59,59,0.45)"
                : "none",
              transition: "all 120ms ease",
            };

            return (
              <div
                key={t.id}
                onClick={() => setSelectedTeam(t.id)}
                style={teamStyle}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-2px)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "translateY(0)";
                }}
              >
                <div style={{ fontSize: 20, fontWeight: 900 }}>{t.name}</div>
                <div style={{ marginTop: 6, fontSize: 14, opacity: 0.75 }}>
                  {t.members}
                </div>
              </div>
            );
          })}
        </div>

        {/* Start button (locked until selection) */}
        <button
          onClick={onStart}
          disabled={!canStart}
          style={{
            ...startBtnBase,
            background: canStart ? "#e44848" : "rgba(228,72,72,0.35)",
            color: canStart ? "#fff" : "rgba(255,255,255,0.75)",
            cursor: canStart ? "pointer" : "not-allowed",
            filter: canStart ? "none" : "grayscale(35%)",
            boxShadow: canStart
              ? "0 6px 0 rgba(0,0,0,0.85)"
              : "0 6px 0 rgba(0,0,0,0.45)",
            border: canStart
              ? "3px solid rgba(0,0,0,0.85)"
              : "3px solid rgba(0,0,0,0.45)",
          }}
          onMouseEnter={(e) => {
            if (!canStart) return;
            e.currentTarget.style.transform = "translateY(-2px)";
            e.currentTarget.style.boxShadow = "0 8px 0 rgba(0,0,0,0.85)";
          }}
          onMouseLeave={(e) => {
            if (!canStart) return;
            e.currentTarget.style.transform = "translateY(0px)";
            e.currentTarget.style.boxShadow = "0 6px 0 rgba(0,0,0,0.85)";
          }}
          onMouseDown={(e) => {
            if (!canStart) return;
            e.currentTarget.style.transform = "translateY(2px)";
            e.currentTarget.style.boxShadow = "0 3px 0 rgba(0,0,0,0.85)";
          }}
          onMouseUp={(e) => {
            if (!canStart) return;
            e.currentTarget.style.transform = "translateY(-2px)";
            e.currentTarget.style.boxShadow = "0 8px 0 rgba(0,0,0,0.85)";
          }}
        >
          Start Battle!
        </button>
      </div>
    </div>
  );
}

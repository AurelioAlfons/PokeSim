// src/components/TypeBadge.jsx
import React from "react";
import { TYPE_COLORS, DEFAULT_TYPE_STYLE } from "../constants/types";

export default function TypeBadge({ type, size = "md" }) {
  const t = (type || "").toLowerCase();
  const style = TYPE_COLORS[t] || DEFAULT_TYPE_STYLE;
  const small = size === "sm";

  return (
    <span
      style={{
        display: "inline-block",
        background: style.bg,
        color: style.text,
        border: "2px solid rgba(0,0,0,0.85)",
        borderRadius: 6,
        padding: small ? "1px 8px" : "3px 10px",
        fontSize: small ? 11 : 13,
        fontWeight: 800,
        letterSpacing: 0.5,
        textTransform: "uppercase",
      }}
    >
      {t}
    </span>
  );
}

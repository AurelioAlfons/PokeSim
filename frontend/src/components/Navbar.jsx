import React, { useEffect, useRef, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();

  const isBuilder = location.pathname === "/" || location.pathname === "/builder";
  const isBattle =
    location.pathname === "/battle" || location.pathname === "/challenge";

  // ---- divider logic ----
  const dividerRef = useRef(null);
  const [splitX, setSplitX] = useState("50%");

  useEffect(() => {
    const updateSplit = () => {
      if (!dividerRef.current) return;

      const rect = dividerRef.current.getBoundingClientRect();
      const APP_TOP_PADDING = -10;
      const y = rect.top - APP_TOP_PADDING;

      const W = window.innerWidth;
      const H = window.innerHeight;

      const x = (W + H) / 2 - y;
      const pct = Math.max(0, Math.min(100, (x / W) * 100));
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

  // ---- hover invert helpers ----
  const invertHoverOn = (e) => {
    const el = e.currentTarget;
    const bg = el.style.background;
    const color = el.style.color;
    el.style.background = color;
    el.style.color = bg;
  };

  const invertHoverOff = (e, active) => {
    const el = e.currentTarget;
    if (active) {
      el.style.background = "#f7e733";
      el.style.color = "#111";
    } else {
      el.style.background = "#111";
      el.style.color = "#f7e733";
    }
  };

  const styles = {
    bar: {
      width: "100%",
      background: "transparent",
    },

    inner: {
      maxWidth: 1400,
      margin: "0 auto",
      padding: "16px 24px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      position: "relative",
    },

    left: {
      display: "flex",
      alignItems: "center",
      gap: 10,
      cursor: "pointer",
    },

    brand: {
      fontWeight: 800,
      fontSize: 27,
      color: "#f7e733",
    },

    center: {
      position: "absolute",
      left: "50%",
      transform: "translateX(-50%)",
      display: "flex",
      gap: 14,
    },

    tab: (active) => ({
      display: "flex",
      alignItems: "center",
      gap: 10,
      padding: "10px 18px",
      borderRadius: 8,
      border: "2px solid #111",
      background: active ? "#f7e733" : "#111",
      color: active ? "#111" : "#f7e733",
      fontWeight: 800,
      fontSize: 20,
      cursor: "pointer",
      transition: "all 0.15s ease",
      outline: "none",
    }),

    iconBox: {
      width: 30,
      height: 32,
      display: "grid",
      placeItems: "center",
    },

    loginBtn: {
      padding: "10px 22px",
      borderRadius: 8,
      border: "2px solid #111",
      background: "#f7e733",
      color: "#111",
      fontWeight: 800,
      fontSize: 20,
      cursor: "pointer",
      transition: "all 0.15s ease",
    },

    divider: {
      position: "relative",
      left: "50%",
      width: "100vw",
      transform: "translateX(-50%)",
      height: "2px",
      marginTop: 10,
      background: `linear-gradient(
        90deg,
        #f7e733 ${splitX},
        #111 ${splitX}
      )`,
    },
  };

  const TabIcon = ({ type }) => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
      {type === "builder" ? (
        <path
          d="M4 4h7v7H4V4Zm9 0h7v7h-7V4ZM4 13h7v7H4v-7Zm9 0h7v7h-7v-7Z"
          stroke="currentColor"
          strokeWidth="2"
        />
      ) : (
        <path
          d="M4 20l6-6 3 3-6 6H4v-3Zm7.5-9.5L19 3l2 2-7.5 7.5-2-2Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinejoin="round"
        />
      )}
    </svg>
  );

  return (
    <div style={styles.bar}>
      <div style={styles.inner}>
        {/* LEFT */}
        <div style={styles.left} onClick={() => navigate("/")}>
          <img src="/assets/SVG/398.svg" alt="logo" width={42} />
          <span style={styles.brand}>PokeSim</span>
        </div>

        {/* CENTER */}
        <div style={styles.center}>
          <button
            style={styles.tab(isBuilder)}
            onClick={() => navigate("/")}
            onMouseEnter={invertHoverOn}
            onMouseLeave={(e) => invertHoverOff(e, isBuilder)}
          >
            <span style={styles.iconBox}>
              <TabIcon type="builder" />
            </span>
            Builder
          </button>

          <button
            style={styles.tab(isBattle)}
            onClick={() => navigate("/challenge")}
            onMouseEnter={invertHoverOn}
            onMouseLeave={(e) => invertHoverOff(e, isBattle)}
          >
            <span style={styles.iconBox}>
              <TabIcon type="battle" />
            </span>
            Battle
          </button>
        </div>

        {/* RIGHT */}
        <button
          style={styles.loginBtn}
          onClick={() => navigate("/login")}
          onMouseEnter={invertHoverOn}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = "#f7e733";
            e.currentTarget.style.color = "#111";
          }}
        >
          Login
        </button>
      </div>

      {/* DIVIDER */}
      <div ref={dividerRef} style={styles.divider} />
    </div>
  );
}

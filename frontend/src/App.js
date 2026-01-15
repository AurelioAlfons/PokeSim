// src/App.js
import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Challenge from "./pages/Challenge";
import BattleArena from "./pages/BattleArena";

function App() {
  const angle = "135deg";
  const dark = "#1c1c1c";
  const yellow = "#f7e733";
  const split = "50%";

  // App padding (keep as numbers so we can reuse them cleanly)
  const padTop = 20;
  const padX = 40;
  const padBottom = 40;

  return (
    <div
      style={{
        minHeight: "100vh",

        // shared variables for whole app
        "--bg-angle": angle,
        "--bg-dark": dark,
        "--bg-yellow": yellow,
        "--bg-split": split,

        // shared padding vars (IMPORTANT for divider math)
        "--app-pad-top": `${padTop}px`,
        "--app-pad-x": `${padX}px`,
        "--app-pad-bottom": `${padBottom}px`,

        background:
          "linear-gradient(var(--bg-angle), var(--bg-dark) var(--bg-split), var(--bg-yellow) var(--bg-split))",
        backgroundAttachment: "fixed",

        padding: `${padTop}px ${padX}px ${padBottom}px`,
      }}
    >
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/challenge" element={<Challenge />} />
        <Route path="/battle" element={<BattleArena />} />
      </Routes>
    </div>
  );
}

export default App;

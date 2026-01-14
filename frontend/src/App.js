// src/App.js
import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Challenge from "./pages/Challenge";

function App() {
  const angle = "135deg";
  const dark = "#1c1c1c";
  const yellow = "#f7e733";
  const split = "50%";

  return (
    <div
      style={{
        minHeight: "100vh",

        // shared variables for whole app
        "--bg-angle": angle,
        "--bg-dark": dark,
        "--bg-yellow": yellow,
        "--bg-split": split,

        background:
          "linear-gradient(var(--bg-angle), var(--bg-dark) var(--bg-split), var(--bg-yellow) var(--bg-split))",
        backgroundAttachment: "fixed",

        padding: "20px 40px 40px",
      }}
    >
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/challenge" element={<Challenge />} />
      </Routes>
    </div>
  );
}

export default App;

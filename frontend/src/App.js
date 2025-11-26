// src/App.js
import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Challenge from "./pages/Challenge";

function App() {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: `
          linear-gradient(
            135deg,
            #1c1c1c 50%,
            #f7e733 50%
          )
        `,
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

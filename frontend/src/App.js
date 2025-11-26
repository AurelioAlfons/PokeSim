// src/App.js
import React from "react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";

function App() {
  return (
    <div style={{ position: "relative", minHeight: "100vh" }}>
      
      {/* --- BLURRED BACKGROUND LAYER --- */}
      <div
        style={{
          position: "absolute",
          top: -20,
          left: -20,
          right: -20,
          bottom: -20,
          background: `
            linear-gradient(
              135deg,
              #1c1c1c 50%,
              #f7e733 90%
            )
          `,
          filter: "blur(6px)",         // <--- adjust blur amount here
          zIndex: 1,
        }}
      ></div>

      {/* --- MAIN CONTENT (not blurred) --- */}
      <div
        style={{
          position: "relative",
          zIndex: 2,
          padding: "20px 40px 40px",
        }}
      >
        <Navbar />
        <Home />
      </div>
    </div>
  );
}

export default App;

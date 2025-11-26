// src/App.js
import React from "react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";

function App() {
  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#f9f5ef", // soft beige like the example
        padding: "20px 40px 40px",
      }}
    >
      <Navbar />
      <Home />
    </div>
  );
}

export default App;

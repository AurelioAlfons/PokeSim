// src/pages/Login.jsx
import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // supabase hands back the error on the response, doesn't throw
    const { error: authError } = await login(email, password);
    setLoading(false);

    if (authError) {
      setError(authError.message);
      return;
    }
    navigate("/");
  };

  return (
    <div style={styles.wrap}>
      <form style={styles.card} onSubmit={handleSubmit}>
        <div style={styles.title}>Log In</div>

        {error && <div style={styles.error}>{error}</div>}

        <label style={styles.label}>Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={styles.input}
          required
        />

        <label style={styles.label}>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
          required
        />

        <button type="submit" style={styles.submitBtn} disabled={loading}>
          {loading ? "Logging in..." : "Log In"}
        </button>

        <div style={styles.links}>
          <Link to="/forgot-password" style={styles.link}>
            Forgot password?
          </Link>
          <Link to="/signup" style={styles.link}>
            Need an account? Sign up
          </Link>
        </div>
      </form>
    </div>
  );
}

const styles = {
  wrap: {
    display: "flex",
    justifyContent: "center",
    marginTop: 60,
  },
  card: {
    width: "100%",
    maxWidth: 400,
    background: "#fff",
    borderRadius: 16,
    border: "3px solid rgba(0,0,0,0.85)",
    boxShadow: "0 12px 0 rgba(0,0,0,0.85)",
    padding: 28,
    display: "flex",
    flexDirection: "column",
    gap: 6,
  },
  title: {
    fontSize: 24,
    fontWeight: 900,
    marginBottom: 10,
  },
  error: {
    background: "#fbe4e4",
    border: "2px solid #a11d1d",
    color: "#a11d1d",
    borderRadius: 8,
    padding: "8px 12px",
    fontSize: 13,
    fontWeight: 700,
    marginBottom: 8,
  },
  label: {
    fontWeight: 800,
    fontSize: 13,
    color: "#333",
    marginTop: 8,
  },
  input: {
    height: 40,
    borderRadius: 8,
    border: "2px solid #ddd",
    padding: "0 12px",
    outline: "none",
    fontSize: 14,
  },
  submitBtn: {
    height: 44,
    marginTop: 18,
    borderRadius: 8,
    border: "2px solid #111",
    background: "#ff2d2d",
    color: "#000",
    fontWeight: 800,
    fontSize: 15,
    cursor: "pointer",
    boxShadow: "3px 3px 0 rgba(0,0,0,0.25)",
  },
  links: {
    display: "flex",
    justifyContent: "space-between",
    marginTop: 16,
    fontSize: 13,
  },
  link: {
    color: "#333",
    fontWeight: 700,
    textDecoration: "underline",
  },
};

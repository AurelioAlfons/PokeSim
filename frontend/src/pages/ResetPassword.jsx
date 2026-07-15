// src/pages/ResetPassword.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ResetPassword() {
  const { updatePassword } = useAuth();
  const navigate = useNavigate();

  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (password !== confirm) {
      setError("Passwords don't match.");
      return;
    }

    setLoading(true);
    // the reset-link click already logged this browser into a temporary
    // recovery session - supabase's client picked that up from the url
    const { error: authError } = await updatePassword(password);
    setLoading(false);

    if (authError) {
      setError(authError.message);
      return;
    }
    setDone(true);
  };

  if (done) {
    return (
      <div style={styles.wrap}>
        <div style={styles.card}>
          <div style={styles.title}>Password updated</div>
          <p style={styles.text}>You're all set.</p>
          <button style={styles.submitBtn} onClick={() => navigate("/")}>
            Go to Builder
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.wrap}>
      <form style={styles.card} onSubmit={handleSubmit}>
        <div style={styles.title}>Reset Password</div>

        {error && <div style={styles.error}>{error}</div>}

        <label style={styles.label}>New Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
          minLength={6}
          required
        />

        <label style={styles.label}>Confirm Password</label>
        <input
          type="password"
          value={confirm}
          onChange={(e) => setConfirm(e.target.value)}
          style={styles.input}
          minLength={6}
          required
        />

        <button type="submit" style={styles.submitBtn} disabled={loading}>
          {loading ? "Updating..." : "Update Password"}
        </button>
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
  text: {
    fontSize: 14,
    color: "#333",
    lineHeight: 1.5,
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
};

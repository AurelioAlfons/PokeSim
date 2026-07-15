// src/context/AuthContext.jsx
import React, { createContext, useContext, useEffect, useState } from "react";
import { supabase } from "../lib/supabaseClient";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // grab whatever session is already stashed in local storage on first load
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setLoading(false);
    });

    // then keep listening - login/logout/token refresh all fire through here
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  const value = {
    session,
    user: session?.user ?? null,
    loading,
    login: (email, password) =>
      supabase.auth.signInWithPassword({ email, password }),
    // signup email needs to know where to send you back - copy resetPassword's trick below
    register: (email, password) =>
      supabase.auth.signUp({
        email,
        password,
        options: { emailRedirectTo: window.location.origin },
      }),
    logout: () => supabase.auth.signOut(),
    resetPassword: (email) =>
      supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/reset-password`,
      }),
    updatePassword: (newPassword) =>
      supabase.auth.updateUser({ password: newPassword }),
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}

// src/lib/supabaseClient.js
import { createClient } from "@supabase/supabase-js";

// one client for the whole app - auth + saved teams both go through this
export const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_ANON_KEY
);

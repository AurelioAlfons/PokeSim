// src/pages/Home.jsx
import React, { useState, useEffect, useRef } from "react";
import TeamHeader from "../components/TeamHeader";
import PokemonPickerGrid from "../components/PokemonPickerGrid";
import PokemonDetailModal from "../components/PokemonDetailModal";
import TeamSlotsPanel from "../components/TeamSlotsPanel";
import SavedTeamsBar from "../components/SavedTeamsBar";
import { createTeam } from "../api/teams";
import { fetchPokemonDetail } from "../api/pokedex";
import { buildDefaultSlotData } from "../utils/pokemonDefaults";

const EMPTY_SLOTS = () => Array(6).fill(null);

export default function Home() {
  // divider logic
  const dividerRef = useRef(null);
  const [splitX, setSplitX] = useState("50%");

  useEffect(() => {
    const updateSplit = () => {
      if (!dividerRef.current) return;

      const rect = dividerRef.current.getBoundingClientRect();

      const APP_TOP_PADDING = -15;
      const y = rect.top - APP_TOP_PADDING;

      const W = window.innerWidth;
      const H = window.innerHeight;

      const boundaryX = (W + H) / 2 - y;
      const localX = boundaryX - rect.left;
      const pct = Math.max(0, Math.min(100, (localX / rect.width) * 100));

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

  // header state
  const [teamName, setTeamName] = useState("");
  const [description, setDescription] = useState("");

  // team assembly state
  const [slots, setSlots] = useState(EMPTY_SLOTS);
  const [editing, setEditing] = useState(null); // { slotIndex, pokedexId, initial }
  const [saving, setSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState(null); // { type: 'success' | 'error', text }
  const [refreshToken, setRefreshToken] = useState(0);

  const teamFull = slots.every(Boolean);

  const resetTeam = () => {
    setTeamName("");
    setDescription("");
    setSlots(EMPTY_SLOTS());
    setSaveStatus(null);
  };

  const handleSelectFromGrid = (summary) => {
    const emptyIndex = slots.findIndex((s) => !s);
    if (emptyIndex === -1) return;
    setEditing({ slotIndex: emptyIndex, pokedexId: summary.id, initial: null });
  };

  const handleEditSlot = (index) => {
    const slot = slots[index];
    if (!slot) return;
    setEditing({
      slotIndex: index,
      pokedexId: slot.pokedex_id,
      initial: {
        level: slot.level,
        ability: slot.ability,
        nickname: slot.nickname,
        moves: slot.moves,
      },
    });
  };

  const handleRemoveSlot = (index) => {
    setSlots((prev) => prev.map((s, i) => (i === index ? null : s)));
  };

  const handleDropOnSlot = (targetIndex, payload) => {
    if (payload.source === "grid") {
      // drag-drop is meant to be instant, no popup - land it with sensible
      // defaults, tap the slot afterward to open the panel and tweak it
      fetchPokemonDetail(payload.pokedexId)
        .then((detail) => {
          setSlots((prev) => {
            const next = [...prev];
            next[targetIndex] = buildDefaultSlotData(detail);
            return next;
          });
        })
        .catch((err) => console.error("Failed to drop Pokemon:", err));
    } else if (payload.source === "slot" && payload.fromIndex !== targetIndex) {
      setSlots((prev) => {
        const next = [...prev];
        [next[targetIndex], next[payload.fromIndex]] = [next[payload.fromIndex], next[targetIndex]];
        return next;
      });
    }
  };

  const handleModalConfirm = (slotData) => {
    setSlots((prev) => {
      const next = [...prev];
      next[editing.slotIndex] = slotData;
      return next;
    });
    setEditing(null);
  };

  const handleLoadTeam = (team) => {
    const newSlots = EMPTY_SLOTS();
    team.pokemon.slice(0, 6).forEach((p, i) => {
      newSlots[i] = {
        pokedex_id: p.id,
        name: p.name,
        nickname: null,
        sprite: p.sprite,
        types: p.types,
        level: p.level,
        ability: p.ability,
        moves: p.moves,
      };
    });
    setTeamName(team.name);
    setDescription("");
    setSlots(newSlots);
    setSaveStatus(null);
  };

  const handleSave = async () => {
    const filled = slots.filter(Boolean);
    if (filled.length === 0) {
      setSaveStatus({ type: "error", text: "Add at least one Pokemon before saving." });
      return;
    }

    const name = teamName.trim() || "New Team";
    setSaving(true);
    setSaveStatus(null);
    try {
      await createTeam({
        name,
        pokemon: filled.map((s) => ({
          pokedex_id: s.pokedex_id,
          nickname: s.nickname,
          level: s.level,
          ability: s.ability,
          moves: s.moves,
        })),
      });
      setSaveStatus({ type: "success", text: `Saved "${name}"!` });
      setRefreshToken((t) => t + 1);
    } catch (err) {
      setSaveStatus({ type: "error", text: err.message });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div
      style={{
        marginTop: 25,
        padding: "0 20px",
      }}
    >
      {/* Top header */}
      <TeamHeader
        teamName={teamName}
        onTeamNameChange={setTeamName}
        description={description}
        onDescriptionChange={setDescription}
        onCancel={resetTeam}
        onSave={handleSave}
      />

      {saveStatus && (
        <div
          style={{
            marginTop: 10,
            padding: "8px 14px",
            borderRadius: 8,
            fontWeight: 700,
            fontSize: 14,
            color: saveStatus.type === "success" ? "#1a7a3c" : "#a11d1d",
            background: saveStatus.type === "success" ? "#e3f7e9" : "#fbe4e4",
            border: `2px solid ${saveStatus.type === "success" ? "#1a7a3c" : "#a11d1d"}`,
          }}
        >
          {saving ? "Saving..." : saveStatus.text}
        </div>
      )}

      {/* Adaptive Divider */}
      <div
        ref={dividerRef}
        style={{
          marginTop: 20,
          height: 3,
          width: "100%",
          background: `linear-gradient(
            90deg,
            #f7e733 ${splitX},
            #111 ${splitX}
          )`,
        }}
      />

      {/* Main content */}
      <div
        style={{
          marginTop: 30,
          display: "flex",
          flexDirection: "column",
          gap: 30,
        }}
      >
        <TeamSlotsPanel
          slots={slots}
          onSlotClick={handleEditSlot}
          onRemove={handleRemoveSlot}
          onDropOnSlot={handleDropOnSlot}
        />

        <PokemonPickerGrid onSelect={handleSelectFromGrid} teamFull={teamFull} />
      </div>

      <SavedTeamsBar refreshToken={refreshToken} onLoad={handleLoadTeam} />

      <PokemonDetailModal
        open={!!editing}
        pokedexId={editing?.pokedexId}
        initial={editing?.initial}
        onConfirm={handleModalConfirm}
        onClose={() => setEditing(null)}
      />
    </div>
  );
}

// src/api/teams.js
import { supabase } from "../lib/supabaseClient";
import { fetchPokemonDetail } from "./pokedex";
import { titleCase } from "../utils/pokemonDefaults";

// supabase only stores pokedex_id + level/ability/moves - sprite/types/name
// used to come free from the old backend's Pokemon.to_dict(), now we go
// fetch that per member off the (fast, cached) pokedex endpoint instead
async function hydrateMember(member) {
  const detail = await fetchPokemonDetail(member.pokedex_id);
  return {
    id: member.pokedex_id,
    name: member.nickname || titleCase(detail.name),
    sprite: detail.sprite,
    types: detail.types,
    level: member.level,
    ability: member.ability,
    moves: member.moves,
  };
}

export async function fetchTeams() {
  // RLS scopes this to the logged-in user automatically, no filter needed
  const { data, error } = await supabase
    .from("teams")
    .select("id, name, team_members(id)")
    .order("id", { ascending: false });
  if (error) throw new Error(error.message);

  return data.map((t) => ({
    id: t.id,
    name: t.name,
    pokemon_count: t.team_members.length,
  }));
}

export async function fetchTeam(teamId) {
  const { data, error } = await supabase
    .from("teams")
    .select("id, name, team_members(*)")
    .eq("id", teamId)
    .single();
  if (error) throw new Error(error.message);

  const members = [...data.team_members].sort((a, b) => a.slot - b.slot);
  const pokemon = await Promise.all(members.map(hydrateMember));

  return { id: data.id, name: data.name, pokemon };
}

export async function createTeam(body) {
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) throw new Error("You must be logged in to save a team.");

  const { data: team, error: teamError } = await supabase
    .from("teams")
    .insert({ name: body.name, user_id: user.id })
    .select()
    .single();
  if (teamError) throw new Error(teamError.message);

  const { error: membersError } = await supabase
    .from("team_members")
    .insert(memberRows(team.id, body.pokemon));
  if (membersError) throw new Error(membersError.message);

  return { id: team.id };
}

export async function updateTeam(teamId, body) {
  // full replace, same approach the old sqlite version used - rename, wipe
  // the members, re-insert from scratch, simplest correct thing
  const { error: renameError } = await supabase
    .from("teams")
    .update({ name: body.name })
    .eq("id", teamId);
  if (renameError) throw new Error(renameError.message);

  const { error: deleteError } = await supabase
    .from("team_members")
    .delete()
    .eq("team_id", teamId);
  if (deleteError) throw new Error(deleteError.message);

  const { error: insertError } = await supabase
    .from("team_members")
    .insert(memberRows(teamId, body.pokemon));
  if (insertError) throw new Error(insertError.message);

  return { ok: true };
}

export async function deleteTeam(teamId) {
  // team_members cascades off the teams FK, no separate delete needed
  const { error } = await supabase.from("teams").delete().eq("id", teamId);
  if (error) throw new Error(error.message);
  return { ok: true };
}

function memberRows(teamId, pokemon) {
  return pokemon.map((mon, i) => ({
    team_id: teamId,
    slot: i,
    pokedex_id: mon.pokedex_id,
    nickname: mon.nickname,
    level: mon.level,
    ability: mon.ability,
    moves: mon.moves,
  }));
}

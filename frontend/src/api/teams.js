// src/api/teams.js
import { get, post, del } from "./client";

export function fetchTeams() {
  return get("/teams/");
}

export function fetchTeam(teamId) {
  return get(`/teams/${teamId}`);
}

export function createTeam(body) {
  return post("/teams/", body);
}

export function deleteTeam(teamId) {
  return del(`/teams/${teamId}`);
}

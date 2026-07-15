// src/api/teams.js
import { get, post, put, del } from "./client";

export function fetchTeams() {
  return get("/teams/");
}

export function fetchTeam(teamId) {
  return get(`/teams/${teamId}`);
}

export function createTeam(body) {
  return post("/teams/", body);
}

export function updateTeam(teamId, body) {
  return put(`/teams/${teamId}`, body);
}

export function deleteTeam(teamId) {
  return del(`/teams/${teamId}`);
}

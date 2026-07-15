-- PokeSim — Supabase schema for user accounts + saved teams
--
-- Run this once in the Supabase dashboard: Project -> SQL Editor -> New query -> paste -> Run.
-- Requires your own logged-in Supabase session (the anon key used by the app
-- can't create tables or policies, so this can't be run from the app itself).

create table teams (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  name text not null,
  created_at timestamptz not null default now()
);

create table team_members (
  id bigint generated always as identity primary key,
  team_id bigint not null references teams(id) on delete cascade,
  slot integer not null,
  pokedex_id integer not null,
  nickname text,
  level integer not null default 50,
  ability text,
  moves jsonb not null default '[]'::jsonb
);

alter table teams enable row level security;
alter table team_members enable row level security;

-- teams: a row's owner is whoever's user_id matches the logged-in user
create policy "select own teams" on teams
  for select using (auth.uid() = user_id);

create policy "insert own teams" on teams
  for insert with check (auth.uid() = user_id);

create policy "update own teams" on teams
  for update using (auth.uid() = user_id);

create policy "delete own teams" on teams
  for delete using (auth.uid() = user_id);

-- team_members has no user_id of its own - ownership is checked through
-- its parent team, otherwise this table would be wide open regardless of
-- how locked-down `teams` is.
create policy "select own team_members" on team_members
  for select using (
    exists (
      select 1 from teams
      where teams.id = team_members.team_id
      and teams.user_id = auth.uid()
    )
  );

create policy "insert own team_members" on team_members
  for insert with check (
    exists (
      select 1 from teams
      where teams.id = team_members.team_id
      and teams.user_id = auth.uid()
    )
  );

create policy "update own team_members" on team_members
  for update using (
    exists (
      select 1 from teams
      where teams.id = team_members.team_id
      and teams.user_id = auth.uid()
    )
  );

create policy "delete own team_members" on team_members
  for delete using (
    exists (
      select 1 from teams
      where teams.id = team_members.team_id
      and teams.user_id = auth.uid()
    )
  );

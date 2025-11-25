Build your own Pokémon Battle Simulator (Gen 4)

This repo is my attempt at creating a small Pokémon battle simulator that focuses on Gen 4 Pokémon only (Diamond / Pearl / Platinum) at the beginning. The idea is to keep it simple first, then slowly expand it as I learn more.

What this project is:

- A Gen 4-only Pokémon battle simulator (for now)
- A practice project to learn frontend ↔ backend ↔ database
- A place to experiment with team building, damage logic, and simple battle flows

Tech stack

- Frontend: React
- Backend: Python (FastAPI)
- Database: SQLite
- API style: REST (JSON)

Core ideas / features

- Access to a Pokémon database for Gen 4:
  - Pokémon names
  - Types
  - Base stats
  - Moves
  - Abilities
- Team creation:
  - Build a team of up to 6 Pokémon
  - Pick moves and abilities for each member
- Simple battle simulator:
  - Battle other “trainer” teams or wild / rogue Pokémon
  - Turn-based damage calculations with a simple formula
  - No battle animations at the start, just text + numbers (HP changes, move messages)

Planned flow

- Get Pokémon data from the backend via API
- Use React to build:
  - Pokémon list view
  - Team builder page
  - Basic battle screen
- Send battle actions (like “use move”) to the backend and return damage + messages

Current status

- Setting up the project structure (frontend + backend folders)
- Starting with basic endpoints and a small Gen 4 Pokémon dataset
- Slowly wiring React components to call the FastAPI backend

Future ideas

- Expand beyond Gen 4 later
- Add more detailed move effects, abilities, and status conditions
- Add simple animations or better UI once the core logic feels solid

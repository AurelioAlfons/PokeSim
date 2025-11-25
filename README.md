# <img src="assets/SVG/445.svg" width="70" /> PokeSim – Gen 4 Pokémon Battle Simulator

![React](https://img.shields.io/badge/Frontend-React-blue?logo=react&logoColor=white)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-teal?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Language-Python-yellow?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-Early%20WIP-orange)

---

This repo is my attempt at creating a small Pokémon battle simulator that focuses on **Gen 4 Pokémon only** at the beginning.  

---

## <img src="assets/SVG/392.svg" width="70" /> What This Project Is

- A Gen 4–only Pokémon battle simulator (for now)  
- A learning project for frontend ↔ backend ↔ database  
- A place to experiment with:
  - Team building  
  - Damage calculation  
  - Basic turn-based battle logic  

---

## <img src="assets/SVG/389.svg" width="70" /> Tech Stack

- **Frontend:** React  
- **Backend:** Python + FastAPI  
- **Database:** PostgreSQL  
- **API:** REST (JSON)  

---

## <img src="assets/SVG/395.svg" width="70" /> Core Features

- **Pokémon Database (Gen 4):**
  - Names  
  - Types  
  - Base stats  
  - Moves  
  - Abilities  

- **Team Builder:**
  - Create a team of up to 6 Pokémon  
  - Select moves and abilities  

- **Battle Simulator:**
  - Fight trainer teams or wild “rogue” Pokémon  
  - Simple damage formula  
  - Text-based battle results  
  - No animations yet  

---

## <img src="assets/SVG/466.svg" width="70" /> Planned Flow

- Fetch Pokémon data from FastAPI  
- Display using React (Pokémon list, team builder, battle page)  
- Send battle actions to backend:
  - “Use move”
  - Backend calculates damage
  - Return results to frontend  

---

## <img src="assets/SVG/398.svg" width="70" /> Current Status

- Project folders set up  
- React frontend created  
- FastAPI backend planned  
- Starting with small Gen 4 Pokémon dataset  
- Connecting frontend → backend next  

---

## <img src="assets/SVG/493.svg" width="70" /> Future Ideas

- Expand to more generations  
- Add more move effects, status conditions  
- Add animations or polished UI later  

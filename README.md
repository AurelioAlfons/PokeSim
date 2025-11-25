# 🟦 PokeSim – Build Your Own Gen 4 Pokémon Battle Simulator

![React](https://img.shields.io/badge/Frontend-React-blue?logo=react&logoColor=white)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-teal?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Language-Python-yellow?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-Early%20WIP-orange)

---

This repo is my attempt at creating a small Pokémon battle simulator that focuses on **Gen 4 Pokémon only** (Diamond / Pearl / Platinum) at the beginning.  
The idea is to keep it simple first, then slowly expand it as I learn more.

**“What I cannot create, I do not understand.” — Richard Feynman**

It’s a fun way for me to learn full-stack development with React + Python.

---

## 🟩 What This Project Is

- A Gen 4–only Pokémon battle simulator (for now)  
- A learning project for frontend ↔ backend ↔ database  
- A place to experiment with:
  - Team building  
  - Damage calculation  
  - Basic turn-based battle logic  

---

## 🟨 Tech Stack

- **Frontend:** React  
- **Backend:** Python + FastAPI  
- **Database:** SQLite  
- **API:** REST (JSON)  

---

## 🟦 Core Features

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

## 🟪 Planned Flow

- Fetch Pokémon data from FastAPI  
- Display using React (Pokémon list, team builder, battle page)  
- Send battle actions to backend:
  - “Use move”
  - Backend calculates damage
  - Return results to frontend  

---

## 🟫 Current Status

- Project folders set up  
- React frontend created  
- FastAPI backend planned  
- Starting with small Gen 4 Pokémon dataset  
- Connecting frontend → backend next  

---

## 🟧 Future Ideas

- Expand to more generations  
- Add more move effects, status conditions  
- Add animations or polished UI later  

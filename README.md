# ⚡ PokeSim – Gen 4 Pokémon Battle Simulator

<!-- Choose ONE: Banner OR Screenshots -->

<!-- Option A: Banner -->
<p align="center">
  <img src="./assets/banner.png" alt="PokeSim Banner" width="100%" />
</p>

<!-- Option B: Screenshots
<p align="center">
  <img src="./assets/screenshot-1.png" width="48%" alt="PokeSim Team Builder" />
  <img src="./assets/screenshot-2.png" width="48%" alt="PokeSim Battle Screen" />
</p>
-->

<p align="center">
  <strong>A Gen 4 Pokémon battle simulator with team building, saved teams, and a rogue-style battle mode.</strong>
</p>

<p align="center">
  <a href="https://poke-sim-two.vercel.app"><strong>🚀 Live Demo</strong></a>
  &nbsp;•&nbsp;
  <a href="https://pokesim-backend.onrender.com/docs"><strong>⚙️ API Docs</strong></a>
</p>

---

## 🛠 Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" />
  <img src="https://img.shields.io/badge/Render-000000?style=for-the-badge&logo=render&logoColor=white" />
</p>

**Frontend:** React (Create React App)  
**Backend:** Python + FastAPI  
**Database & Auth:** Supabase + PostgreSQL  
**API:** REST API  
**Hosting:** Vercel + Render

---

## 📖 About

PokeSim started as a small project to learn how a frontend and backend communicate through an API.

It has since grown into a Gen 4 Pokémon battle simulator with a full Pokédex, drag-and-drop Team Builder, user accounts, saved teams, turn-based battles, and Rogue Mode.

Generation 4 is currently the only supported generation.

---

## ✨ Core Features

### 📖 Pokédex & Team Builder

- Browse, search, and filter all **107 Gen 4 Pokémon**
- Drag and drop Pokémon to build and reorder teams
- Swap Pokémon between team slots
- Configure nickname, level, ability, and moveset

### 👤 Accounts & Saved Teams

- Register and log in
- Save, load, and edit teams
- Password reset support
- Private account data using **Supabase Row Level Security**

### ⚔️ Battle System

- Turn-based battle flow
- Move selection
- Pokémon switching
- Running from battles
- HP and EXP system
- Backend-driven battle calculations

### 🏆 Rogue Mode

- Battle through waves of wild Pokémon
- Enemies scale based on your team
- Wave progression system
- Between-battle healing

---

## ⚙️ How It Works

```text
React Frontend
      ↓
   REST API
      ↓
FastAPI Backend
      ↓
 Battle Logic
      ↓
Updated Battle State
      ↓
 React UI
```

The React frontend sends actions such as moves, switching, and running to the FastAPI backend.

The backend processes the battle logic and returns updated Pokémon stats, battle logs, and battle state to the frontend.

Supabase handles authentication and account-based saved teams.

---

## 📌 Project Status

- ✅ Full Gen 4 Pokédex
- ✅ Drag-and-drop Team Builder
- ✅ User authentication
- ✅ Saved Teams
- ✅ Turn-based battle system
- ✅ HP and EXP system
- ✅ Rogue Mode
- ✅ Frontend deployed on Vercel
- ✅ Backend deployed on Render
- ✅ Supabase Row Level Security

---

## 🔮 What's Next

- Expand support to more Pokémon generations
- Add more move effects
- Add status conditions
- Improve battle animations and UI
- Expand Rogue Mode
- Multiplayer / PvP battles

---

## ⚠️ Disclaimer

Pokémon and related names, characters, and assets are trademarks of Nintendo, Game Freak, Creatures Inc., and The Pokémon Company.

PokeSim is an unofficial educational and portfolio project and is not affiliated with or endorsed by these companies.

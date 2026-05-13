from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.battle_router import router as battle_router

app = FastAPI(title="PokeSim – Gen 4 Battle API")

# allow local frontend ports for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://poke-sim-two.vercel.app",
        "https://poke-aznezhjd0-aurelio-alfons-projects.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "PokeSim API root"}

@app.get("/health")
def health():
    return {"status": "ok", "message": "API is running"}

app.include_router(battle_router, prefix="/battle", tags=["battle"])

# optional local manual run
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("backend.main:app", host="127.0.0.1", port=5000, reload=True)
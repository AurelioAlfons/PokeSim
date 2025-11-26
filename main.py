# main.py
from fastapi import FastAPI
from backend.routers.battle_router import router as battle_router

app = FastAPI(title="PokeSim – Gen 4 Battle API")

# simple root route
@app.get("/")
def root():
    return {"message": "PokeSim API root"}

# health check
@app.get("/ping")
def root_ping():
    return {"status": "ok", "message": "root API is running"}

# battle routes
app.include_router(battle_router, prefix="/battle", tags=["battle"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)

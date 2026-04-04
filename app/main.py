from fastapi import FastAPI, Depends
from .routers import lieux, personnages

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bienvenue dans L'Épopée des Cités Perdues"}

app.include_router(
    lieux.router,
    prefix="/lieux",
    tags=["lieux"]
)

app.include_router(
    personnages.router,
    prefix="/personnages",
    tags=["personnages"]
)
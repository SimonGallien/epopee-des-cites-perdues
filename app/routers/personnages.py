from fastapi import APIRouter
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from scripts.init_db import get_engine
from app.schemas import PersonnageSchema
from src.modeles import Personnage, RessourcePersonnage

engine = get_engine()
router = APIRouter()

@router.get("", response_model=list[PersonnageSchema])
async def get_personnages():
    with Session(engine) as session:
        personnages = session.scalars(
            select(Personnage)
            .options(joinedload(Personnage.inventaire).joinedload(RessourcePersonnage.ressource))
            .order_by(Personnage.id)
            ).unique().all()
    return personnages
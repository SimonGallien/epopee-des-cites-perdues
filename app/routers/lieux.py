from fastapi import APIRouter
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from scripts.init_db import get_engine
from app.schemas import LieuSchema
from src.modeles import Lieu, RessourceLieu

engine = get_engine()
router = APIRouter()

@router.get("", response_model=list[LieuSchema])
async def get_lieux():
    with Session(engine) as session:
        lieux = session.scalars(
            select(Lieu)
            .options(joinedload(Lieu.inventaire).joinedload(RessourceLieu.ressource))
            .order_by(Lieu.id)
            ).unique().all()
    return lieux
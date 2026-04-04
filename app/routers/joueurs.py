from fastapi import APIRouter
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from scripts.init_db import get_engine
from app.schemas import JoueurSchema, JoueurCreateSchema, JoueurUpdateSchema
from src.modeles import Joueur, RessourceJoueur
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

engine = get_engine()
router = APIRouter()

@router.get("", response_model=list[JoueurSchema])
async def get_joueurs():
    with Session(engine) as session:
        joueurs = session.scalars(
            select(Joueur)
            .options(joinedload(Joueur.inventaire).joinedload(RessourceJoueur.ressource),
                     joinedload(Joueur.lieu_actuel))
            .order_by(Joueur.id)
            ).unique().all()
    return joueurs

@router.get("/{joueur_id}", response_model=JoueurSchema)
async def get_joueur(joueur_id: int):
    with Session(engine) as session:
        joueur = session.scalar(
            select(Joueur)
            .options(
                joinedload(Joueur.inventaire).joinedload(RessourceJoueur.ressource),
                joinedload(Joueur.lieu_actuel))
            .where(Joueur.id == joueur_id)
        )
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur introuvable")
    return joueur

@router.post("", response_model=JoueurSchema)
async def create_joueur(nom_joueur: JoueurCreateSchema):
    with Session(engine) as session:
        try:
            joueur = Joueur(nom=nom_joueur.nom)
            session.add(joueur)
            session.commit()
            joueur_id = joueur.id
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Ce nom de joueur existe déjà")
    
    return await get_joueur(joueur_id)

@router.put("/{joueur_id}", response_model=JoueurSchema)
async def update_joueur(joueur_id: int, joueur_data: JoueurUpdateSchema):

    with Session(engine) as session:
        joueur = session.scalar(select(Joueur).where(Joueur.id == joueur_id))

        if not joueur:
            raise HTTPException(status_code=404, detail="Joueur introuvable")
        
        if joueur_data.force is not None:
            joueur.force = joueur_data.force
        if joueur_data.point_de_vie is not None:
            joueur.point_de_vie = joueur_data.point_de_vie
        if joueur_data.lieu_actuel_id is not None:
            joueur.lieu_actuel_id = joueur_data.lieu_actuel_id

        session.commit()

    return await get_joueur(joueur_id)

@router.delete("/{joueur_id}")
async def delete_joueur(joueur_id: int):
    
    with Session(engine) as session:
        joueur = session.scalar(select(Joueur).where(Joueur.id == joueur_id))

        if not joueur:
            raise HTTPException(status_code=404, detail="Joueur introuvable")

        session.delete(joueur)
        session.commit()

    return {"message": f"Joueur {joueur_id} supprimé"}

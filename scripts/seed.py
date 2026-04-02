from scripts.init_db import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
import json
from src.modeles import Lieu, RessourceLieu, Ressource, Personnage, RessourcePersonnage

with open(file="data/data.json", mode="r", encoding="utf-8") as fichier:
    data = json.load(fichier)

# create session and add objects
with Session(engine) as session:

    for r in data["ressources"]:

        insert_ressource = insert(Ressource).values(
            nom=r["nom"],
            utilite=r["utilite"]
            ).on_conflict_do_nothing(index_elements=["nom"])
        
        session.execute(insert_ressource)
        session.commit()

    for l in data["lieux"]:

        insert_lieu = insert(Lieu).values(
            nom=l["nom"], 
            description=l["description"]
            ).on_conflict_do_nothing(index_elements=["nom"])
        
        session.execute(insert_lieu)
        session.commit()

        for nom_ressource, qte in l["ressources"].items():

            lieu_obj = session.scalar(select(Lieu).filter_by(nom=l["nom"]))
            ressource_obj = session.scalar(select(Ressource).filter_by(nom=nom_ressource))

            insert_ressource_lieu = insert(RessourceLieu).values(
                lieu_id=lieu_obj.id, 
                ressource_id=ressource_obj.id,
                quantite=qte
                ).on_conflict_do_nothing(index_elements=["lieu_id", "ressource_id"])
            
            session.execute(insert_ressource_lieu)
            session.commit()

    for p in data["personnages"]:

        insert_personnage = insert(Personnage).values(nom=p["nom"],type=p["type"], force=p["force"], dialogue=p["dialogue"]).on_conflict_do_nothing(index_elements=["nom"])
        
        session.execute(insert_personnage)
        session.commit()

        for nom_ressource, qte in p["ressources"].items():

            personnage_obj = session.scalar(select(Personnage).filter_by(nom=p["nom"]))
            ressource_obj = session.scalar(select(Ressource).filter_by(nom=nom_ressource))

            insert_ressource_personnage = insert(RessourcePersonnage).values(
                quantite=qte, 
                personnage_id=personnage_obj.id, 
                ressource_id=ressource_obj.id
                ).on_conflict_do_nothing(index_elements=["personnage_id", "ressource_id"])
            
            session.execute(insert_ressource_personnage)
            session.commit()
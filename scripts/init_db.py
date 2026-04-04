# Les classes 'Joueur', 'Lieu' et 'Personnage'
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from src.modeles import Base

load_dotenv()

def get_engine():
    db_user = os.environ["DB_USER"]
    db_password = os.environ["DB_PASSWORD"]
    db_name = os.environ["POSTGRES_DB"]
    db_host = os.environ["DB_HOST"]
    db_port = os.environ["DB_PORT"]
    db_url = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_url, echo=True)
    return engine

def init_db():
    try:
        Base.metadata.create_all(get_engine())
        print("✅ Success! Toutes les tables sont créées.")
    except Exception as e:
        print(e)
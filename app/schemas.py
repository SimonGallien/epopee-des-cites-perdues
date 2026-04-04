from pydantic import BaseModel, ConfigDict

class LieuSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nom: str
    description: str
    # inventaire: list["RessourceLieuSchema"] = []

class RessourceLieuSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    quantite: int
    ressource: "RessourceSchema"

class PersonnageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nom: str
    type: str
    dialogue: str
    force: int
    inventaire: list["RessourcePersonnageSchema"]

class RessourcePersonnageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    quantite: int
    ressource: "RessourceSchema"

class JoueurSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nom: str
    force: int
    point_de_vie: int
    lieu_actuel: "LieuSchema | None" = None
    inventaire: list["RessourceJoueurSchema"]

class RessourceJoueurSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    quantite: int
    ressource: "RessourceSchema"

class RessourceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nom: str
    utilite: str

class JoueurCreateSchema(BaseModel):
    nom: str

class JoueurUpdateSchema(BaseModel):
    force: int | None = None
    point_de_vie: int | None = None
    lieu_actuel_id: int | None = None
    # inventaire: list["RessourceJoueurSchema"]

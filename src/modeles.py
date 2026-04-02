# Les classes 'Joueur', 'Lieu' et 'Personnage' et 'Ressource
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

class Base(DeclarativeBase):
    pass

# ========= Class principal =========

class Ressource(Base):
    __tablename__ = "ressource"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String, unique=True)
    utilite: Mapped[str] = mapped_column(String)

    inventaires_personnages: Mapped[list["RessourcePersonnage"]] = relationship(
        back_populates="ressource", 
        cascade="all, delete-orphan")
    
    inventaires_lieux: Mapped[list["RessourceLieu"]] = relationship(
        back_populates="ressource", 
        cascade="all, delete-orphan")

    inventaires_joueur: Mapped[list["RessourceJoueur"]] = relationship(
        back_populates="ressource", 
        cascade="all, delete-orphan")

    def __repr__(self):
        return f"Ressource = {self.id!r}, nom = {self.nom!r}"    

class Personnage(Base):
    __tablename__ = "personnage"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(30), unique=True)
    type: Mapped[str] = mapped_column(String(30))
    dialogue: Mapped[str] = mapped_column(String(230))
    force: Mapped[int] = mapped_column(Integer)

    inventaire: Mapped[list["RessourcePersonnage"]] = relationship(
        back_populates="personnage", 
        cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Personnage(id={self.id!r}, nom={self.nom!r}, type={self.type!r}, dialogue={self.dialogue!r}, force={self.force!r})"

class Lieu(Base):
    __tablename__ = "lieu"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str] = mapped_column(String(230))

    inventaire: Mapped[list["RessourceLieu"]] = relationship(
        back_populates="lieu",
        cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Lieu = {self.id!r}, nom = {self.nom!r}, description = {self.description!r}" 

class Joueur(Base):
    __tablename__ = "joueur"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(42), unique=True)
    force: Mapped[int] = mapped_column(Integer, default=1)
    point_de_vie: Mapped[int] = mapped_column(Integer, default=100)

    inventaire: Mapped[list["RessourceJoueur"]] = relationship(
        back_populates="joueur",
        cascade="all, delete-orphan")

    def __repr__(self):
        return f"Joueur = {self.id!r}, nom = {self.nom!r}, force = {self.force!r}, point de vie = {self.point_de_vie!r}"

 # ========== Tables de liaisons ==========

class RessourcePersonnage(Base):
    __tablename__ = "ressource_personnage"

    personnage_id: Mapped[int] = mapped_column(ForeignKey("personnage.id"), primary_key=True)
    ressource_id: Mapped[int] = mapped_column(ForeignKey("ressource.id"), primary_key=True)

    quantite: Mapped[int] = mapped_column(Integer, default=0)

    personnage: Mapped["Personnage"] = relationship(back_populates="inventaire")
    ressource: Mapped["Ressource"] = relationship(back_populates="inventaires_personnages") 

class RessourceLieu(Base):
    __tablename__ = "ressource_lieu"

    lieu_id: Mapped[int] = mapped_column(ForeignKey("lieu.id"), primary_key=True)
    ressource_id: Mapped[int] = mapped_column(ForeignKey("ressource.id"), primary_key=True)

    quantite: Mapped[int] = mapped_column(Integer, default=0)

    lieu: Mapped["Lieu"] = relationship(back_populates="inventaire")
    ressource: Mapped["Ressource"] = relationship(back_populates="inventaires_lieux") 

class RessourceJoueur(Base):
    __tablename__ = "ressource_joueur"

    joueur_id: Mapped[int] = mapped_column(ForeignKey("joueur.id"), primary_key=True)
    ressource_id: Mapped[int] = mapped_column(ForeignKey("ressource.id"), primary_key=True)

    quantite: Mapped[int] = mapped_column(Integer, default=0)

    joueur: Mapped["Joueur"] = relationship(back_populates="inventaire")
    ressource: Mapped["Ressource"] = relationship(back_populates="inventaires_joueur")
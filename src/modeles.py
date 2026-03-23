# Les classes 'Joueur', 'Lieu' et 'Personnage'
from src.erreur import NomInvalideError

class Personnage:
    """Classe représentant un personnage non joueur du jeu"""

    def __init__(self, nom: str, type: str, dialogue: str, force: int):
        """Initialise un personnage

        Args:
            nom (str): Nom du personnage
            type (str): Type du personnage (Allié ou ennemi)
            dialogue (str): Dialogue du personnage
            force (int): Force du personnage
        """
        self.nom = nom
        self.type = type
        self.dialogue = dialogue
        self.force = force

class Lieu:
    """Classe représentant un lieu du jeu"""

    def __init__(self, nom: str, description: str, ressources: list, ennemis: list):
        """Initialisation d'un lieu

        Args:
            nom (str): Nom du lieu
            description (str): Description du lieu
            ressources (list): Ressource présent dans le lieu
            ennemis (list): Ennemi présent dans le lieu
        """
        self.nom = nom
        self.description = description
        self.ressources = ressources
        self.ennemi = ennemis

class Joueur:
    """Classe représentant un joueur"""

    def __init__(self, nom: str, force = 1, inventaire = None, point_de_vie = 100):
        """Initialisation de la classe joueur

        Args:
            nom (str): Nom du joueur
            force (int, optional): Force du joueur
            inventaire (dict, optional): Inventaire du joueur
            point_de_vie (int, optional): Nombre de points de vies du joueur. 100 poinst par défaut.
        """

        nom = nom.strip()

        if not nom:
            raise NomInvalideError("Le nom de joueur ne peut pas être vide.")
        elif len(nom) > 15:
            raise NomInvalideError("le nom est trop long (15 caractères maximum).")
        
        self.nom = nom
        self.force = force
        self.point_de_vie = point_de_vie
        self.inventaire = inventaire
        
class Ressource:
    """Classe représentant une ressource du jeu"""

    def __init__(self, nom: str, utilite: str):
        """Initialisation de la classe ressource

        Args:
            nom (str): Nom de la ressource
            qte (int): Quantité de la ressource
            utilite (str): utilité de la ressource
        """
        self.nom = nom
        self.utilite = utilite
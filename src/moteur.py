# La classe 'Jeu' qui gère les menus, ...
from src.modeles import Joueur, Lieu, Personnage, Ressource
from src.vue import VueConsole
from src.erreur import NomInvalideError
from pathlib import Path
import json
import sys

data_file = Path("data/data.json")
data_joueur = Path("data/joueur.json")

class Jeu:
    """Classe Jeu représentant une partie"""

    def __init__(self):
        """Initialisation de la classe Jeu"""
        self.joueur = None
        self.lieux = []
        self.lieu_actuel = None
        self.personnages = []
        self.ressources = []
        self.vue = VueConsole()

    def charger_donnes(self):
        """Cette fonction vient charger les données (Lieux, Personnages et Ressources) du fichier .json du Jeu"""

        with open(data_file, "r", encoding="utf-8") as fichier:
            data = json.load(fichier)

            for lieu in data["lieux"]:
                objet_lieu = Lieu(
                    nom = lieu["nom"],
                    description = lieu["description"],
                    ennemis = lieu["ennemis"],
                    ressources = lieu["ressources"]
                )
                self.lieux.append(objet_lieu)

            for personnage in data["personnages"]:
                objet_personnage = Personnage(
                    nom = personnage["nom"],
                    type = personnage["type"],
                    force = personnage["force"],
                    dialogue = personnage["dialogue"]
                )
                self.personnages.append(objet_personnage)

            for ressource in data["ressources"]:
                objet_ressource = Ressource(
                    nom = ressource["nom"],
                    utilite = ressource["utilite"],
                )
                self.ressources.append(objet_ressource)
    
    def menu_accueil(self):
        """Affiche le menu de démarrage du jeu avec la possibilité de charger un Joueur existant ou en créé un nouveau"""

        select = self.vue.afficher_menu_accueil()

        match select:

            case "1":
                self.nouveau_joueur()

            case "2":
                self.charger_une_sauvegarde()
                
            case _:
                self.vue.afficher_erreur_saisie()

    def menu_parti(self):
        """Affiche le menu une fois le joueur dans la partie..."""
        
        while True:
            self.vue.afficher_menu_action()
            
            choix_action = input("Ton choix : ")

            match choix_action:

                case "1":
                    self.changer_lieu()

                case "2":
                    self.attaquer()

                case "3":
                    self.prendre_ressource()

                case "4":
                    self.afficher_inventaire()

                case "5":
                    self.sauvegarder()
                    
                case "6":
                    self.quitter()

                case _:
                    self.vue.afficher_erreur_saisie()
    
    def nouveau_joueur(self):
        """Demande au joueur de renseigner son nom de joueur,
        charge un lieu et affiche le menu d'action de la partie"""

        while True:
            nom_joueur = input("Ok, donne un nom à ton personnage : ").strip()

            try:
                self.joueur = Joueur(nom = nom_joueur)
                break
            
            except NomInvalideError as e:
                self.vue.afficher_erreur(e)
        
        self.lieu_actuel = self.lieux[0]
        self.vue.afficher_description_lieu(self.lieu_actuel.nom, self.lieu_actuel.description)
        self.menu_parti()

    def charger_une_sauvegarde(self):
        """Demande au joueur de sélectionner une sauvegarde,
        puis charge la partie correspondante depuis le fichier json"""

        print("Avec quelle personnage tu veux jouer ?")

    def changer_lieu(self):
        """Affiche la liste des lieux et propose au joueur de choisir l'index de cette liste comme destination.
            Le joueur est avertie sur sa nouvelle destination et affiche la description du lieu"""
        
        self.vue.afficher_menu_changer_lieu(self.lieux, self.lieu_actuel.nom)

        # Le joueur choisi l'index correspondant à la destination choisi
        index_choisi = input("Renseigne le numéro de ta destination :")

        # Mise à jour du lieu actuel
        self.lieu_actuel = self.lieux[int(index_choisi) - 1]

        # On informe le joueur de sa nouvelle destination
        self.vue.afficher_description_lieu(nom_lieu=self.lieu_actuel.nom, description_lieu=self.lieu_actuel.description)

    def prendre_ressource(self):
        """Affiche la liste des ressources disponible dans le lieu ou se trouve le joueur,
        Le joueur peux chosir d'ajouter ces ressources dans son inventaire"""

        print("Ressources disponible :")
        for ressource in self.lieu_actuel.ressources:
            for r in self.ressources:
                if ressource == r.nom:
                    print(f"{ressource}, il y a {r.qte}")
    
    def attaquer(self):
        """Affiche le ou les ennemis avec leur niveau de force dans le lieu ou se trouve le joueur,
        le joueur peut choisir d'attaquer ou de battre en retraite"""

        print("Fonctionnalité 'Attaquer' à venir...")

    def afficher_inventaire(self):
        """Affiche l'inventaire du jeu et propose au joueur d'augmenter ses stats"""

        print(f"Inventaire de {self.joueur.nom} : {self.joueur.inventaire}")
    
    def sauvegarder(self):
        """Propose au joueur de valider la sauvegarde de sa partie en cours"""

        print("Fonctionnalité 'Sauvegarder' à venir...")

    def quitter(self):
        """Quitter le jeu, propose de sauvegarder avant de valider pour quitter"""

        print("Merci d'avoir joué ! À bientôt.")

        sys.exit()
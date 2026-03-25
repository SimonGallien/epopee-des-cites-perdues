from src.modeles import Joueur, Lieu, Personnage, Ressource
from src.vue import VueConsole
from src.erreur import NomInvalideError
from pathlib import Path
import json
import sys
import os

data_file = Path("data/data.json")
data_joueur = Path("data/joueur.json")
data_sauvegarde = Path("data/sauvegarde.json")

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

    def menu_parti(self):
        """Affiche le menu une fois le joueur dans la partie..."""

        while True:
            choix_action = self.vue.afficher_menu_action()
            
            match choix_action:
                case "1":
                    self.changer_lieu()
                case "2":
                    self.attaquer()
                case "3":
                    self.prendre_ressource()
                case "4":
                    self.inventaire()
                case "5":
                    self.sauvegarder()   
                case "6":
                    self.quitter()
    
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

        if not data_sauvegarde.exists():
            self.vue.afficher_erreur("Aucune sauvegarde n'a été trouvée.")
            return

        # Initialisation d'une liste qui contiendra les noms de sauvegardes
        liste_sauvegarde = []

        # Ouverture du fichier pour récupérer les sauvegardes
        with open(file=data_sauvegarde, mode="r", encoding="utf-8") as fichier:
            try:
                data = json.load(fichier)
            except:
                self.vue.afficher_erreur("Le fichier de sauvegarde est corrompu.")
                return
        
        # On ajoute les noms de sauvegarde dans la liste_sauvegarde
        for sauvegarde in data.keys():
            liste_sauvegarde.append(sauvegarde)

        # On affiche les sauvegardes au joueur
        nom_sauvegarde = self.vue.afficher_sauvegardes(liste_sauvegarde)

        if nom_sauvegarde is None or nom_sauvegarde == "RETOUR":
            return

        # On récupère les données de la sauvegarde sélectionner par le joueur
        data_joueur = data[nom_sauvegarde]

        force_joueur = data_joueur["force_joueur"]
        pdv_joueur = data_joueur["point_de_vie_joueur"]
        inventaire_joueur = data_joueur["inventaire_joueur"]
        lieu_joueur = data_joueur["lieu_de_sauvegarde"]

        self.joueur = Joueur(nom=nom_sauvegarde, force=force_joueur, inventaire=inventaire_joueur, point_de_vie=pdv_joueur)

        for lieu in self.lieux:
            if lieu.nom == lieu_joueur:
                self.lieu_actuel = lieu
                break

        self.vue.afficher_description_lieu(self.lieu_actuel.nom, self.lieu_actuel.description)
        self.menu_parti()

    def changer_lieu(self):
        """Affiche la liste des lieux et propose au joueur de choisir une destination.
            Le joueur est avertie sur sa nouvelle destination et affiche la description du lieu"""
        
        lieu_choisi = self.vue.afficher_menu_changer_lieu(self.lieux, self.lieu_actuel.nom)

        # CTRL + C ou rester sur le lieu => return
        if lieu_choisi is None or lieu_choisi == self.lieu_actuel:
            return

        # Mise à jour du lieu actuel
        self.lieu_actuel = lieu_choisi

        # On informe le joueur de sa nouvelle destination
        self.vue.afficher_description_lieu(nom_lieu=self.lieu_actuel.nom, description_lieu=self.lieu_actuel.description)

    def prendre_ressource(self):
        """Affiche la liste des ressources disponible dans le lieu ou se trouve le joueur,
        Le joueur peux chosir d'ajouter ces ressources dans son inventaire"""

        resultat = self.vue.afficher_ressources_disponible(self.lieu_actuel.ressources)

        # Si le joueur choisi de faire retour sans rien récolter
        if resultat == "RETOUR" or resultat is None:
            return
        
        nom, qte = resultat

        # On met à jour la qté disponible du lieu
        self.lieu_actuel.ressources[nom] -= qte

        # Si le lieu est vidé de sa ressource on la supprime de son dict
        if self.lieu_actuel.ressources[nom] <= 0:
            del self.lieu_actuel.ressources[nom]

        # On ajoute la récolte dans l'inventaire du joueur
        if nom in self.joueur.inventaire:
            self.joueur.inventaire[nom] += qte
        else:
            self.joueur.inventaire[nom] = qte
    
    def inventaire(self):
        """Appelle la fonction de la class Vue pour afficher l'inventaire"""

        retour = self.vue.afficher_inventaire(self.joueur.inventaire)

        if retour == "RETOUR" or retour is None:
            return

    def attaquer(self):
        """Affiche le ou les ennemis avec leur niveau de force dans le lieu ou se trouve le joueur,
        le joueur peut choisir d'attaquer ou de battre en retraite"""

        print("Fonctionnalité 'Attaquer' à venir...")
    
    def sauvegarder(self):
        """Propose au joueur de valider la sauvegarde de sa partie en cours"""

        sauvegarde = {
            "force_joueur" : self.joueur.force,
            "point_de_vie_joueur" : self.joueur.point_de_vie,
            "inventaire_joueur" : self.joueur.inventaire,
            "lieu_de_sauvegarde" : self.lieu_actuel.nom
        }

        base_sauvegarde = {}

        if data_sauvegarde.exists():
            with open(file=data_sauvegarde, mode="r", encoding="utf-8") as fichier_lecture:
                try :
                    base_sauvegarde = json.load(fp=fichier_lecture)
                except json.JSONDecodeError:
                    base_sauvegarde = {}

        with open(data_sauvegarde, "w", encoding="utf-8") as fichier_ecriture:
            base_sauvegarde[self.joueur.nom] = sauvegarde
            json.dump(obj = base_sauvegarde, fp = fichier_ecriture ,indent=4)

        self.vue.informer_joueur(message="Donner sauvegarder avec succès !")

    def quitter(self):
        """Quitter le jeu, propose de sauvegarder avant de valider pour quitter"""

        print("Merci d'avoir joué ! À bientôt.")

        sys.exit()
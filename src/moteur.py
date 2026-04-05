from src.modeles import Joueur, Lieu, Personnage, RessourceJoueur, RessourceLieu, RessourcePersonnage
from src.vue import VueConsole
from src.erreur import NomInvalideError
import sys
from scripts.init_db import get_engine
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

engine = get_engine()

class Jeu:
    """Classe Jeu représentant une partie"""

    def __init__(self):
        """Initialisation de la classe Jeu"""
        self.joueur = None
        self.lieux = []
        self.lieu_actuel = None
        self.personnages = []
        self.vue = VueConsole()

    def charger_data(self):
        """Charger les données du jeu stocké sur le serveur postgres
        """

        with Session(engine) as session:
            self.lieux = session.scalars(
                select(Lieu)
                .options(joinedload(Lieu.inventaire).joinedload(RessourceLieu.ressource))
                .order_by(Lieu.id)
                ).unique().all()
            self.personnages = session.scalars(
                select(Personnage)
                .options(joinedload(Personnage.inventaire).joinedload(RessourcePersonnage.ressource))
                .order_by(Personnage.id)
                ).unique().all()
    
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

        liste_sauvegarde = []

        with Session(engine) as session:
            all_save = session.scalars(
                select(Joueur)
                .options(
                    joinedload(Joueur.lieu_actuel).joinedload(Lieu.inventaire).joinedload(RessourceLieu.ressource),
                    joinedload(Joueur.inventaire).joinedload(RessourceJoueur.ressource)
                )
                .order_by(Joueur.id)
                ).unique().all()
            
        for joueur in all_save:
            liste_sauvegarde.append(joueur.nom)

        if not liste_sauvegarde:
            self.vue.afficher_erreur("Aucune sauvegarde n'a été trouvée.")
            return

        # On affiche les sauvegardes au joueur
        nom_sauvegarde = self.vue.afficher_sauvegardes(liste_sauvegarde)

        if nom_sauvegarde is None or nom_sauvegarde == "RETOUR":
            return

        # On récupère les données de la sauvegarde sélectionner par le joueur
        for joueur in all_save:
            if joueur.nom == nom_sauvegarde:
                self.joueur = joueur
                self.lieu_actuel = self.joueur.lieu_actuel
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

        liste_inventaire = {ressource_lieu.ressource.nom: ressource_lieu.quantite for ressource_lieu in self.lieu_actuel.inventaire}

        resultat = self.vue.afficher_ressources_disponible(liste_inventaire)

        # Si le joueur choisi de faire retour sans rien récolter
        if resultat == "RETOUR" or resultat is None:
            return
        
        nom, qte = resultat
        ressource = None

        for r in self.lieu_actuel.inventaire:
            if r.ressource.nom == nom:
                ressource = r.ressource #Utiliser si le joueur n'a pas cette ressource dans son inventaire
                r.quantite -= qte
                if r.quantite <= 0:
                    self.lieu_actuel.inventaire.remove(r)
                break
        
        if ressource is None:
            self.vue.afficher_erreur("Ressource introuvable")
            return

        # On ajoute la récolte dans l'inventaire du joueur
        ressource_trouvee = False

        for r in self.joueur.inventaire:
            if r.ressource.nom == nom:
                r.quantite += qte
                ressource_trouvee = True
                break

        if not ressource_trouvee:
            # créer un nouveau RessourceJoueur
            id_joueur = self.joueur.id
            self.joueur.inventaire.append(
                RessourceJoueur(
                    quantite=qte, 
                    ressource = ressource, 
                    joueur = self.joueur)
            )
    
    def inventaire(self):
        """Appelle la fonction de la class Vue pour afficher l'inventaire"""

        inventaire_joueur = {ji.ressource.nom : ji.quantite for ji in self.joueur.inventaire}

        retour = self.vue.afficher_inventaire(inventaire_joueur)

        if retour == "RETOUR" or retour is None:
            return

    def attaquer(self):
        """Affiche le ou les ennemis avec leur niveau de force dans le lieu ou se trouve le joueur,
        le joueur peut choisir d'attaquer ou de battre en retraite"""

        print("Fonctionnalité 'Attaquer' à venir...")
    
    def sauvegarder(self):
        """
        Propose au joueur de valider la sauvegarde de sa partie en cours
        Ce qui est sauvegardé:
            - force_joueur
            - point_de_vie_joueur
            - inventaire_joueur
            - lieu_actuel
        """
        self.joueur.lieu_actuel = self.lieu_actuel

        with Session(engine) as session:
            session.merge(self.joueur)
            session.commit()

        self.vue.informer_joueur(message="Donner sauvegarder avec succès !")

    def quitter(self):
        """Quitter le jeu, propose de sauvegarder avant de valider pour quitter"""

        print("Merci d'avoir joué ! À bientôt.")

        sys.exit()
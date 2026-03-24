import questionary
from questionary import Choice

class VueConsole:

    def afficher_menu_accueil(self) -> str:
        """Affiche un menu au joueur pour créer une nouvelle partie ou charger une partie existante"""
        choix = questionary.select(
            "Bienvenue dans ce jeu d'aventure, que souhaites-tu faire ?",
            choices = [
                Choice(title = "1. Nouvelle partie", value = "1"),
                # Choice(title = "2. Charger une partie", value = "2")
            ]
        ).ask()

        return choix
    
    def demander_nom_joueur(self) -> str:
        """Demande la saisie du nom et renvoie le texte (nettoyé des espaces)"""
        return input("Ok, donne un nom à ton personnage : ").strip()

    def afficher_menu_action(self):
        """Affiche le menu d'action au joueur"""

        choix = questionary.select(
            "--- QUE VOULEZ-VOUS FAIRE ? ---",
            choices = [
                Choice(title = "1. Changer de lieu", value = "1"),
                # Choice(title = "2. Attaquer un ennemi", value = "2"),
                Choice(title = "3. Récupérer des ressources", value = "3"),
                Choice(title = "4. Afficher l'inventaire", value = "4"),
                Choice(title = "5. Sauvegarder la partie", value = "5"),
                Choice(title = "6. Quitter le jeu", value = "6")
            ]
        ).ask()

        return choix

    def afficher_erreur(self, message_erreur: str):
        """Affiche le message d'erreur"""
        print(f"❌ {message_erreur}")

    def afficher_description_lieu(self, nom_lieu: str, description_lieu: str):
        print()
        print(42 * "=")
        print(f"Vous avez voyagé vers : {nom_lieu}")
        print(f"📖 {description_lieu}")
        print(42 * "=")

    def afficher_menu_changer_lieu(self, liste_lieux: list[dict], nom_lieu_actuel: dict) -> dict:
        """Affiche les lieux disponible du jeu et le joueur sélectionne sa destination"""
        lieux = []

        for x, lieu in enumerate(liste_lieux):
            if lieu.nom == nom_lieu_actuel:
                lieux.append(Choice(title=f"Rester à {nom_lieu_actuel}", value = liste_lieux[x]))
            else:
                lieux.append(Choice(title=f"Voyager vers {lieu.nom}", value = liste_lieux[x]))
        
        choix = questionary.select(
            "Ou souhaites-tu aller ?",
            choices = lieux
        ).ask()

        return choix
    
    def afficher_ressources_disponible(self, ressources: dict) -> str:
        """Affiche les ressources que le joueur peut récolter"""
        mes_choix = []

        for nom, qte in ressources.items():
            mes_choix.append(Choice(title=f"Ressouce : {nom}, il y en a {qte}", value = (nom, qte)))

        if not mes_choix:
            mes_choix.append(Choice(title="Il n'y a plus de ressources disponible", value = "RETOUR"))
        else:
            mes_choix.append(Choice(title="❌ Ne rien prendre et revenir", value = "RETOUR"))

        choix = questionary.select(
            "Que souhaites-tu récolter ?",
            choices = mes_choix
        ).ask()

        return choix
    
    def afficher_inventaire(self, inventaire: dict) -> str:
        """Affiche l'inventaire du joueur"""
        
        print("\n🎒 === INVENTAIRE DU JOUEUR ===\n")
        
        if not inventaire:
            print("Ton sac à dos est vide !")
        else:
            for key, value in inventaire.items():
                print(f"  🔹 {key.capitalize()} : {value}")
                
        print("\n===============================\n")
        
        choix = questionary.select(
            "Appuie sur Entrée pour fermer l'inventaire",
            choices=[
                Choice(title="➡️  Retour", value="RETOUR")
            ]
        ).ask()

        return choix
    
    def informer_joueur(self, message: str):
        """Affiche un message au joueur"""
        print(message)
        
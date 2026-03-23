import questionary
from questionary import Choice

class VueConsole:

    def afficher_menu_accueil(self):
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
        print("\n--- QUE VOULEZ-VOUS FAIRE ? ---")
        print("1. Changer de lieu")
        print("2. Attaquer un ennemi")
        print("3. Récupérer des ressources")
        print("4. Afficher l'inventaire")
        print("5. Sauvegarder la partie")
        print("6. Quitter le jeu")

    def afficher_erreur(self, message_erreur: str):
        """Affiche le message d'erreur"""
        print(f"❌ {message_erreur}")

    def afficher_description_lieu(self, nom_lieu, description_lieu):
        print()
        print(42 * "=")
        print(f"Vous avez voyagé vers : {nom_lieu}")
        print(f"📖 {description_lieu}")
        print(42 * "=")

    def afficher_menu_changer_lieu(self, liste_lieux, nom_lieu_actuel):
        print("Ou veux-tu aller ?")

        # Affiche les lieux avec un index
        for x, lieu in enumerate(liste_lieux):
            if lieu.nom == nom_lieu_actuel:
                print(f"{x + 1}. {lieu.nom} (Votre position)")
            else:
                print(f"{x + 1}. {lieu.nom}")
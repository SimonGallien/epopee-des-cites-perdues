from src.moteur import Jeu

def main():
    ma_partie = Jeu()
    ma_partie.charger_data()
    ma_partie.menu_accueil()


if __name__ == "__main__":
    main()

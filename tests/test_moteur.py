from src.moteur import Jeu
from unittest.mock import MagicMock, patch
    
def test_charger_data():

    # On crée une fausse partie
    ma_partie = Jeu()

    # On crée de faux objets
    faux_lieu = MagicMock()
    faux_personnage = MagicMock()

    # On remplace Session dans moteur.py par un faux
    with patch("src.moteur.Session") as FausseSession:

        # Session(engine) retourne un faux objet
        fausse_instance = FausseSession.return_value

        # "with Session() as session" → __enter__ retourne le faux session
        fausse_session = fausse_instance.__enter__.return_value

        # Premier appel à scalars() → retourne les lieux
        # Deuxième appel à scalars() → retourne les personnages
        fausse_session.scalars.return_value.unique.return_value.all.side_effect = [
            [faux_lieu],
            [faux_personnage]
        ]

        # On appelle la vraie fonction
        ma_partie.charger_data()

    # On vérifie que les lieux et personnages sont bien chargés
    assert len(ma_partie.lieux) == 1
    assert len(ma_partie.personnages) == 1

def test_menu_jeu_choix_1_appelle_nouveau_joueur():
    """Vérifie que taper '1' à l'accueil déclenche bien la création de joueur"""
    
    # Préparation d'une fausse partie pour le test
    ma_partie = Jeu()
    ## Une fausse vue
    ma_partie.vue.afficher_menu_accueil = MagicMock(return_value="1")
    ## Un faux joueur
    ma_partie.nouveau_joueur = MagicMock()
    ## Une fausse sauvegarde
    ma_partie.charger_une_sauvegarde = MagicMock()
    
    # On test la fonction qui doit appeler la fonction nouveau_joueur()
    ma_partie.menu_accueil()

    # On vérifie que la fonction a bien été appelé
    ma_partie.nouveau_joueur.assert_called_once()
    # On vérifie aussi que la fonction charger_une_sauvegarde n'a pas été appelé
    ma_partie.charger_une_sauvegarde.assert_not_called()

def test_menu_jeu_choix_2_appelle_charger_une_sauvegarde():
    """Vérifie que taper '2' à l'accueil déclenche bien le chargement d'une sauvegarde"""
    
    # Préparation d'une fausse partie pour le test
    ma_partie = Jeu()
    ## Une fausse vue
    ma_partie.vue.afficher_menu_accueil = MagicMock(return_value="2")
    ## Un faux joueur
    ma_partie.nouveau_joueur = MagicMock()
    ## Une fausse sauvegarde
    ma_partie.charger_une_sauvegarde = MagicMock()
    
    # On test la fonction qui doit appeler la fonction nouveau_joueur()
    ma_partie.menu_accueil()

    # On vérifie que la fonction a bien été appelé
    ma_partie.charger_une_sauvegarde.assert_called_once()
    # On vérifie aussi que la fonction nouveau_joueur n'a pas été appelé
    ma_partie.nouveau_joueur.assert_not_called()
from src.moteur import Jeu
from src.modeles import Lieu, Personnage, Ressource
from unittest.mock import MagicMock

def test_charger_donnes():
    """Test si la fonction instencie bien le contenu du json en Objet de la bonne classe"""
    
    ma_partie = Jeu()
    ma_partie.charger_donnes()

    assert len(ma_partie.lieux) > 0
    assert len(ma_partie.personnages) > 0
    assert len(ma_partie.ressources) > 0

    assert all(isinstance(lieu, Lieu) for lieu in ma_partie.lieux)
    assert all(isinstance(personnage, Personnage) for personnage in ma_partie.personnages)
    assert all(isinstance(ressource, Ressource) for ressource in ma_partie.ressources)

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
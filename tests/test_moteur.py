from src.moteur import Jeu
from src.modeles import Lieu, Personnage, Ressource

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

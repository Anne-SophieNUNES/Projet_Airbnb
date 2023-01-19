"""DESCRIPTION :

Librairie qui permet de tester la fonction de la librairie affichage.
"""

from final.lib_predicteur import meilleur_modele, prediction, choix_annonces


def test_meilleur_modele():
    resultat = meilleur_modele("toulouse.json")
    assert resultat != []


def test_prediction():
    df = prediction("toulouse.json")
    assert len(df) != 0


def test_choix_annonces():
    resultat = choix_annonces("toulouse.json")
    assert resultat != []

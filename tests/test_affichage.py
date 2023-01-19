"""DESCRIPTION :

Librairie qui permet de tester la fonction de la librairie affichage.
"""

from final.lib_affichage import affichage


def test_affichage():
    resultat = affichage("toulouse.json")
    assert resultat != ""

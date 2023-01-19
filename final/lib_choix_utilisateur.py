"""DESCRIPTION :
Une librarie qui permet de prendre en compte les choix de l'utilisateur. 
"""

import datetime
from serde import serde


def _nb_valide(nb_adulte: int, nb_enfant: int) -> bool:
    """Permet de vérifer le nombre d'adulte et d'enfant par voyage.
    Pour lancer une recherche Airbnb il faut au minimum avoir 1 adulte, et au
    maximum avoir 16 voyageurs (adulte et enfant).

    Exemple :
    >>> _nb_valide(1,0)
    True

    >>> _nb_valide(0,1)
    False

    >>> _nb_valide(16,1)
    False
    """
    if nb_adulte != 0:
        if nb_enfant + nb_adulte <= 16:
            return True
        return False
    return False


def _ecriture_dates(date_arrivee: str, date_depart: str) -> bool:
    """Permet de vérifier l'écriture de la date d'arrivée et de la date de départ du séjour.
    La fonction vérifie que :
        - la date de départ soit bien ultérieure à la date d'arrivée,
        - la date d'arrivée et la date de départ soient bien écrites sous la forme AAAA/MM/JJ.

    Exemple :
     >>> _ecriture_dates("2023/02/10", "2023/02/12")
     True

     >>> _ecriture_dates("2023/02-10", "2023/02/12")
     False

     >>> _ecriture_dates("2023/02/12", "2023/02/10")
     False

     >>> _ecriture_dates("2023/02/10", "20233/02/10")
     False

     >>> _ecriture_dates("2023/02", "2023/02/12")
     False
    """
    if len(date_arrivee) == 10 and len(date_depart) == 10:
        if "/" == date_arrivee[4] and "/" == date_arrivee[-3]:
            if "/" == date_depart[4] and "/" == date_depart[-3]:
                d_arriver = datetime.datetime.strptime(date_arrivee, "%Y/%m/%d").date()
                d_depart = datetime.datetime.strptime(date_depart, "%Y/%m/%d").date()

                if d_depart > d_arriver:
                    return True
                return False
            return False
        return False
    return False


@serde
class Choix:
    ville: str
    date_arrivee: str
    date_depart: str
    nb_adulte: int
    nb_enfant: int

    def __post_init__(self):
        if _nb_valide(self.nb_adulte, self.nb_enfant) == False:
            raise ValueError(
                "Le nombre d'enfant(s) et d'adulte(s) doivent être valides."
            )
        if _ecriture_dates(self.date_arrivee, self.date_depart) == False:
            raise ValueError("Les dates doivent être écrites comme AAAA/MM/JJ")

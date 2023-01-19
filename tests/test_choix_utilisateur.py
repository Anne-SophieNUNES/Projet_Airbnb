"""Description.

Tests automatiques de la librairie lib_choix_utilisateur.py
"""

import pytest
from final.lib_choix_utilisateur import Choix, _nb_valide, _ecriture_dates


def test_nb_valide():
    assert _nb_valide(5, 6)
    assert _nb_valide(1, 2)
    assert not _nb_valide(16, 1)


def test_ecriture_dates():
    assert _ecriture_dates("2000/01/23", "2001/01/29")
    assert _ecriture_dates("2018/07/15", "2019/07/15")
    assert not _ecriture_dates("20000/01/06", "2000/02/1")


def test_ecriture_dates_false():
    assert not _ecriture_dates("2000/01/", "2000/02/1")


def test_choix_initialisation():
    choix = Choix(
        ville="Paris",
        date_arrivee="2022/02/10",
        date_depart="2022/02/12",
        nb_adulte=1,
        nb_enfant=0,
    )
    isinstance(choix, Choix)


def test_choix_initialisation_nb_valide():
    with pytest.raises(ValueError):
        Choix(
            ville="Paris",
            date_arrivee="2022/02/10",
            date_depart="2022/02/12",
            nb_adulte=0,
            nb_enfant=1,
        )


def test_choix_initialisation_nb_validess():
    with pytest.raises(ValueError):
        Choix(
            ville="Paris",
            date_arrivee="2022/02/10",
            date_depart="2022/02/12",
            nb_adulte=2,
            nb_enfant=16,
        )


def test_choix_initialisation_dates_valide():
    with pytest.raises(ValueError):
        Choix(
            ville="Paris",
            date_arrivee="2022/02/12",
            date_depart="2022/02/10",
            nb_adulte=1,
            nb_enfant=0,
        )


def test_choix_initialisation_ecriture_dates_valides():
    with pytest.raises(ValueError):
        Choix(
            ville="Paris",
            date_arrivee="20220/02/12",
            date_depart="2022/02/10",
            nb_adulte=1,
            nb_enfant=0,
        )


def test_choix_initialisation_ecriture_dates_valide_false():
    with pytest.raises(ValueError):
        Choix(
            ville="Paris",
            date_arrivee="2022/02",
            date_depart="2022/02/01",
            nb_adulte=1,
            nb_enfant=0,
        )


def test_choix_initialisation_ecriture_dates_valide_falses():
    with pytest.raises(ValueError):
        Choix(
            ville="Paris",
            date_arrivee="2023/02/10",
            date_depart="2023/02012",
            nb_adulte=1,
            nb_enfant=0,
        )


def test_choix_initialisation_ecriture_dates_valide_falsess():
    with pytest.raises(ValueError):
        Choix(
            ville="Paris",
            date_arrivee="2023/02-10",
            date_depart="2023/02/12",
            nb_adulte=1,
            nb_enfant=0,
        )

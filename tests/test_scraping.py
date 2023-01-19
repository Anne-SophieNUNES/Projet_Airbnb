"""DESCRIPTION :

Librairie qui permet de tester les fonctions de la librairie scraping.
"""

from final.lib_choix_utilisateur import Choix
from final.lib_scraping import url, annonces, stock_donnees, scraping


def test_url():
    resultat = url(Choix("Paris", "2023/02/10", "2023/02/12", 1, 0))
    assert (
        resultat
        == "https://www.airbnb.fr/s/Paris/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=2&date_picker_type=calendar&checkin=2023-02-10&checkout=2023-02-12&adults=1&source=structured_search_input_header&search_type=search_query"
    )


def test_url_valide():
    resultat = url(Choix("Paris", "2023/02/10", "2023/02/12", 1, 1))
    assert (
        resultat
        == "https://www.airbnb.fr/s/Paris/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=2&date_picker_type=calendar&checkin=2023-02-10&checkout=2023-02-12&adults=1&children=1&source=structured_search_input_header&search_type=search_query"
    )


def test_url_false():
    resultat = url(Choix("Paris", "2023/02/10", "2023/02/12", 1, 0))
    assert (
        resultat
        != "https://www.airbnb.fr/s/Tours/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=2&date_picker_type=calendar&checkin=2023-02-10&checkout=2023-02-12&adults=1&source=structured_search_input_header&search_type=search_query"
    )


def test_annonces_false():
    resultat = annonces(Choix("Nixéville-Blercourt", "2023/02/10", "2023/02/12", 16, 0))
    assert resultat != []


def test_scraping_false():
    resultat = scraping(
        Choix("Nixéville-Blercourt, France", "2023/02/10", "2023/02/12", 16, 0)
    )
    assert resultat != []


def test_stock_donnees():
    resultat = stock_donnees(
        Choix("Nixéville-Blercourt", "2023/02/10", "2023/02/12", 16, 0)
    )
    assert str(type(resultat)) == "<class '_io.TextIOWrapper'>"


def test_stock_donnees_false():
    resultat = stock_donnees(
        Choix("Nixéville-Blercourt", "2023/02/10", "2023/02/12", 16, 0)
    )
    assert str(type(resultat)) != "_io.TextIOWrapper"

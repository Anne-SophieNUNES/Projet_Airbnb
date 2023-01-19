"""DESCRIPTION : 

Librairie permettant de récupérer les données des annonces sur les sites Airbnb.
"""

from .lib_choix_utilisateur import Choix
from .lib_annonce import Annonce
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import List
import json
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains


def url(choix: Choix) -> str:
    """Fonction qui permet de générer l'url correspondant aux critères de recherche de l'utilisateur.

    Exemple :
    >>> url(Choix('Paris', '2023/02/10', '2023/02/12', 1, 0))
    'https://www.airbnb.fr/s/Paris/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=2&date_picker_type=calendar&checkin=2023-02-10&checkout=2023-02-12&adults=1&source=structured_search_input_header&search_type=search_query'
    """
    ville = choix.ville
    date_arrivee = choix.date_arrivee
    date_depart = choix.date_depart
    nb_adulte = choix.nb_adulte
    nb_enfant = choix.nb_enfant
    date_arrivee = datetime.datetime.strptime(date_arrivee, "%Y/%m/%d").date()
    date_depart = datetime.datetime.strptime(date_depart, "%Y/%m/%d").date()
    if nb_enfant == 0:
        url_page = f"https://www.airbnb.fr/s/{ville}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=2&date_picker_type=calendar&checkin={date_arrivee}&checkout={date_depart}&adults={nb_adulte}&source=structured_search_input_header&search_type=search_query"
    else:
        nb_enfant = f"&children={nb_enfant}"
        url_page = f"https://www.airbnb.fr/s/{ville}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=2&date_picker_type=calendar&checkin={date_arrivee}&checkout={date_depart}&adults={nb_adulte}{nb_enfant}&source=structured_search_input_header&search_type=search_query"
    return url_page


def annonces(choix: Choix) -> list[str]:
    """Fonction qui permet de récupérer dans une liste toutes les annonces liées à la recherche de l'utilisateur.

    Exemple :
    >>> annonces(Choix("Nixéville-Blercourt", "2023/02/10", "2023/02/12", 16,0))
    ['https://www.airbnb.fr/rooms/50933513?adults=16&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000', 'https://www.airbnb.fr/rooms/37054365?adults=16&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000', 'https://www.airbnb.fr/rooms/43583514?adults=16&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000', 'https://www.airbnb.fr/rooms/557678697827102729?adults=16&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000', 'https://www.airbnb.fr/rooms/16716773?adults=16&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000', 'https://www.airbnb.fr/rooms/553439618608441289?adults=16&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000', 'https://www.airbnb.fr/rooms/15696829?adults=16&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000', 'https://www.airbnb.fr/rooms/38567448?adults=16&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000', 'https://www.airbnb.fr/rooms/695667446993367263?adults=16&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000', 'https://www.airbnb.fr/rooms/50590436?adults=16&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000', 'https://www.airbnb.fr/rooms/599060927465519912?adults=16&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000']
    """
    liens_page = []
    liste_annonces = []
    liens_annonces = []
    url_page = url(
        Choix(
            choix.ville,
            choix.date_arrivee,
            choix.date_depart,
            choix.nb_adulte,
            choix.nb_enfant,
        )
    )
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(url_page)
    time.sleep(20)

    consent01_button = driver.find_element(by=By.CLASS_NAME, value="_148dgdpk")
    consent01_button.click()
    time.sleep(2)
    liens_page.append(url_page)

    derniere_page = True

    while derniere_page:
        lien = []
        lien = driver.find_elements(by=By.XPATH, value="//*[@itemprop='url']")
        for ii in lien:
            liste_annonces.append(ii.get_attribute("content"))

        try:
            next_page = driver.find_element(
                by=By.XPATH, value="//a[@aria-label='Suivant']"
            )
            is_last_page = next_page.get_attribute("href")
            time.sleep(5)
            liens_page.append(is_last_page)

            next_page.click()
            time.sleep(5)
        except:
            derniere_page = False
            driver.close()

    for k in liste_annonces:
        liens_annonces.append(f"https://{k}")
    return liens_annonces


def infos_utiles(extension) -> list[str]:
    """Sous fonction appartenant à la fonction scraping.
    Cette fonction permet de récupérer des caractéristiques des annonces telles que le nombre de voyageurs et le nombre de salle de bain.
    """
    try:
        nom_voyageur = extension.find_element(
            by=By.XPATH, value='//*[@class="_jro6t0"]/div[1]/ol/li[1]/span[1]'
        ).text
    except:
        nom_voyageur = []
    try:
        nom_type_bien = extension.find_element(
            by=By.XPATH, value='//*[@class="_jro6t0"]/div[1]/ol/li[2]/span[2]'
        ).text
        if "Studio" in nom_type_bien[0]:
            bien = "Studio"
        else:
            bien = "chambre"
    except:
        nom_type_bien = []
    try:
        nom_nb_lit = extension.find_element(
            by=By.XPATH, value='//*[@class="_jro6t0"]/div[1]/ol/li[3]/span[2]'
        ).text
    except:
        nom_nb_lit = []
    try:
        nom_nb_salle_bain = extension.find_element(
            by=By.XPATH, value='//*[@class="_jro6t0"]/div[1]/ol/li[4]/span[2]'
        ).text
    except:
        nom_nb_salle_bain = []
    try:
        if len(nom_nb_salle_bain[0]) == 1:
            voyageur = nom_voyageur
            type_bien = nom_type_bien
            nb_lit = nom_nb_lit
            nb_salle_bain = nom_nb_salle_bain
    except:
        try:
            if len(nom_nb_lit[0]) == 1:
                if "lit" in nom_nb_lit[0]:
                    voyageur = nom_voyageur
                    type_bien = nom_type_bien
                    nb_lit = nom_nb_lit
                    nb_salle_bain = "NA"
                else:
                    voyageur = nom_voyageur
                    type_bien = nom_type_bien
                    nb_salle_bain = nom_nb_lit
                    nb_lit = "NA"
        except:
            try:
                if len(nom_type_bien[0]) == 1:
                    if bien in nom_type_bien[0]:
                        voyageur = nom_voyageur
                        type_bien = nom_type_bien
                        nb_lit = "NA"
                        nb_salle_bain = "NA"
                    elif "voyageur" in nom_voyageur[0] and "lit" in nom_type_bien[0]:
                        voyageur = nom_voyageur
                        type_bien = "NA"
                        nb_lit = nom_type_bien
                        nb_salle_bain = "NA"
                    elif "voyageur" in nom_voyageur[0] and "bain" in nom_type_bien[0]:
                        voyageur = nom_voyageur[0]
                        type_bien = "NA"
                        nb_lit = "NA"
                        nb_salle_bain = nom_type_bien
                    elif bien in nom_voyageur[0] and "lit" in nom_type_bien[0]:
                        voyageur = "NA"
                        type_bien = nom_voyageur
                        nb_lit = nom_type_bien
                        nb_salle_bain = "NA"
                    elif bien in nom_voyageur[0] and "bain" in nom_type_bien[0]:
                        voyageur = "NA"
                        type_bien = nom_voyageur
                        nb_lit = "NA"
                        nb_salle_bain = nom_type_bien
                    elif "lit" in nom_voyageur[0] and "bain" in nom_type_bien[0]:
                        voyageur = "NA"
                        type_bien = "NA"
                        nb_lit = nom_voyageur
                        nb_salle_bain = nom_type_bien
            except:
                try:
                    if len(nom_voyageur[0]) == 1:
                        if "voyageur" in nom_voyageur[0]:
                            voyageur = nom_voyageur
                            type_bien = "NA"
                            nb_salle_bain = "NA"
                            nb_lit = "NA"
                        elif bien in nom_voyageur[0]:
                            voyageur = "NA"
                            type_bien = nom_voyageur
                            nb_salle_bain = "NA"
                            nb_lit = "NA"
                        elif "lit" in nom_voyageur[0]:
                            voyageur = "NA"
                            type_bien = "NA"
                            nb_salle_bain = "NA"
                            nb_lit = nom_voyageur
                        elif "bain" in nom_voyageur[0]:
                            voyageur = "NA"
                            type_bien = "NA"
                            nb_salle_bain = nom_voyageur
                            nb_lit = "NA"
                except:
                    voyageur = "NA"
                    type_bien = "NA"
                    nb_salle_bain = "NA"
                    nb_lit = "NA"
    return [voyageur, type_bien, nb_salle_bain, nb_lit]


def recup_costsName(extension) -> list[str]:
    """Sous fonction appartenant à la fonction scraping.
    Cette fonction permet de récupérer des caractéristiques des annonces.
    """
    try:
        nom_detail = extension.find_element(
            by=By.XPATH, value='//*[@class="_18x0pkv"]/div[1]/span/div/button/div'
        ).text
    except:
        nom_detail = []
    try:
        nom_offre_speciale = extension.find_element(
            by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span/div/button/div'
        ).text
        offre = []
        if "Offre spéciale" in nom_offre_speciale:
            offre = "Offre spéciale"
        elif "Réduction" in nom_offre_speciale:
            offre = "Réduction"
        else:
            offre = "vide"
    except:
        nom_offre_speciale = []
    try:
        nom_menage = extension.find_element(
            by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span/div/button/div'
        ).text
    except:
        nom_menage = []
    try:
        nom_service = extension.find_element(
            by=By.XPATH, value='//*[@class="_18x0pkv"]/div[4]/span/div/button/div'
        ).text
    except:
        nom_service = []
    try:
        nom_taxes = extension.find_element(
            by=By.XPATH, value='//*[@class="_18x0pkv"]/div[5]/span/div/button/div'
        ).text
    except:
        nom_taxes = []
    return [nom_detail, nom_offre_speciale, nom_menage, nom_service, nom_taxes, offre]


def recup_5costs(extension, nom_taxes) -> list[str]:
    """Fonction qui permet de récupérer les informations concernant les coûts de location tels que les frais de ménage et les taxes.
    Cependant, chaque annonce ne comporte pas le même nombre de coûts. La fonction permet de vérifier si on récupère le "bon coût".
    """
    if len(nom_taxes[0]) == 1:
        detail = extension.find_element(
            by=By.XPATH, value='//*[@class="_18x0pkv"]/div[1]/span[2]'
        ).text
        offre_speciale = extension.find_element(
            by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
        ).text
        frais_menage = extension.find_element(
            by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
        ).text
        frais_service = extension.find_element(
            by=By.XPATH, value='//*[@class="_18x0pkv"]/div[4]/span[2]'
        ).text
        taxes = extension.find_element(
            by=By.XPATH, value='//*[@class="_18x0pkv"]/div[5]/span[2]'
        ).text
    return [detail, offre_speciale, frais_menage, frais_service, taxes]


def recup_4costs(
    extension, nom_detail, nom_offre_speciale, nom_menage, nom_service, offre
) -> list[str]:
    """Fonction qui permet de récupérer les informations concernant les coûts de location tels que les frais de ménage et les taxes.
    Cependant, chaque annonce ne comporte pas le même nombre de coûts. La fonction permet de vérifier si on récupère le "bon coût".
    """
    if len(nom_service[0]) == 1:
        if "service" in nom_service:
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[4]/span[2]'
            ).text
            taxes = "NA"
        elif (
            "nuit" in nom_detail
            and "ménage" in nom_offre_speciale
            and "service" in nom_menage
            and "Taxes" in nom_service
        ):
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[4]/span[2]'
            ).text
            offre_speciale = "NA"
        elif (
            "nuit" in nom_detail
            and offre in nom_offre_speciale
            and "ménage" in nom_menage
            and "Taxes" in nom_service
        ):
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[4]/span[2]'
            ).text
            frais_service = "NA"
        elif (
            offre in nom_detail
            and "ménage" in nom_offre_speciale
            and "service" in nom_menage
            and "Taxes" in nom_service
        ):
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[4]/span[2]'
            ).text
            detail = "NA"
        elif (
            "nuit" in nom_detail
            and offre in nom_offre_speciale
            and "service" in nom_menage
            and "Taxes" in nom_service
        ):
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[4]/span[2]'
            ).text
            frais_ménage = "NA"
    return [detail, offre_speciale, frais_menage, frais_service, taxes]


def recup_3costs(
    extension, nom_detail, nom_offre_speciale, nom_menage, offre
) -> list[str]:
    """Fonction qui permet de récupérer les informations concernant les coûts de location tels que les frais de ménage et les taxes.
    Cependant, chaque annonce ne comporte pas le même nombre de coûts. La fonction permet de vérifier si on récupère le "bon coût".
    """
    if len(nom_menage[0]) == 1:
        if "ménage" in nom_menage:
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            frais_service = "NA"
            taxes = "NA"
        elif (
            "nuit" in nom_detail
            and offre in nom_offre_speciale
            and "service" in nom_menage
        ):
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            frais_menage = "NA"
            taxes = "NA"
        elif (
            "nuit" in nom_detail
            and offre in nom_offre_speciale
            and "Taxes" in nom_menage
        ):
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            frais_menage = "NA"
            frais_service = "NA"
        elif (
            offre in nom_detail
            and "ménage" in nom_offre_speciale
            and "service" in nom_menage
        ):
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            detail = "NA"
            taxes = "NA"
        elif (
            offre in nom_detail
            and "service" in nom_offre_speciale
            and "Taxes" in nom_menage
        ):
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            detail = "NA"
            frais_menage = "NA"
        elif (
            "ménage" in nom_detail
            and "service" in nom_offre_speciale
            and "Taxes" in nom_menage
        ):
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            detail = "NA"
            offre_speciale = "NA"
        elif (
            "nuit" in nom_detail
            and "ménage" in nom_offre_speciale
            and "Taxes" in nom_menage
        ):
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            offre_speciale = "NA"
            frais_service = "NA"
        elif (
            "nuit" in nom_detail
            and "ménage" in nom_offre_speciale
            and "service" in nom_menage
        ):
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            offre_speciale = "NA"
            taxes = "NA"
        elif (
            offre in nom_detail
            and "ménage" in nom_offre_speciale
            and "Taxes" in nom_menage
        ):
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            detail = "NA"
            frais_service = "NA"
        elif (
            "nuit" in nom_detail
            and "service" in nom_offre_speciale
            and "Taxes" in nom_menage
        ):
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[3]/span[2]'
            ).text
            offre_speciale = "NA"
            frais_menage = "NA"
    return [detail, offre_speciale, frais_menage, frais_service, taxes]


def recup_2costs(extension, nom_detail, nom_offre_speciale, offre) -> list[str]:
    """Fonction qui permet de récupérer les informations concernant les coûts de location tels que les frais de ménage et les taxes.
    Cependant, chaque annonce ne comporte pas le même nombre de coûts. La fonction permet de vérifier si on récupère le "bon coût".
    """
    if len(nom_offre_speciale[0]) == 1:
        if offre in nom_offre_speciale:
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            frais_menage = "NA"
            frais_service = "NA"
            taxes = "NA"
        elif "nuit" in nom_detail and "ménage" in nom_offre_speciale:
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            offre_speciale = "NA"
            frais_service = "NA"
            taxes = "NA"
        elif "nuit" in nom_detail and "service" in nom_offre_speciale:
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            offre_speciale = "NA"
            frais_menage = "NA"
            taxes = "NA"
        elif "nuit" in nom_detail and "Taxes" in nom_offre_speciale:
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            offre_speciale = "NA"
            frais_menage = "NA"
            frais_service = "NA"
        elif offre in nom_detail and "ménage" in nom_offre_speciale:
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            detail = "NA"
            frais_service = "NA"
            taxes = "NA"
        elif offre in nom_detail and "service" in nom_offre_speciale:
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            detail = "NA"
            frais_menage = "NA"
            taxes = "NA"
        elif offre in nom_detail and "Taxes" in nom_offre_speciale:
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            detail = "NA"
            frais_menage = "NA"
            frais_service = "NA"
        elif "ménage" in nom_detail and "service" in nom_offre_speciale:
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            detail = "NA"
            offre_speciale = "NA"
            taxes = "NA"
        elif "ménage" in nom_detail and "Taxes" in nom_offre_speciale:
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            detail = "NA"
            offre_speciale = "NA"
            frais_service = "NA"
        elif "service" in nom_detail and "Taxes" in nom_offre_speciale:
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div[2]/span[2]'
            ).text
            detail = "NA"
            offre_speciale = "NA"
            frais_menage = "NA"
    return [detail, offre_speciale, frais_menage, frais_service, taxes]


def recup_1cost(extension, nom_detail, offre) -> list[str]:
    """Fonction qui permet de récupérer les informations concernant les coûts de location tels que les frais de ménage et les taxes.
    Cependant, chaque annonce ne comporte pas le même nombre de coûts. La fonction permet de vérifier si on récupère le "bon coût".
    """
    if len(nom_detail[0]) == 1:
        if "nuit" in nom_detail:
            detail = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            offre_speciale = "NA"
            frais_menage = "NA"
            frais_service = "NA"
            taxes = "NA"

        elif offre in nom_detail:
            offre_speciale = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            detail = "NA"
            frais_menage = "NA"
            frais_service = "NA"
            taxes = "NA"

        elif "ménage" in nom_detail:
            frais_menage = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            detail = "NA"
            offre_speciale = "NA"
            frais_service = "NA"
            taxes = "NA"

        elif "service" in nom_detail:
            frais_service = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            detail = "NA"
            offre_speciale = "NA"
            frais_menage = "NA"
            taxes = "NA"

        elif "Taxes" in nom_detail:
            taxes = extension.find_element(
                by=By.XPATH, value='//*[@class="_18x0pkv"]/div/span[2]'
            ).text
            detail = "NA"
            offre_speciale = "NA"
            frais_menage = "NA"
            frais_service = "NA"
    return [detail, offre_speciale, frais_menage, frais_service, taxes]


def avis(extension) -> list[str]:
    """Sous fonction appartenant à la fonction scraping.
    Cette fonction permet de récupérer des caractéristiques des annonces telles que la note de l'annonce, les commentaires des utilisateurs d'Airbnb et les notes associées aux services (propreté, communication, accueil).
    """
    try:
        etoiles = extension.find_element(
            by=By.XPATH, value='//*[@class="_klarpw"]/span/span[2]'
        ).text
    except:
        etoiles = "NA"
    try:
        proprete = extension.find_element(
            by=By.XPATH,
            value='//*[@class="r1f90fvr dir dir-ltr"]/div/div[1]/div/div/div[2]/span',
        ).text
    except:
        proprete = "NA"
    try:
        precision = extension.find_element(
            by=By.XPATH,
            value='//*[@class="r1f90fvr dir dir-ltr"]/div/div[2]/div/div/div[2]/span',
        ).text
    except:
        precision = "NA"
    try:
        communication = extension.find_element(
            by=By.XPATH,
            value='//*[@class="r1f90fvr dir dir-ltr"]/div/div[3]/div/div/div[2]/span',
        ).text
    except:
        communication = "NA"
    try:
        emplacement = extension.find_element(
            by=By.XPATH,
            value='//*[@class="r1f90fvr dir dir-ltr"]/div/div[4]/div/div/div[2]/span',
        ).text
    except:
        emplacement = "NA"
    try:
        arrivee = extension.find_element(
            by=By.XPATH,
            value='//*[@class="r1f90fvr dir dir-ltr"]/div/div[5]/div/div/div[2]/span',
        ).text
    except:
        arrivee = "NA"
    try:
        qualite_prix = extension.find_element(
            by=By.XPATH,
            value='//*[@class="r1f90fvr dir dir-ltr"]/div/div[6]/div/div/div[2]/span',
        ).text
    except:
        qualite_prix = "NA"
    try:
        commentaires = extension.find_element(
            by=By.XPATH, value='//*[@class="_klarpw"]/span/button/span'
        ).text
    except:
        commentaires = "NA"
    return [
        etoiles,
        proprete,
        precision,
        communication,
        emplacement,
        arrivee,
        qualite_prix,
        commentaires,
    ]


def scraping(choix: Choix) -> list[dict]:
    """Fonction qui permet de scrapper les données.

    Explication:
    Les critères de l'utilisateur sont stockés dans un fichier json. Ces données sont ensuite récupérées par la fonction url() qui génère
    le lien de la destination. Les liens des différentes annonces possibles sont récupérées grâce à la fonction annonces().
    La fonction sraping() qui est découpée en 8 sous fonctions permet de parcourir chaque lien d'annonces et d'extraire les caractéristiques de celles-ci.

    Chaque caractéristique est récupérée et stockée grâce à la dataclass Annonce. Puisque chaque annonce
    est un dictionnaire, la fonction scraping renvoie une liste de dictionnaires.


    Exemple :
    >>> scraping(Choix("Nixéville-Blercourt", "2023/02/10", "2023/02/12", 16,0))
    [{'nom': 'Maison de maître 20 pers avec piscine', 'adresse': 'Bairon et ses environs, Grand Est, France', 'info': 'Logement entier : logement ⸱ Chez Sylvie', 'voyageur': '16 voyageurs et plus', 'type_bien': '7 chambres', 'nb_lit': '14 lits', 'nb_salle_bain': '6 salles de bain', 'prix_nuit': '885 € par nuit', 'detail': '1\u202f770 €', 'offre_speciale': 'NA', 'frais_menage': 'NA', 'frais_service': '300 €', 'taxes': '49 €', 'prix_total': '2\u202f119 €', 'etoiles': '4,92 ·', 'commentaires': '36 commentaires', 'proprete': '5,0', 'precision': '4,9', 'communication': '5,0', 'emplacement': '4,4', 'arrivee': '5,0', 'qualite_prix': '4,8', 'lien': 'https://www.airbnb.fr/rooms/50933513?adults=16&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000'}]
    """
    newListDict = []
    liens = annonces(
        Choix(
            choix.ville,
            choix.date_arrivee,
            choix.date_depart,
            choix.nb_adulte,
            choix.nb_enfant,
        )
    )
    time.sleep(5)
    for i in liens:
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get(i)
        time.sleep(20)

        try:
            trad_button = driver.find_element(
                by=By.XPATH, value='//*[@class="_1piuevz"]/button'
            )
            trad_button.click()
            time.sleep(5)
        except NoSuchElementException:
            pass

        consent_button = driver.find_element(by=By.CLASS_NAME, value="_148dgdpk")
        consent_button.click()
        time.sleep(5)

        try:
            action = ActionChains(driver)
            action.move_to_element(
                driver.find_element(by=By.XPATH, value='//*[@class="_1sl8tba"]/button')
            )
            action.perform()
            time.sleep(5)

            cliquer_affiche_detail = driver.find_element(
                by=By.XPATH, value='//*[@class="_ud8a1c"]/div[2]/div/section/button'
            )
            cliquer_affiche_detail.click()
            time.sleep(20)
        except NoSuchElementException:
            pass

        try:
            disponibilite = driver.find_element(
                by=By.XPATH, value='//*[@class="e17hsan dir dir-ltr"]/div[1]'
            )
            driver.close()
            pass
        except:
            pas_encore_dispo = driver.find_element(
                by=By.XPATH, value='//*[@class="_qqb2vcb"]/span[2]'
            ).text
            if pas_encore_dispo != "Réserver":
                driver.close()
                pass
            else:
                lien = i
                nom = driver.find_element(by=By.CLASS_NAME, value="_fecoyn4").text
                adresse = driver.find_element(by=By.CLASS_NAME, value="_9xiloll").text
                info = driver.find_element(
                    by=By.XPATH, value='//*[@class="_jro6t0"]/div[1]/div/h2'
                ).text
                infos = infos_utiles(driver)
                voyageur = infos[0]
                type_bien = infos[1]
                nb_salle_bain = infos[2]
                nb_lit = infos[3]
                prix_nuit = driver.find_element(
                    by=By.XPATH, value='//*[@class="_c7v1se"]/div[1]/div/span/span'
                ).text
                prix_total = driver.find_element(
                    by=By.XPATH, value='//*[@class="_1qh0b5n"]/span[2]'
                ).text
                nom_frais = recup_costsName(driver)
                nom_detail = nom_frais[0]
                nom_offre_speciale = nom_frais[1]
                nom_menage = nom_frais[2]
                nom_service = nom_frais[3]
                nom_taxes = nom_frais[4]
                offre = nom_frais[5]
                try:
                    detail = recup_5costs(driver, nom_taxes)[0]
                    offre_speciale = recup_5costs(driver, nom_taxes)[1]
                    frais_menage = recup_5costs(driver, nom_taxes)[2]
                    frais_service = recup_5costs(driver, nom_taxes)[3]
                    taxes = recup_5costs(driver, nom_taxes)[4]
                except:
                    try:
                        detail = recup_4costs(
                            driver,
                            nom_detail,
                            nom_offre_speciale,
                            nom_menage,
                            nom_service,
                            offre,
                        )[0]
                        offre_speciale = recup_4costs(
                            driver,
                            nom_detail,
                            nom_offre_speciale,
                            nom_menage,
                            nom_service,
                            offre,
                        )[1]
                        frais_menage = recup_4costs(
                            driver,
                            nom_detail,
                            nom_offre_speciale,
                            nom_menage,
                            nom_service,
                            offre,
                        )[2]
                        frais_service = recup_4costs(
                            driver,
                            nom_detail,
                            nom_offre_speciale,
                            nom_menage,
                            nom_service,
                            offre,
                        )[3]
                        taxes = recup_4costs(
                            driver,
                            nom_detail,
                            nom_offre_speciale,
                            nom_menage,
                            nom_service,
                            offre,
                        )[4]
                    except:
                        try:
                            detail = recup_3costs(
                                driver,
                                nom_detail,
                                nom_offre_speciale,
                                nom_menage,
                                offre,
                            )[0]
                            offre_speciale = recup_3costs(
                                driver,
                                nom_detail,
                                nom_offre_speciale,
                                nom_menage,
                                offre,
                            )[1]
                            frais_menage = recup_3costs(
                                driver,
                                nom_detail,
                                nom_offre_speciale,
                                nom_menage,
                                offre,
                            )[2]
                            frais_service = recup_3costs(
                                driver,
                                nom_detail,
                                nom_offre_speciale,
                                nom_menage,
                                offre,
                            )[3]
                            taxes = recup_3costs(
                                driver,
                                nom_detail,
                                nom_offre_speciale,
                                nom_menage,
                                offre,
                            )[4]
                        except:
                            try:
                                detail = recup_2costs(
                                    driver, nom_detail, nom_offre_speciale, offre
                                )[0]
                                offre_speciale = recup_2costs(
                                    driver, nom_detail, nom_offre_speciale, offre
                                )[1]
                                frais_menage = recup_2costs(
                                    driver, nom_detail, nom_offre_speciale, offre
                                )[2]
                                frais_service = recup_2costs(
                                    driver, nom_detail, nom_offre_speciale, offre
                                )[3]
                                taxes = recup_2costs(
                                    driver, nom_detail, nom_offre_speciale, offre
                                )[4]
                            except:
                                try:
                                    detail = recup_1cost(
                                        driver, nom_detail, nom_offre_speciale, offre
                                    )[0]
                                    offre_speciale = recup_1cost(
                                        driver, nom_detail, nom_offre_speciale, offre
                                    )[1]
                                    frais_menage = recup_1cost(
                                        driver, nom_detail, nom_offre_speciale, offre
                                    )[2]
                                    frais_service = recup_1cost(
                                        driver, nom_detail, nom_offre_speciale, offre
                                    )[3]
                                    taxes = recup_1cost(
                                        driver, nom_detail, nom_offre_speciale, offre
                                    )[4]
                                except:
                                    detail = "NA"
                                    offre_speciale = "NA"
                                    frais_menage = "NA"
                                    frais_service = "NA"
                                    taxes = "NA"
                elements_avis = avis(driver)
                etoiles = avis(driver)[0]
                communication = avis(driver)[1]
                proprete = avis(driver)[2]
                precision = avis(driver)[3]
                emplacement = avis(driver)[4]
                arrivee = avis(driver)[5]
                qualite_prix = avis(driver)[6]
                commentaires = avis(driver)[7]
                newAnnonce = Annonce(
                    nom,
                    adresse,
                    info,
                    voyageur,
                    type_bien,
                    nb_lit,
                    nb_salle_bain,
                    prix_nuit,
                    detail,
                    offre_speciale,
                    frais_menage,
                    frais_service,
                    taxes,
                    prix_total,
                    etoiles,
                    commentaires,
                    proprete,
                    precision,
                    communication,
                    emplacement,
                    arrivee,
                    qualite_prix,
                    lien,
                ).__dict__

                newListDict.append(newAnnonce)
                driver.close()
    return newListDict


def stock_donnees(choix: Choix):
    """Fonction qui permet de stocker la liste des dictionnaires dans un fichier json."""
    newListDict = scraping(
        Choix(
            choix.ville,
            choix.date_arrivee,
            choix.date_depart,
            choix.nb_adulte,
            choix.nb_enfant,
        )
    )
    jsonFile = open("annonces.json", "w")
    jsonString = json.dumps(newListDict)
    jsonFile.write(jsonString + "\n")
    jsonFile.close()
    return jsonFile

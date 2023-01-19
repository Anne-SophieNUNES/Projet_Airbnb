"""DESCRIPTION : 
Librairie qui affiche les meilleures annonces.
"""

import pandas as pd
import numpy as np
from rich import print
from .lib_nettoyage import nettoyage_donnees
from .lib_predicteur import choix_annonces, meilleur_modele


def affichage(fichier: str) -> str:
    """Génère la liste des annonces sélectionnées dans la librairie lib_predicteur par le critère de minimisation du prix.

    Exemple :
    >>> affichage("toulouse.json")
    Voici les annonces associées à votre recherche, attention, présence de sur-apprentissage :
    1. Nom : Chill & Work - Villa spa & piscine à Toulouse
     Adresse : Toulouse, Occitanie, France
     Prix total (€) : 308
     Lien : https://www.airbnb.fr/rooms/790983623567164389?adults=1&check_in=2023-02-10&check_out=2023-02-12&previous_page_s
    ection_name=1000
    2. Nom : Chambre privée cosy avec un style naturel et doux.
     Adresse : Toulouse, Occitanie, France
     Prix total (€) : 88
     Lien : https://www.airbnb.fr/rooms/805044156078733328?adults=1&check_in=2023-02-10&check_out=2023-02-12&previous_page_s
    ection_name=1000
    """
    liste = choix_annonces(fichier)
    donnees = nettoyage_donnees(fichier)
    nom_annonces = liste[0]
    indices_annonces = liste[1]
    over_fitting = liste[2]

    affichage = []
    for i in indices_annonces:
        affichage.append(donnees.loc[i, ["nom", "adresse", "prix_total", "lien"]])

    df = pd.DataFrame(affichage)
    df_affichage = df.drop_duplicates()

    if over_fitting != []:
        titre = f", attention, {over_fitting}"
    else:
        titre = ""

    indice = df_affichage["nom"].index.tolist()
    nb = 0
    print(f"Voici les annonces associées à votre recherche{titre} :")
    for i in indice:
        nb = nb + 1
        print(
            f"{nb}. Nom : {df_affichage['nom'][i]} \n Adresse : {df_affichage['adresse'][i]} \n Prix total (€) : {df_affichage['prix_total'][i]} \n Lien : {df_affichage['lien'][i]} "
        )

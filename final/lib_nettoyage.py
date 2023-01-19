"""DESCRIPTION : 

Libraririe associée au nettoyage de données.
"""

import json
import pandas as pd
import numpy as np
from serde.json import from_json, to_json
from serde import serde


def fichier_json(fichier: str) -> list[dict]:
    """Récupération des données."""
    with open(fichier) as f:
        data = json.loads(f.read())
    return data


def nettoyage_donnees(fichier: str):
    """Nettoyage des données :
    - création de nouvelles colonnes,
    - transformation du type des variables,
    - gestion des données manquantes.
    """
    dataframe = fichier_json(fichier)
    df = pd.DataFrame(dataframe)
    df.insert(8, "prixNuit", "")
    df.insert(9, "prixInit", "")
    for i in df.prix_nuit:
        a = i.split(",")
        df.loc[df["prix_nuit"] == i, "prixNuit"] = a[0]
    if len(a) > 1:
        b = a[1].split("t ")
        df.loc[df["prix_nuit"] == i, "prixInit"] = b[1]
    df.voyageur = df["voyageur"].str.replace("NA", "")
    df.type_bien = df["type_bien"].str.replace("NA", "")
    df.nb_lit = df["nb_lit"].str.replace("NA", "")
    df.nb_salle_bain = df["nb_salle_bain"].str.replace("NA", "")
    df.detail = df["detail"].str.replace("NA", "0 €")
    df.offre_speciale = df["offre_speciale"].str.replace("NA", "0 €")
    df.frais_menage = df["frais_menage"].str.replace("NA", "0 €")
    df.frais_service = df["frais_service"].str.replace("NA", "0 €")
    df.taxes = df["taxes"].str.replace("NA", "0 €")
    df.etoiles = df["etoiles"].str.replace("NA", "0 ·")
    df.commentaires = df["commentaires"].str.replace("NA", "0 commentaires")
    df.proprete = df["proprete"].str.replace("NA", "0,0")
    df.precision = df["precision"].str.replace("NA", "0,0")
    df.communication = df["communication"].str.replace("NA", "0,0")
    df.emplacement = df["emplacement"].str.replace("NA", "0,0")
    df.arrivee = df["arrivee"].str.replace("NA", "0,0")
    df.qualite_prix = df["qualite_prix"].str.replace("NA", "0,0")
    df["prixNuit"] = df["prixNuit"].apply(
        lambda x: int(x.split()[0].replace("€ par nuit", ""))
    )
    df["detail"] = df["detail"].apply(lambda x: int(x.split()[0].replace("€", "")))
    df["offre_speciale"] = df["offre_speciale"].apply(
        lambda x: int(x.split()[0].replace("€", ""))
    )
    df["frais_menage"] = df["frais_menage"].apply(
        lambda x: int(x.split()[0].replace("€", ""))
    )
    df["frais_service"] = df["frais_service"].apply(
        lambda x: int(x.split()[0].replace("€", ""))
    )
    df["taxes"] = df["taxes"].apply(lambda x: int(x.split()[0].replace("€", "")))
    df["prix_total"] = df["prix_total"].apply(
        lambda x: int(x.split()[0].replace("€", ""))
    )
    df["etoiles"] = df["etoiles"].apply(
        lambda x: float(x.split()[0].replace(".", "").replace(",", "."))
    )
    df["commentaires"] = df["commentaires"].apply(
        lambda x: int(x.split()[0].replace("commentaires", ""))
    )
    df["proprete"] = df["proprete"].apply(
        lambda x: float(x.split()[0].replace(",", "."))
    )
    df["precision"] = df["precision"].apply(
        lambda x: float(x.split()[0].replace(",", "."))
    )
    df["communication"] = df["communication"].apply(
        lambda x: float(x.split()[0].replace(",", "."))
    )
    df["emplacement"] = df["emplacement"].apply(
        lambda x: float(x.split()[0].replace(",", "."))
    )
    df["arrivee"] = df["arrivee"].apply(lambda x: float(x.split()[0].replace(",", ".")))
    df["qualite_prix"] = df["qualite_prix"].apply(
        lambda x: float(x.split()[0].replace(",", "."))
    )
    return df

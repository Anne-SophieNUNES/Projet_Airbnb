"""Description.

Application ligne de commande pour la librairie affichage de notre problématique.
"""

from .lib_scraping import scraping
from .lib_affichage import affichage
from .lib_scraping import stock_donnees
from .lib_choix_utilisateur import Choix
from serde.json import from_json, to_json
import typer
from rich import print
from rich.table import Table
from typing import List
import json


application = typer.Typer()


@application.command()
def utilisateur(nom_fichier: str):
    exemple_choix = Choix(
        ville = str(input("Quelle est votre destination ? ")),
        date_arrivee = str(input("A quelle date souhaiteriez vous arriver ? (AAAA/MM/JJ) ")), 
        date_depart = str(input("A quelle date souhaiteriez vous repartir ? (AAAA/MM/JJ) ")),
        nb_adulte = int(input("Nombre d'adulte(s) ")),
        nb_enfant = int(input("Nombre d'enfant(s) "))
    )
    code = to_json(exemple_choix)
    
    with open(nom_fichier, "w") as fichier_data:
        fichier_data.write(code)


@application.command()
def scrap(nom_fichier: str):  
    with open(nom_fichier,"r") as fichier:
        code = fichier.read()   
    
    donnees = from_json(Choix, code)
    stock_donnees(donnees)
       
        
@application.command()   
def solution(nom_fichier: str):
    resultat = affichage(nom_fichier)
    return resultat

        
if __name__ == "__main__":
    application()
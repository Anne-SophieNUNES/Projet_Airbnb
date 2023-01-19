# <span style="color:#f5b7b1 ">Présentation du projet</span>
## <span style="color:#b7d8e6">Cadre</span>
Notre projet s'inscrit dans la dynamique actuelle des plateformes de réservation en ligne. En effet, nous avons choisi la plateforme [Lien](airbnb.com) comme support pour notre étude. De nombreuses réservations de locations sont effectuées chaque jour. Ces outils (les plateformes) permettent aux utilisateurs de trouver de manière efficace des suggestions de locations répondants à leurs critères et leurs attentes. Airbnb, comme tant d'autres, recense de nombreuses offres de locations de logements proposées par des particuliers ou bien professionnels. Chaque annonce est très bien référencée avec des caractéristiques précises, une partie allouée au montant et à son détail, ainsi que l'avis d'autres utilisateurs sur ce logement.

## <span style="color:#b7d8e6">Problématique</span>
Une problématique économique peut être dégagée : le montant proposé est-il convenable pour les utilisateurs au vu des caractéristiques de l'annonce ? 
Nous avons choisi de créer une application permettant à un utilisateur d'obtenir une liste d'annonces adaptées à sa recherche (destination, dates et nombre de voyageurs) et dont le prix est propice aux caractéristiques de l'annonce. 

# <span style="color:#f5b7b1">Méthodologie des librairies</span>
Pour résoudre cette problématique économique, nous avons créé plusieurs librairies avec leurs tests correspondants.

## <span style="color:#b7d8e6">Librairie **lib_choix_utilisateur.py**</span>
Permet d'initialiser les données nécessaires pour lancer la recherche : la destination choisie par l'utilisateur, les dates d'arrivée et de départ choisies également par l'utilisateur, ainsi que le nombre de voyageurs (nombre d'adulte(s) et nombre d'enfant(s)). 

## <span style="color:#b7d8e6">Librarie **lib_annonce.py**</span>
Permet de stocker les données d'une annonce dans un objet de type classe et de générer un dictionnaire par la suite pour chaque annonce.

## <span style="color:#b7d8e6">Librairie **lib_scraping.py**</span>
Permet d'extraire (sraper) les données de chaque annonce associée à une recherche choisie au préalable par l'utilisateur. La liste des dictionnaires (annonces) est ensuite sérialiser dans un fichier json.

## <span style="color:#b7d8e6">Librairie **lib_nettoyage.py**</span>
Permet de nettoyer les données du fichier json pour obtenir le bon type de données et gérer les données manquantes.

## <span style="color:#b7d8e6">Librairie **lib_predicteur.py**</span>
Permet de mettre en pratique la partie machine learning du projet. Le but du projet est de créer un modèle de prédiction qui prédit un prix raisonnable pour chaque annonce scraper. Pour rappel, le but est de minimser les coûts de l'utilisateur qui cherche une annonce. 

## <span style="color:#b7d8e6">Librairie **lib_affichage.py**</span>
Permet de paramétrer l'affichage du résultat obtenu par la résolution du problème. La fonction `affichage()`affiche ainsi les annonces dont les prix sont les plus raisonnables.

# <span style="color:#f5b7b1">Utilisation de l'application</span>
1. Pour utiliser l'application, il faut d'abord télécharger un **chromedriver** à l'aide de ce site [Lien](https://chromedriver.chromium.org/downloads).

2. <span style="color:#e5d6f3">Ouvrir un terminal puis utiliser le package `pip` pour intaller `poetry`, `pyserde`, `typer`, `rich`, `pandas`, `numpy`, `scikit-learn`, `selenium` si cela n'est pas déjà fait :</span>
```bash
pip install poetry
pip install pyserde
pip install typer
pip install rich
pip install pandas
pip install numpy
pip install scikit-learn
pip install selenium
```

3. <span style="color:#e5d6f3">Exécuter la ligne de commande suivante pour activer l'environnement.</span>
```bash
poetry shell
```

4. <span style="color:#e5d6f3">Exécuter ensuite la ligne de commande suivante afin de visualiser les commandes possibles de notre application. En l'occurence, ici devront apparaître `utilisateur`, `scrap` et `solution`.</span>
```bash
python -m final --help
```
Si tout fonctionne correctement, le message suivant devrait apparaître :
```bash
Usage: python -m final [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  utilisateur
  scrap
  solution
```

5. <span style="color:#e5d6f3">Enfin, exécuter les lignes de commande ci-dessous pour faire fonctionner l'application :</span>
```bash
python -m final utilisateur donnees.json
```
Les messages suivants devraient alors apparaître :
```bash
Quelle est votre destination ? 
A quelle date souhaiteriez vous arriver ? (AAAA/MM/JJ) 
A quelle date souhaiteriez vous repartir ? (AAAA/MM/JJ)
Nombre d\'adulte(s) 
Nombre d\'enfant(s) 
```
Il suffit alors d'écrire la destination de la recherche, les dates d'arrivée et de départ ainsi que le nombre d'adulte(s) et d'enfant(s) prévu.

```bash
python -m final scrap donnees.json
```
Les données collectées sont stockées dans le fichier **annonces.json**. Pour lancer la fonction *solution*, il suffit de préciser ce nom de fichier.
```bash
python -m final solution annonces.json
```
Avec pour résultat, si on choisit la recherche 
  destination : Toulouse, France
  date arrivée : 2023/02/10
  date départ : 2023/02/12
  nombre adulte(s) : 1
  nombre enfant(s) : 0
```bash
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
```

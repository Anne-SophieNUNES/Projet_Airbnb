"""DESCRIPTION : 

Librairie associée à la partie Machine Learning.

"""

from typing import List
import json
import pandas as pd
import numpy as np
import sklearn.datasets as data
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from .lib_nettoyage import nettoyage_donnees


def meilleur_modele(fichier: str) -> list:
    """Choix du meilleur modèle de prédiction et vérification de la présence de sur-apprentissage.

    Exemple :
    >>> meilleur_modele("toulouse.json")
    [KNeighborsRegressor(n_neighbors=3, weights='distance'), 'présence de sur-apprentissage']
    """
    df = nettoyage_donnees(fichier)
    data_df = df.loc[
        :,
        [
            "prixNuit",
            "detail",
            "offre_speciale",
            "frais_menage",
            "frais_service",
            "taxes",
            "etoiles",
            "commentaires",
            "proprete",
            "precision",
            "communication",
            "emplacement",
            "arrivee",
            "qualite_prix",
        ],
    ]
    target_df = df.loc[:, ["prix_total"]]
    donnees = np.array(data_df)
    predict = np.array(target_df)
    X = donnees
    y = predict
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.1, random_state=42, shuffle=True
    )
    meilleur_estimateur = []
    en = ElasticNet()
    en_gs = GridSearchCV(
        en,
        {
            "alpha": [2**p for p in range(-3, 6)],
            "l1_ratio": (0.01, 0.25, 0.5, 0.75, 1),
        },
        cv=KFold(5),
    )
    en_gs.fit(X_tr, y_tr)
    meilleur_estimateur.append(en_gs.best_estimator_)
    knr = KNeighborsRegressor()
    knr_gs = GridSearchCV(
        knr,
        {
            "n_neighbors": range(0, 10),
            "weights": ("uniform", "distance"),
        },
        cv=KFold(5),
    )
    knr_gs.fit(X_tr, y_tr)
    meilleur_estimateur.append(knr_gs.best_estimator_)
    rfr = RandomForestRegressor()
    rfr_gs = GridSearchCV(
        rfr,
        {
            "n_estimators": (8, 16, 32, 64, 128, 256),
        },
        cv=KFold(5),
    )
    rfr_gs.fit(X_tr, y_tr)
    meilleur_estimateur.append(rfr_gs.best_estimator_)
    svr = SVR()
    svr_pip = Pipeline(
        [
            ("mise_echelle", MinMaxScaler()),
            ("standardisation", StandardScaler()),
            ("support_vecteurs", svr),
        ]
    )
    svr_gs = GridSearchCV(
        svr_pip,
        {
            "support_vecteurs__C": [0.1, 1.0, 10],
            "support_vecteurs__epsilon": (0.1, 1.0, 10),
        },
        cv=KFold(5),
    )
    svr_gs.fit(X_tr, y_tr)
    meilleur_estimateur.append(svr_gs.best_estimator_)
    mlp = MLPRegressor()
    mlp_pip = Pipeline(
        [
            ("mise_echelle", MinMaxScaler()),
            ("standardisation", StandardScaler()),
            ("neurones", mlp),
        ]
    )
    mlp_gs = GridSearchCV(
        mlp_pip,
        {
            "neurones__alpha": 10.0 ** -np.arange(1, 7),
            "neurones__hidden_layer_sizes": ((25,), (50,), (100,), (20, 20)),
        },
        cv=KFold(5),
    )
    mlp_gs.fit(X_tr, y_tr)
    meilleur_estimateur.append(mlp_gs.best_estimator_)
    score_train = []
    for i in meilleur_estimateur:
        i.fit(X_tr, y_tr)
        score_train.append(i.score(X_tr, y_tr))
    df_estimateur = pd.DataFrame(
        {"estimateur": meilleur_estimateur, "score train": score_train}
    )
    meilleur_score_tr = max(df_estimateur["score train"])
    position = int(
        df_estimateur.loc[
            df_estimateur["score train"] == meilleur_score_tr
        ].index.values
    )
    meilleur_modele = df_estimateur["estimateur"][position]
    meilleur_score_train = meilleur_modele.score(X_tr, y_tr)
    meilleur_score_test = meilleur_modele.score(X_te, y_te)
    over_fitting = []
    if (
        meilleur_score_train > meilleur_score_test
        or abs(meilleur_score_train - meilleur_score_test) > 0.4
    ):
        over_fitting = "présence de sur-apprentissage"
    else:
        over_fitting = []
    return [meilleur_modele, over_fitting]


def prediction(fichier: str) -> list:
    """Utilisation du meilleur modèle de prédiction pour prédire les données.

    Exemple :
    Apperçu des dernières lignes du dataframe dont les colonnes sont nom de l'annonce,
    prix réel, prix prédit, écart entre la prédiction et la réalité.

    >>> prediction("toulouse.json")
    [                                                   nom    y  y_pred  ecart (y_pred - y)
    0        Superbe T2 (duplex) Jeanne d’Arc /Les Chalets  134     134                   0
    1       Merveilleux T2 de Standing à 90m de la Garonne  183     183                   0
    2       *Chambre chez un hôte proche du métro roseraie   51      51                   0
    3    Le Roseau - Superbe studio # hypercentre Toulouse  145     145                   0
    4    Chambre privative (pré de la Gare Matabiau SNC...   68      68                   0
    ..                                                 ...  ...     ...                 ...
    260     C3 Chambre bien équipée avec parking sur place   70      70                   0
    261  Villa avec piscine et grande terrasse en trave...  269     269                   0
    262   Riverside Toulouse Immobilier Harmony - Capitole  224     224                   0
    263                                  La maisondubois31  180     180                   0
    264                   T2 meuble banlieue toulouse C 11   98      98                   0

    [265 rows x 4 columns], 'présence de sur-apprentissage']
    """
    liste = meilleur_modele(fichier)
    modele = liste[0]
    over_fitting = liste[1]

    df = nettoyage_donnees(fichier)
    data_df = df.loc[
        :,
        [
            "prixNuit",
            "detail",
            "offre_speciale",
            "frais_menage",
            "frais_service",
            "taxes",
            "etoiles",
            "commentaires",
            "proprete",
            "precision",
            "communication",
            "emplacement",
            "arrivee",
            "qualite_prix",
        ],
    ]
    target_df = df.loc[:, ["prix_total"]]
    X = np.array(data_df)
    y = np.array(target_df)
    y_pred = []
    nom = df.loc[:, "nom"]
    for i in range(0, len(data_df)):
        y_pred.append(modele.predict(X[[i]]))
    liste_y_pred = []
    for a in range(0, len(y_pred)):
        liste_y_pred.append(int(y_pred[a]))
    liste_y = []
    for k in range(0, len(y)):
        liste_y.append(int(y[k]))
    ecart = []
    for j, l in zip(liste_y, liste_y_pred):
        ecart.append(l - j)
    df_pred = pd.DataFrame(
        {"nom": nom, "y": liste_y, "y_pred": liste_y_pred, "ecart (y_pred - y)": ecart}
    )
    return [df_pred, over_fitting]


def choix_annonces(fichier: str) -> list:
    """Sélection des annonces pour lesquelles le prix total réel est minimiser en comparaison du prix prédit.

    Exemple :
    >>> choix_annonces("toulouse.json")
    [['Chill & Work - Villa spa & piscine à Toulouse', 'Chambre privée cosy avec un style naturel et doux.', 'Chambre privée cosy avec un style naturel et doux.'], [66, 175, 175], 'présence de sur-apprentissage']
    """
    liste = prediction(fichier)
    df = liste[0]
    over_fitting = liste[1]
    nom = []
    indices = []
    maximum = max(df["ecart (y_pred - y)"])
    position_max1 = int(df.loc[df["ecart (y_pred - y)"] == maximum].index.values)
    nom.append(df["nom"][position_max1])
    indices.append(position_max1)
    df_1 = df.drop([df.index[position_max1]])
    maximum2 = max(df_1["ecart (y_pred - y)"])
    position_max2 = int(df_1.loc[df_1["ecart (y_pred - y)"] == maximum2].index.values)
    nom.append(df_1["nom"][position_max2])
    indices.append(position_max2)
    df_2 = df_1.drop([df_1.index[position_max2]])
    maximum3 = max(df_2["ecart (y_pred - y)"])
    position_max3 = int(df_2.loc[df_2["ecart (y_pred - y)"] == maximum3].index.values)
    nom.append(df_2["nom"][position_max3])
    indices.append(position_max3)
    return [nom, indices, over_fitting]

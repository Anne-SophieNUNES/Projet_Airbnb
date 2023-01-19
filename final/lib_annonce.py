"""DESCRIPTION : 

Librairie qui permet de créer les dictionnaires des différentes annonces.
"""


class Annonce:
    """Création d'un dictionnaire par annonce."""

    def __init__(
        self,
        nom: str,
        adresse: str,
        info: str,
        voyageur: str,
        type_bien: str,
        nb_lit: str,
        nb_salle_bain: str,
        prix_nuit: str,
        detail: str,
        offre_speciale: str,
        frais_menage: str,
        frais_service: str,
        taxes: str,
        prix_total: str,
        etoiles: str,
        commentaires: str,
        proprete: str,
        precision: str,
        communication: str,
        emplacement: str,
        arrivee: str,
        qualite_prix: str,
        lien: str,
    ):

        self.nom = nom
        self.adresse = adresse
        self.info = info
        self.voyageur = voyageur
        self.type_bien = type_bien
        self.nb_lit = nb_lit
        self.nb_salle_bain = nb_salle_bain
        self.prix_nuit = prix_nuit
        self.detail = detail
        self.offre_speciale = offre_speciale
        self.frais_menage = frais_menage
        self.frais_service = frais_service
        self.taxes = taxes
        self.prix_total = prix_total
        self.etoiles = etoiles
        self.commentaires = commentaires
        self.proprete = proprete
        self.precision = precision
        self.communication = communication
        self.emplacement = emplacement
        self.arrivee = arrivee
        self.qualite_prix = qualite_prix
        self.lien = lien

    def __repr__(self) -> str:
        """
        Exemple :
        >>> repr(Annonce(nom = "Studio Grand Hotel Dieu - Quai Gailleton Bellecour", adresse = "Lyon, Auvergne-Rhône-Alpes, France", info = "Logement entier : appartement chez Chez Jordan", voyageur = "2 voyageurs", type_bien = "Studio", nb_lit = "1 lit", nb_salle_bain =  "1 salle de bain", prix_nuit = "54 € par nuit", detail = "107 €", offre_speciale = "0 €", frais_menage = "0 €", frais_service = "0 €", taxes = "3 €", prix_total = "110 €", etoiles =  "4,55", commentaires = "219 commentaires", proprete = "4,8", precision = "4,8", communication = "4,8", emplacement = "4,9", arrivee = "4,8", qualite_prix = "4,4", lien =  "https://www.airbnb.fr/rooms/40531012?adults=1&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000"))
        "Annonce(nom='Studio Grand Hotel Dieu - Quai Gailleton Bellecour', adresse='Lyon, Auvergne-Rhône-Alpes, France', info='Logement entier : appartement chez Chez Jordan', voyageur='2 voyageurs', type_bien='Studio', nb_lit='1 lit', nb_salle_bain='1 salle de bain', prix_nuit='54 € par nuit', detail='107 €', offre_speciale='0 €', frais_menage='0 €', frais_service='0 €', taxes='3 €', prix_total='110 €', etoiles='4,55', commentaires='219 commentaires', proprete='4,8', precision='4,8', communication='4,8', emplacement='4,9', arrivee='4,8', qualite_prix='4,4', lien='https://www.airbnb.fr/rooms/40531012?adults=1&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000')"
        """

        resultat = (
            f"Annonce(nom={repr(self.nom)}, adresse={repr(self.adresse)}, info={repr(self.info)},"
            f" voyageur={repr(self.voyageur)}, type_bien={repr(self.type_bien)}, nb_lit={repr(self.nb_lit)},"
            f" nb_salle_bain={repr(self.nb_salle_bain)}, prix_nuit={repr(self.prix_nuit)}, detail={repr(self.detail)},"
            f" offre_speciale={repr(self.offre_speciale)}, frais_menage={repr(self.frais_menage)}, frais_service={repr(self.frais_service)},"
            f" taxes={repr(self.taxes)}, prix_total={repr(self.prix_total)}, etoiles={repr(self.etoiles)},"
            f" commentaires={repr(self.commentaires)}, proprete={repr(self.proprete)}, precision={repr(self.precision)},"
            f" communication={repr(self.communication)}, emplacement={repr(self.emplacement)}, arrivee={repr(self.arrivee)},"
            f" qualite_prix={repr(self.qualite_prix)}, lien={repr(self.lien)})"
        )
        return resultat

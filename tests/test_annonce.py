"""DESCRIPTION : 

Tests associés à la librarire Annonce.
"""

from final.lib_annonce import Annonce


def test_annonce_initialisation():
    annonce = Annonce(
        nom="Studio Grand Hotel Dieu - Quai Gailleton Bellecour",
        adresse="Lyon, Auvergne-Rhône-Alpes, France",
        info="Logement entier : appartement Chez Jordan",
        voyageur="2 voyageurs",
        type_bien="Studio",
        nb_lit="1 lit",
        nb_salle_bain="1 salle de bain",
        prix_nuit="54 € par nuit",
        detail="107 €",
        offre_speciale="0 €",
        frais_menage="0 €",
        frais_service="0 €",
        taxes="3 €",
        prix_total="110 €",
        etoiles="4,55",
        commentaires="219 commentaires",
        proprete="4,8",
        precision="4,8",
        communication="4,8",
        emplacement="4,9",
        arrivee="4,8",
        qualite_prix="4,4",
        lien="https://www.airbnb.fr/rooms/40531012?adults=1&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000",
    )
    assert isinstance(annonce, Annonce)


def test_repr():
    resultat = Annonce(
        nom="Studio Grand Hotel Dieu - Quai Gailleton Bellecour",
        adresse="Lyon, Auvergne-Rhône-Alpes, France",
        info="Logement entier : appartement Chez Jordan",
        voyageur="2 voyageurs",
        type_bien="Studio",
        nb_lit="1 lit",
        nb_salle_bain="1 salle de bain",
        prix_nuit="54 € par nuit",
        detail="107 €",
        offre_speciale="0 €",
        frais_menage="0 €",
        frais_service="0 €",
        taxes="3 €",
        prix_total="110 €",
        etoiles="4,55",
        commentaires="219 commentaires",
        proprete="4,8",
        precision="4,8",
        communication="4,8",
        emplacement="4,9",
        arrivee="4,8",
        qualite_prix="4,4",
        lien="https://www.airbnb.fr/rooms/40531012?adults=1&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000",
    )
    assert (
        repr(resultat)
        == "Annonce(nom='Studio Grand Hotel Dieu - Quai Gailleton Bellecour', adresse='Lyon, Auvergne-Rhône-Alpes, France', info='Logement entier : appartement Chez Jordan', voyageur='2 voyageurs', type_bien='Studio', nb_lit='1 lit', nb_salle_bain='1 salle de bain', prix_nuit='54 € par nuit', detail='107 €', offre_speciale='0 €', frais_menage='0 €', frais_service='0 €', taxes='3 €', prix_total='110 €', etoiles='4,55', commentaires='219 commentaires', proprete='4,8', precision='4,8', communication='4,8', emplacement='4,9', arrivee='4,8', qualite_prix='4,4', lien='https://www.airbnb.fr/rooms/40531012?adults=1&check_in=2023-02-10&check_out=2023-02-12&previous_page_section_name=1000')"
    )

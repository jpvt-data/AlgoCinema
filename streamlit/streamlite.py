# La commande du Terminal pour lancer le site : 
# streamlit run .\streamlit\streamlite.py
# OU ne marche pas pour l'instant
# streamlit run 'https://github.com/aliceaupaysdesdata/Movie-recommendation-project/raw/refs/heads/main/streamlit/streamlite.py'


# Importer les bibliothèques nécessaires

import streamlit as st
from streamlit_authenticator import Authenticate
import pandas as pd
from streamlit_option_menu import option_menu


# Configuration de la page : 
# st.set_page_config(page_title="Le 23ème Écran", layout="wide")


# Style CSS pour personnaliser le design : (phase 2)

# st.markdown("""
#    <style>
#        /* Fond général */
#            """)


# BDD gestion de l'authentification des utilisateurs (à mettre avant la page connexion)
# Nos données utilisateurs doivent respecter ce format (cf. quête streamlit 3)
# Chercher comment faire le lien avec la BDD données personnelles 



# Barre de menu : (JP) 
page = option_menu(
            menu_title=None,
            options = ["Accueil", "A propos","Actualité","Programmation"]
        )

# En fonction de l'option sélectionnée afficher le contenu correspondant dans votre application
if page == "Accueil": # IDEE : mettre ça dans une fonction appelée pour simplifier 
    st.write("Bienvenue sur la page d'accueil !")
    # "Recherchez un film de votre choix pour découvrir X propisitions de films proches" à retravailler

    # Barre de recherche (sur toutes les pages) : (Alice)
    # Texte affiché par défaut 'Titre du film'
    # Affiche X options avec titres proches, sous la barre quand l'utilisateur écrit
    # Sélection déclenche la recherche de similarité (model ML)

    # Bloc d'affichage des films : (JP)
        # Nom du film + Lien cliquabe vers page du film
        # Image de l'affiche + Lien cliquabe vers page du film
        # Note (mettre des étoiles en option)
        # Année
        # Genres
        # Durée

    # Base de données fictive avec 5 films similaires
    data = {
            "Titre": ["Inception", "Interstellar", "The Prestige", "Memento", "Tenet"],
            "Affiche": [
                        "https://via.placeholder.com/150/0000FF/808080?text=Inception",
                        "https://via.placeholder.com/150/0000FF/808080?text=Interstellar",
                        "https://via.placeholder.com/150/0000FF/808080?text=The+Prestige",
                        "https://via.placeholder.com/150/0000FF/808080?text=Memento",
                        "https://via.placeholder.com/150/0000FF/808080?text=Tenet"
                        ],
            "Note": [10, 8.6, 4, 8.4, 7.8],
            "Annee_de_Sortie": [2010, 2014, 2006, 2000, 2020],
            "Genres": [
                "Science-fiction, Thriller",
                "Science-fiction, Drame",
                "Drame, Mystère, Science-fiction",
                "Mystère, Thriller",
                "Science-fiction, Action, Thriller"
            ],
            "Duree": [148, 169, 130, 113, 150]  # Durée en minutes
    }
    # Convertir en DataFrame
    df = pd.DataFrame(data)

    # Disposition en 5 colonnes fixes
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    # Remplir chaque colonne avec les infos d'un film
    for col, (_, row) in zip(cols, df.iterrows()):
        with col:
            # Affiche l'image
            st.image(row["Affiche"], use_container_width=True)  # Affiche

            # Titre avec moins d'espace
            st.markdown(f"<h3 style='margin-bottom: 5px;'>{row['Titre']}</h3>", unsafe_allow_html=True)

            # Calcul des étoiles
            étoile_j = round(row['Note'] / 2)  # Nombre d'étoiles jaunes (note sur 5)
            étoile_n = 5 - étoile_j  # Nombre d'étoiles vides pour compléter
            étoiles = "⭐" * étoile_j + "⚫" * étoile_n  # Étoiles jaunes + vides

            # Affichage des autres informations avec moins d'espace
            st.markdown(f"<p style='margin: 0;'>{row['Annee_de_Sortie']} - {row['Duree']} min.</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin: 0;'>{row['Note']} / 10  - {étoiles}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin: 0;'>{row['Genres']}</p>", unsafe_allow_html=True)
    # afficher le df pour vérification
    print(df)



    # df = le résultat de la recherche de similarité
    # st.table(df)

elif page == "A propos":
    st.write("**Le 23ème Écran**, votre cinéma creusois et innovant.")
    # ajouter le texte nécessaire, des images etc...

elif page == "Actualité":
    st.write("**Le 23ème Écran**, les actualités de votre cinéma à Guéret")
    # ajouter le texte nécessaire, des images etc...

elif page == "Programmation":
    st.write("**Le 23ème Écran**, la programmation que nous vous proposons")

# elif page == "Connexion":   
    # st.write("**Le 23ème Écran**, accédez à votre espace privé avec plus de fonctionnalités")

    # authenticator.login() # afficher le formulaire de connexion et vérifier les informations d'identification de l'utilisateur


    # Gérer l'accès en fonction des informations renseignées

    # def accueil():
    #     st.title("Bienvenu sur le contenu réservé aux utilisateurs connectés")

    # if st.session_state["authentication_status"]:
    #     accueil()
        # Le bouton de déconnexion
    #     authenticator.logout("Déconnexion")

    # elif st.session_state["authentication_status"] is False:
    #     st.error("L'username ou le password est/sont incorrect")
    # elif st.session_state["authentication_status"] is None:
    #    st.warning('Les champs username et mot de passe doivent être remplie')

# Page les pages vitrines : actualités, programmation, à propos (optionnel)


# Page == "Film", n'apparait pas dans le menu, comment la définie-t-on ?







# Authentification simple : 

# Faire la quête streamlit avancée



# Configuration des autres pages : comprendre le code avant de le faire ici


# Page film dynamique (hors menu) (différente de la page d'accueil)
# - Titre du film
# - Affiche
# - Année
# - Genres
# - Réalisateur
# - Distribution (3 acteurs principaux)
# - Note 
# - Bechdel
# - Possibilité de voter
# - Synopsis
# - Pays
# - Autre résultat de similiarité (avec infos succintes)


# Formulaire d'inscription qui alimente :

# Base de gestion des données personnelles utilisateurs (en option avec la connexion)
# - ID
# - Prénom
# - Nom
# - Email
# - Date de naissance
# - Adresse postale
# - CP
# - Ville
# - Pays


# Base de données notations
# - ID utilisateur
# - ID film
# - note


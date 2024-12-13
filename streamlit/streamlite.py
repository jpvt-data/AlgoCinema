# La commande du Terminal pour lancer le site : 
# streamlit run .\streamlit\streamlite.py
# OU ne marche pas pour l'instant
# streamlit run 'https://github.com/aliceaupaysdesdata/Movie-recommendation-project/raw/refs/heads/main/streamlit/streamlite.py'


# Importer les bibliothèques nécessaires

import streamlit as st
from streamlit_authenticator import Authenticate
import pandas as pd
from streamlit_option_menu import option_menu
from fuzzywuzzy import process
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

# Configuration de la page : 
st.set_page_config(page_title="Le 23ème Écran", layout="wide")



# Barre de recherche (sur toutes les pages) : (Alice)
# Texte affiché par défaut 'Titre du film'
# Affiche X options avec titres proches, sous la barre quand l'utilisateur écrit
# Sélection déclenche la recherche de similarité (model ML)

# Exemple de dataframe
data = {
    'Title': ["Le Hobbit", "Inception", "Batman", "La Petite Sirène"],
    'Description': ["trilogie cinématographique américano-néo-zélandaise de fantasy", "Dom Cobb est un voleur expérimenté dans l'art périlleux de l'extraction", "Batman est un héro taciturne", "Ariel veut explorer le monde des hommes"]
} # Il faudra remplacer les données par la liste des films (BIGDF)
df_films = pd.DataFrame(data)

# Fonction pour trouver les correspondances proches dans la colonne
def search(query, choices, limit=10, threshold=50):
    results = process.extract(query, choices, limit=limit)
    # Filtrer les résultats par seuil
    filtered_results = [result[0] for result in results if result[1] >= threshold]
    return filtered_results

# Fonction de similarité avec un modèle de ML
def compute_similarity(selected_item, data):
    similar_items = data[data['Title'] != selected_item].head(3)  # Simule des films similaires
    # Lancer la recherche de similarité
    return similar_items[['Title', 'Description']]

# Initialiser la session_state pour la recherche
if "search_query" not in st.session_state:
    st.session_state["search_query"] = ""

# Barre de recherche
search_query = st.text_input(
    "Recherchez un film :", 
    placeholder="Tapez un titre de film...",
    key="search_query"
)

# Résultats dynamiques
if search_query:
    results = search(search_query, df_films['Title'].tolist())
    if results:
        selected_title = st.selectbox("Le film recherché est-il disponible dans la liste :", results)
        st.write(f"Vous avez sélectionné : {selected_title}")
        if selected_title:
            st.write(f"Vous avez sélectionné : {selected_title}")
            st.write("Calcul des films similaires...")
            
            # Appeler la fonction de similarité
            similar_films = compute_similarity(selected_title, df_films)
            
            # Afficher les résultats de similarité
            st.write("Films similaires :")
            st.write(similar_films)
    else:
        st.write("Aucun résultat trouvé.")
else:
    st.write("Commencez à taper pour voir les suggestions.")



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
            options = ["Accueil", "A propos","Actualité","Programmation"],
            menu_icon="cast",  # Icône du menu principal
            default_index=0,  # Option par défaut
            orientation="horizontal"
        )

# En fonction de l'option sélectionnée afficher le contenu correspondant dans votre application
if page == "Accueil": # IDEE : mettre ça dans une fonction appelée pour simplifier 
    st.write("Bienvenue sur la page d'accueil !")
    # "Recherchez un film de votre choix pour découvrir X propisitions de films proches" à retravailler




##############################  Bloc d'affichage des films : (JP) ###############################
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
                        "https://image.tmdb.org/t/p/w400/fKwCdrjp1afjgZvHoPR3IUeA8HR.jpg",
                        "https://image.tmdb.org/t/p/w400/AbafEN6mBCxolihpPiSOmvlCIen.jpg",
                        "https://image.tmdb.org/t/p/w400/vOdA1SuDkjxvRr3xBZVCJJyTNlz.jpg",
                        "https://image.tmdb.org/t/p/w400/ijayvLrCAwOVizi9OY8LZWq5SRW.jpg",
                        "https://image.tmdb.org/t/p/w400/qgyp48naq0W7j4NbOttFi91DlYW.jpg"
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


                                    # Affichage de base qui fonctionne >>> on garde de côté
                                    # afficher le df en position centrée
                                    #   st.write(df)
                                    #
                                    #    # Disposition en 5 colonnes fixes
                                    #   col1, col2, col3, col4, col5 = st.columns(5)
                                    #    cols = [col1, col2, col3, col4, col5]
                                    #
                                    #    # Remplir chaque colonne avec les infos d'un film
                                    #    for col, (_, row) in zip(cols, df.iterrows()):
                                    #        with col:
                                    #            # Affiche l'image
                                    #            st.image(row["Affiche"], width=100,  use_container_width=True)  # Affiche
                                    #
                                    #            # Titre avec moins d'espace
                                    #            st.markdown(f"<h3 style='margin-bottom: 5px;'>{row['Titre']}</h3>", unsafe_allow_html=True)
                                    #
                                    #            # Calcul des étoiles
                                    #            étoile_j = round(row['Note'] / 2)  # Nombre d'étoiles jaunes (note/5)
                                    #            étoile_n = 5 - étoile_j  # Nombre d'étoiles vides pour compléter
                                    #            étoiles = "⭐" * étoile_j + "⚫" * étoile_n  # Étoiles jaunes + vides
                                    #
                                    #            # Affichage des autres informations avec moins d'espace
                                    #            st.markdown(f"<p style='margin: 0;'>{row['Annee_de_Sortie']} - {row['Duree']} min.</p>", unsafe_allow_html=True)
                                    #            st.markdown(f"<p style='margin: 0;'>{row['Note']} / 10  - {étoiles}</p>", unsafe_allow_html=True)
                                    #            st.markdown(f"<p style='margin: 0;'>{row['Genres']}</p>", unsafe_allow_html=True)

    # Fonction pour afficher la page d'accueil
    def afficher_accueil():
        st.title("Bienvenue à l'accueil des films")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]

        # Remplir chaque colonne avec les infos d'un film
        for col, (_, row) in zip(cols, df.iterrows()):
            with col:
                # Crée un lien cliquable sur l'image
                image_lien = f'''
                <a href="javascript:void(0)" 
                onclick="window.parent.sessionStorage.setItem('selected_movie', '{row["Titre"]}'); window.parent.location.reload(true);">
                <img src="{row["Affiche"]}" width="400">
                </a>'''
                st.markdown(image_lien, unsafe_allow_html=True)

                # Crée un lien cliquable sur le titre avec du style
                titre_lien = f'''
                <a href="javascript:void(0)" 
                onclick="window.parent.sessionStorage.setItem('selected_movie', '{row["Titre"]}'); window.parent.location.reload(true);" 
                style="font-size: 1.5em; color: white; text-decoration: none; font-weight: bold;">
                {row["Titre"]}
                </a>'''
                st.markdown(titre_lien, unsafe_allow_html=True)

                # Calcul des étoiles
                étoile_j = round(row['Note'] / 2)  # Nombre d'étoiles jaunes (note/5)
                étoile_n = 5 - étoile_j  # Nombre d'étoiles vides pour compléter
                étoiles = "⭐" * étoile_j + "⚫" * étoile_n  # Étoiles jaunes + vides

                # Affichage des autres informations avec moins d'espace
                st.markdown(f"<p style='margin: 0;'>{row['Annee_de_Sortie']} - {row['Duree']} min.</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin: 0;'>{row['Note']} / 10  - {étoiles}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin: 0;'>{row['Genres']}</p>", unsafe_allow_html=True)

    # Fonction pour afficher les détails du film sélectionné
    def afficher_details_film():
        movie_title = st.session_state.selected_movie
        # Recherche du film dans la base de données
        movie_data = df[df['Titre'] == movie_title].iloc[0]

        # Affichage des informations détaillées du film
        st.title(movie_data['Titre'])
        st.image(movie_data['Affiche'], width=300)
        st.markdown(f"**Année de sortie :** {movie_data['Annee_de_Sortie']}")
        st.markdown(f"**Durée :** {movie_data['Duree']} min")
        st.markdown(f"**Genres :** {movie_data['Genres']}")
        st.markdown(f"**Note :** {movie_data['Note']}/10")

        # Bouton pour revenir à la liste des films
        if st.button("Retour à la liste des films"):
            del st.session_state.selected_movie
            st.rerun()

    # Si un film est sélectionné, on affiche la page de détails
    if 'selected_movie' in st.session_state:
        afficher_details_film()
    else:
        afficher_accueil()






##############################  Fin Bloc d'affichage des films : (JP) ###############################

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


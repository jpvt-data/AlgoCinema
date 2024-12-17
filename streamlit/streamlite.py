# Script pour l'application Streamlit "Le 23ème Écran".

# ------- INFOS POUR LANCER LE STREAMLIT -------

# Commande pour lancer : streamlit run .\streamlit\streamlite.py
# Afficher le site web hébergé sur Git Hub / Streamlit Cloud : https://movie-recommendation-project-wcs-bleu-sauvage.streamlit.app/



# ------- Import des bibliothèques nécessaires -------

import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from streamlit_option_menu import option_menu
from fuzzywuzzy import process
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
import os # lire la feuille de style (chemin absolu)


# ------- Configuration globale -------

st.set_page_config(
    page_title="Le 23ème Écran",
    layout="wide")
st.image("streamlit\logo.png", caption="Le 23ème Écran")


# ------ Style CSS ------

def load_css(file_name):
    # Utiliser un chemin relatif basé sur la racine
    file_path = file_name  # Avec style.css dans le même dossier que ce script
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Erreur : Le fichier CSS n'a pas été trouvé. Vérifiez le chemin.")
        

# ------- DONNEES -------

load_css("streamlit\style.css")

df_recherche_titres_films = pd.DataFrame({
    'tconst': ['tt001', 'tt002', 'tt003', 'tt004', 'tt005'],
    'Title': ['Film A', 'Film B', 'Film C', 'Film D', 'Film E'],
}) # à remplacer par fichier.csv --> title_akas.csv --> à compléter


df_infos = pd.DataFrame({ # Simulation du dataframe des informations des films
    'tconst': ['tt001', 'tt002', 'tt003', 'tt004', 'tt005'],
    'Title': ['Film A', 'Film B', 'Film C', 'Film D', 'Film E'],
    'Affiche': ['https://via.placeholder.com/400'] * 5,
    'Note': [8.5, 7.2, 6.8, 9.1, 7.0],
    'Annee_de_Sortie': [2023, 2022, 2021, 2020, 2019],
    'Duree': [120, 110, 95, 105, 100],
    'Genres': ['Action', 'Drama', 'Comedy', 'Sci-Fi', 'Thriller']
}) # à remplacer par fichier.csv --> à compléter pour pouvoir aller piocher les infos à afficher


# ------- Fonctions de navigation -------

# Fonction pour afficher le menu
def afficher_menu():
    return option_menu(
        menu_title=None,
        options=["Accueil", "À propos", "Actualités", "Programmation"],
        menu_icon="cast",  # Icône du menu principal
        default_index=0,  # Option par défaut
        orientation="horizontal"
    )

# Pages spécifiques
def afficher_accueil():
    st.title("Bienvenue au **23ème Écran**")
    st.write("Votre cinéma local innovant, au cœur de la Creuse.")
    # Autres contenus pour l'accueil...

def afficher_a_propos():
    st.title("À propos")
    st.write("**Le 23ème Écran**, votre cinéma creusois et innovant.")
    # Ajouter d'autres contenus...

def afficher_actualites():
    st.title("Actualités")
    st.write("**Le 23ème Écran**, les actualités de votre cinéma à Guéret.")
    # Ajouter d'autres contenus...

def afficher_programmation():
    st.title("Programmation")
    st.write("**Le 23ème Écran**, voici les films que nous vous proposons.")
    # Ajouter d'autres contenus...

# ------- Fonction de recherche -------

# Fonction pour trouver les correspondances proches dans la colonne
def search(query, choices, limit=10, threshold=50):
    results = process.extract(query, choices, limit=limit)
    filtered_results = [result[0] for result in results if result[1] >= threshold]
    return filtered_results


# Fonction de similarité avec un modèle de ML
def compute_similarity(selected_title):
    # Simulation du dataframe avec une colonne 'tconst' et 4 lignes fixes
    selected_title
    df_resultats_similarite = pd.DataFrame({
        'tconst': ['tt001', 'tt002', 'tt003', 'tt004', 'tt005']  # Identifiants fictifs
    })  # À compléter avec la fonction de ML développée par Pierre et Rodrigo
    afficher_resultats_similarite(df_resultats_similarite)
    return


# Fonction d'affichage des résultats de recherche de similarité (ML):
def afficher_resultats_similarite(df_resultats_similarite): 
    # Recherche des informations dans DF_Infos pour les tconst du df_ML
    df_display = df_infos[df_infos['tconst'].isin(df_resultats_similarite['tconst'])]

    # Gestion dynamique du nombre de colonnes
    num_results = len(df_display)
    num_cols = min(5, num_results)
    cols = st.columns(num_cols)

    # Remplir chaque colonne avec les infos d'un film
    for col, (_, row) in zip(cols, df_display.iterrows()):
        with col:
            # Crée un lien cliquable sur l'image
            image_lien = f'''
            <a href="javascript:void(0)" 
            onclick="window.parent.sessionStorage.setItem('selected_movie', '{row["Title"]}'); window.parent.location.reload(true);">
            <img src="{row["Affiche"]}" width="400">
            </a>'''
            st.markdown(image_lien, unsafe_allow_html=True)

            # Crée un lien cliquable sur le titre avec du style
            titre_lien = f'''
            <a href="javascript:void(0)" 
            onclick="window.parent.sessionStorage.setItem('selected_movie', '{row["Title"]}'); window.parent.location.reload(true);" 
            style="font-size: 1.5em; color: white; text-decoration: none; font-weight: bold;">
            {row["Title"]}
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
# def afficher_details_film():
#     movie_title = st.session_state.selected_movie
#   # Recherche du film dans la base de données
#    movie_data = df[df['Titre'] == movie_title].iloc[0]

    # Affichage des informations détaillées du film
#    st.title(movie_data['Titre'])
#    st.image(movie_data['Affiche'], width=300)
#    st.markdown(f"**Année de sortie :** {movie_data['Annee_de_Sortie']}")
#    st.markdown(f"**Durée :** {movie_data['Duree']} min")
#    st.markdown(f"**Genres :** {movie_data['Genres']}")
#   st.markdown(f"**Note :** {movie_data['Note']}/10")

    # Bouton pour revenir à la liste des films
#    if st.button("Retour à la liste des films"):
#        del st.session_state.selected_movie
#        st.rerun()


# ------- État de Session -------

# Initialiser la session_state pour la recherche
if "search_query" not in st.session_state:
    st.session_state["search_query"] = ""

# ------- Interface Utilisateur (UI) -------
    
# Main
if __name__ == "__main__":
    
    # Afficher le menu principal et récupérer la page sélectionnée
    page = afficher_menu()

    # Vérifier si la recherche a déjà été effectuée, et réinitialiser si nécessaire
    if "search_query" not in st.session_state:
        st.session_state["search_query"] = ""
    
    # Réinitialiser la recherche si l'utilisateur change de page
    if page != st.session_state.get("current_page", ""):
        st.session_state["search_query"] = ""
        st.session_state["current_page"] = page

    # Barre de recherche
    search_query = st.text_input(
        "Recherchez un film :", 
        placeholder="Tapez un titre de film...",
        key="search_query"
    )

    # Résultats dynamiques
    if search_query:
        results = search(search_query, df_recherche_titres_films['Title'].tolist())
        if results:
            selected_title = st.selectbox("Résultats :", results)
            st.write(f"Vous avez sélectionné : {selected_title}")
            compute_similarity(selected_title) # à voir si on envoi un tconst et adapter si besoin
        else:
            st.write("Aucun résultat trouvé.")
    else:
        st.write("Commencez à taper pour voir les suggestions.")


    # Coordonner l'affichage en fonction de la page sélectionnée
    if page == "Accueil":
        # Si un film est sélectionné, afficher la page de détails
        if 'selected_movie' in st.session_state:
            t.write(f"Vous avez sélectionné le film : {st.session_state['selected_movie']}")
            afficher_details_film()
        else:
            afficher_accueil()
    
    elif page == "À propos":
        afficher_a_propos()
    
    elif page == "Actualités":
        afficher_actualites()
    
    elif page == "Programmation":
        afficher_programmation()


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
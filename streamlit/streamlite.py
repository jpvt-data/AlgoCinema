# Script pour l'application Streamlit "Le 23ème Écran".

# ------- INFOS POUR LANCER LE STREAMLIT -------

# Commande pour lancer : streamlit run .\streamlit\streamlite.py
# Afficher le site web hébergé sur Git Hub / Streamlit Cloud : https://movie-recommendation-project-wcs-bleu-sauvage.streamlit.app/



# ------- Import des bibliothèques nécessaires -------

import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from streamlit_option_menu import option_menu
# from fuzzywuzzy import process
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
import os # lire la feuille de style (chemin absolu)
from rapidfuzz import process, fuzz



# ------- CHEMINS FICHIERS DONNEES -------

logo = "streamlit/logo.png"

style_css = "streamlit/style.css"

df_infos_csv = "donnees/data/df_info.csv.gz"    

df_ml_csv = "machine learning\DF_ML.csv.gz"



# ------- Configuration globale -------


st.set_page_config(
    page_title="Cinéma le 23ème Écran",
    layout="wide")
st.image(logo)



# ------- CHARGEMENT DES DONNEES -------

@st.cache_data
def load_movie_infos():
    df = pd.read_csv(df_infos_csv)
    return df

df_infos = load_movie_infos() 

   

# ------ Fonction de récupération du style CSS ------

def load_css(file_name):
    # Utiliser un chemin relatif basé sur la racine
    file_path = file_name  # Avec style.css dans le même dossier que le script.py
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Erreur : Le fichier CSS n'a pas été trouvé. Vérifiez le chemin.")


load_css(style_css)



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
def afficher_accueil(search_query=""):
    if search_query:
        results = search(search_query, df_infos['Titre'].tolist())
        if results:
            selected_title = st.selectbox("Sélectionnez un des noms de films les plus proches :", results)
            st.write(f"Vous avez sélectionné : {selected_title}")
            compute_similarity(df_infos[df_infos['Titre'] == selected_title]['tconst'].values[0])  # Passer uniquement le tconst
        else:
            st.write("Aucun résultat trouvé.")
    else:
        st.write("Commencez à taper pour voir les suggestions.")

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

# Fonction de correspondances des noms de films par rapport à l'entrée utilisateur barre de recherches
def search(query, choices, limit=10, threshold=50):
    results = process.extract(query, choices, limit = limit, scorer=fuzz.WRatio, score_cutoff=80)
    filtered_results = [result[0] for result in results if result[1] >= threshold]
    return filtered_results



# Fonction de similarité avec un modèle de ML
def compute_similarity(tconst):
# def recommandation(tconst):

     import pandas as pd
     from sklearn.neighbors import NearestNeighbors

     import warnings
     warnings.filterwarnings("ignore", category=UserWarning)
     warnings.filterwarnings("ignore", category=FutureWarning)

     df_ml = pd.read_csv(df_ml_csv)

     index = df_ml.index
     df_ml_num = df_ml.select_dtypes('number')
     df_ml_cat = df_ml.select_dtypes(['object', 'category', 'string', 'bool'])

     from sklearn.preprocessing import MinMaxScaler
     SN = MinMaxScaler()
     df_ml_num_SN = pd.DataFrame(SN.fit_transform(df_ml_num), columns=df_ml_num.columns, index=index)

     df_ml_encoded = pd.concat([df_ml_num_SN, df_ml_cat], axis=1)

     #On crée une liste des colonnes à utiliser pour le modèle
     caracteristiques = df_ml_encoded.columns.drop(['tconst', 'nconst', 'title', 'tmdb_popularity', 'title_ratings_numVotes','tmdb_US',
          'tmdb_FR', 'tmdb_GB', 'tmdb_DE', 'tmdb_JP', 'tmdb_IN', 'tmdb_IT',
          'tmdb_CA', 'tmdb_ES', 'tmdb_MX', 'tmdb_HK', 'tmdb_BR', 'tmdb_SE',
          'tmdb_SU', 'tmdb_PH', 'tmdb_KR', 'tmdb_AU', 'tmdb_CN', 'tmdb_AR',
          'tmdb_RU', 'tmdb_DK', 'tmdb_NL', 'tmdb_BE', 'tmdb_AT', 'tmdb_TR',
          'tmdb_PL', 'tmdb_CH', 'tmdb_XC', 'tmdb_FI', 'tmdb_NO', 'tmdb_IR',
          'tmdb_XG', 'tmdb_EG', 'tmdb_NG', 'tmdb_ZA'])

     #On sépare notre df en deux groupes, en fonction de la note
     bons_films = df_ml_encoded[df_ml_encoded['notes'] >= 0.7]
     mauvais_films = df_ml_encoded[df_ml_encoded['notes'] < 0.7]

     #On crée notre modèle
     model = NearestNeighbors(n_neighbors=10, metric='euclidean')
     model.fit(bons_films[caracteristiques])

     #On déclare les caractéristiques du film sélectionné par l'utilisateur
     caract_film = df_ml_encoded[df_ml_encoded['tconst'] == tconst]
     caract_film = caract_film[caracteristiques]
     caract_film

     distances, indices = model.kneighbors(caract_film)

     if caract_film['notes'].values[0] > 0.7:
          distances = distances[0][1:]
          indices = indices[0][1:]
          selection = bons_films.iloc[indices]['tconst']
     else:
          selection = bons_films.iloc[indices[0]]['tconst']

     df_resultats_similarite = pd.DataFrame(selection).reset_index(drop=True)
     return afficher_resultats_similarite(df_resultats_similarite)



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
            # Gestion des affiches
            if pd.notna(row["Chemin Affiche"]) and row["Chemin Affiche"]:
                image_lien = f'''
                <a href="javascript:void(0)" 
                onclick="window.parent.sessionStorage.setItem('selected_movie', '{row["Titre"]}'); window.parent.location.reload(true);">
                <img src="https://image.tmdb.org/t/p/w500{row['Chemin Affiche']}" width="300">
                </a>'''
            else:
                # Création d'un bloc noir avec le nom du film
                image_lien = f'''
                <a href="javascript:void(0)" 
                onclick="window.parent.sessionStorage.setItem('selected_movie', '{row["Titre"]}'); window.parent.location.reload(true);"
                style="display: block; width: 300px; height: 400px; background-color: black; color: white; 
                display: flex; justify-content: center; align-items: center; text-align: center; 
                text-decoration: none; font-size: 1.2em;">
                {row["Titre"]}
                </a>'''

            # Afficher le bloc (image ou texte)
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
            st.markdown(f"<p style='margin: 0;'>{row['Année de Sortie']} - {row['Durée (min)']} min.</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin: 0;'>{round(row['Note'], 1)} / 10  - {étoiles}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin: 0;'>{row['genres']}</p>", unsafe_allow_html=True)


    
# Fonction pour afficher les détails du film sélectionné A FINIR ET RELIER AU RESTE NE FONCTIONNE PAS POUR LINSTANT
def afficher_details_film():
    movie_title = st.session_state['selected_movie']
    # Recherche du film dans la base de données
    movie_data = df_infos[df_infos['Titre'] == movie_title]

    # Affichage des informations détaillées du film
    st.title(movie_data['Titre'])
    image_url = f"https://image.tmdb.org/t/p/w500{movie_data['Chemin Affiche']}"
    if movie_data['Chemin Affiche'].isna()== False:
        st.image(image_url, width=300)
    else:
        st.write("Aucune affiche disponible.")

    st.markdown(f"**Année de sortie :** {movie_data['Année de Sortie']}")
    st.markdown(f"**Durée :** {movie_data['Durée (min)']} min")
    st.markdown(f"**Genres :** {movie_data['genres']}")
    st.markdown(f"**Note :** {round(movie_data['Note'], 2)}/10")

    # Bouton pour revenir à la liste des films
    if st.button("Retour à la liste des films"):
        del st.session_state['selected_movie']
        st.rerun()



# ------- Interface Utilisateur (UI) -------
if __name__ == "__main__":
    # Afficher le menu principal
    page = afficher_menu()

    # Gestion de l'état de session
    if "search_query" not in st.session_state:
        st.session_state["search_query"] = ""
    if page != st.session_state.get("current_page", ""):
        st.session_state["search_query"] = ""
        st.session_state["current_page"] = page

    # Logique pour chaque page
    if page == "Accueil":
        st.title("Votre cinéma local et innovant vous accueille")  # Titre spécifique
        search_query = st.text_input(
            "Recherchez un titre de film :", 
            placeholder="Tapez un titre de film...",
            key="search_query"
        )
        if 'selected_movie' in st.session_state:
            afficher_details_film()
        else:
            afficher_accueil(search_query)

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
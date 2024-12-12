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
# st.set_page_config(page_title="Le 23ème Écran", layout="wide")



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



# Bar de menu : (JP)
page = option_menu(
            menu_title=None,
            options = ["Accueil", "A propos","Actualité","Programmation"]
        )

# En fonction de l'option sélectionnée afficher le contenu correspondant dans votre application
if page == "Accueil": # IDEE : mettre ça dans une fonction appelée pour simplifier 
    st.write("Bienvenue sur la page d'accueil !")
    # "Recherchez un film de votre choix pour découvrir X propisitions de films proches" à retravailler




    # Bloc d'affichage des films : (JP)
    # Nom du film + Lien cliquabe vers page du film
    # Image de l'affiche + Lien cliquabe vers page du film
    # Note (mettre des étoiles en option)
    # Année
    # Genres
    # Durée 

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


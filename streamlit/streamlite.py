# Script pour l'application Streamlit "Le 23ème Écran".

# ------- INFOS POUR LANCER LE STREAMLIT -------

# Commande pour lancer sur Windows : streamlit run .\streamlit\streamlite.py
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

df_ml_csv = "machine learning/DF_ML.csv.gz"

# ------- CONFIG GLOBALE -------

st.set_page_config(
    page_title="Cinéma le 23ème Écran",
    layout="wide")


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
    # Affichage du menu avec le logo à gauche et les boutons de navigation
    col1, col2 = st.columns([1, 4])
    with col1:
    # Affichage du logo à gauche
        st.image(logo, use_container_width=True)
    with col2:
    # Initialisation de l'état si nécessaire
        if "menu_choice" not in st.session_state:
            st.session_state["menu_choice"] = "Accueil" 
        # Liste des options du menu
        options = ["Accueil", "À propos", "Actualités"]
        # Construction des boutons dans une disposition horizontale
        cols = st.columns(len(options))
        for i, option in enumerate(options):
            # Bouton interactif dans chaque colonne
            if cols[i].button(option, key=f"bouton_{option}"):
                st.session_state["menu_choice"] = option
    

# Fonction pour afficher l'accueil
def afficher_accueil(search_query=""):
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    search_query = st.text_input("Pour recevoir des suggestions personnalisées :",
                                placeholder="Renseignez le titre d'un film que vous appreciez...",
                                key="search_query")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if search_query:
        results = search(search_query, df_infos['Titre'].tolist())
        if results:
            selected_title = st.selectbox("Sélectionnez un film :", results)
            st.markdown(f"<h2>Votre sélection</h2>",
                    unsafe_allow_html=True)
            col3, col4, col5, col6 = st.columns([1, 1, 1, 1])
            with col3:
                # Vérifier si le chemin de l'affiche n'est pas manquant
                st.markdown(f"<h3>{df_infos.loc[df_infos['Titre'] == selected_title, 'Titre'].values[0]} ({df_infos.loc[df_infos['Titre'] == selected_title, 'Année de Sortie'].values[0]})</h3>", unsafe_allow_html=True)
                if not pd.isna(df_infos.loc[df_infos['Titre'] == selected_title, "Chemin Affiche"]).values[0]:
                    st.image(f"https://image.tmdb.org/t/p/w500{df_infos.loc[df_infos['Titre'] == selected_title, 'Chemin Affiche'].values[0]}", width=150)
                else:
                    st.markdown(
                        f"<div style='width: 150px; height: 225px; background-color: black; color: white; display: flex; justify-content: center; align-items: center; text-align: center;'>{selected_title}</div>",
                        unsafe_allow_html=True
                    )
            with col4:
                # Informations supplémentaires
                
                st.markdown(f"Durée : {df_infos.loc[df_infos['Titre'] == selected_title, 'Durée (min)'].values[0]} min")
                st.markdown(f"{df_infos.loc[df_infos['Titre'] == selected_title, 'genres'].values[0]}")

                etoiles_jaunes = "⭐" * int(round(df_infos.loc[df_infos['Titre'] == selected_title, 'Note'].values[0] / 2))
                st.markdown(f"{round(df_infos.loc[df_infos['Titre'] == selected_title, 'Note'].values[0],1)}/10 {etoiles_jaunes}")
                st.markdown(f"{round(df_infos.loc[df_infos['Titre'] == selected_title, 'Indice Bechdel'].values[0],0)}/3 🙍‍♀️ Test de Bechdel")
            recommandation(df_infos[df_infos['Titre'] == selected_title]['tconst'].values[0])
        else:
            st.write("Aucun résultat trouvé.")
    else:
        st.write("Commencez à taper pour voir les suggestions.")



# Fonction pour afficher "À propos"
def afficher_a_propos():
    st.markdown("<header>", unsafe_allow_html=True)
    st.title("À propos")
    st.markdown("<p>Le 23ème Écran, votre cinéma creusois et innovant.</p>", unsafe_allow_html=True)
    st.markdown("</header>", unsafe_allow_html=True)



# Fonction pour afficher les actualités
def afficher_actualites():
    st.title("Actualités")
    st.write("Les actualités de votre cinéma à Guéret.")


# ------- Fonction de correspondances de noms entré barre de recherches -------

def search(query, choices, limit=10, threshold=50):
    results = process.extract(query, choices, limit = limit, scorer=fuzz.WRatio, score_cutoff=80)
    filtered_results = [result[0] for result in results if result[1] >= threshold]
    return filtered_results



#  ------- Fonction de similarité avec un modèle de ML -------

def recommandation(tconst):
    import pandas as pd
    from sklearn.neighbors import NearestNeighbors

    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

    df_test = pd.read_csv("machine learning/DF_ML.csv.gz")

    # Préparation des données

    index = df_test.index
    df_test_num = df_test.select_dtypes('number')
    df_test_cat = df_test.select_dtypes(['object', 'category', 'string', 'bool'])

    # Normalisation des colonnes numériques
    from sklearn.preprocessing import MinMaxScaler
    SN = MinMaxScaler()
    df_test_num_SN = pd.DataFrame(SN.fit_transform(df_test_num), columns=df_test_num.columns, index=index)

    # Encodage uniquement de la colonne 'nconst'
    df_test_cat_encoded = df_test_cat.copy()
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    df_test_cat_encoded['nconst'] = le.fit_transform(df_test_cat_encoded['nconst'].fillna('inconnu'))

    # On assemble le df numérique et le df texte
    df_test_encoded = pd.concat([df_test_num_SN, df_test_cat_encoded], axis=1)

    #On sépare notre df en deux groupes, en fonction de la note
    bons_films = df_test_encoded[df_test_encoded['notes'] >= 0.7]

    # KNN sur les caractéristiques numériques

    colonnes_a_exclure = ['tconst', 'title', 'tmdb_popularity', 'title_ratings_numVotes', 'imdb_id', 'genres', 'overview', 'overview_lem']
    caracteristiques = df_test_encoded.columns.drop(colonnes_a_exclure, errors='ignore')

    model = NearestNeighbors(n_neighbors=1000, metric='euclidean') # Il faudra tester d'autres combinaisons
    model.fit(bons_films[caracteristiques])

    caract_film = df_test_encoded[df_test_encoded['tconst'] == tconst][caracteristiques]
    distances, indices = model.kneighbors(caract_film)

    if not df_test_encoded[(df_test_encoded['tconst'] == tconst) & (df_test_encoded['notes'] >= 0.7)].empty:
        selection = bons_films.iloc[indices[0]].copy()
        selection['distance_knn'] = distances[0]
    else:
        selection = bons_films.iloc[indices[0]].copy()
        selection = pd.concat([df_test_encoded[df_test_encoded['tconst'] == tconst], selection.iloc[:-1]], axis=0)
        selection['distance_knn'] = distances[0]

    # TF-IDF avec lemmatisation

    colonnes_poids = {
        'genres': 1,
        'overview_lem': 1,
        'nconst': 1
    }

    # On crée une colonne 'texte' qui combine les valeurs pondérées des colonnes spécifiées
    selection['texte'] = selection.apply(lambda row: 
        ' '.join([
            (str(row[col]) + ' ') * colonnes_poids.get(col, 1)  # Répète la valeur de la colonne selon son poids
            for col in colonnes_poids.keys()
        ]),
        axis=1
    )

    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.8)
    tfidf_matrix = vectorizer.fit_transform(selection['texte'])

    model_tfidf = NearestNeighbors(n_neighbors=1000, metric='cosine')
    model_tfidf.fit(tfidf_matrix)

    distances_tfidf, indices_tfidf = model_tfidf.kneighbors(tfidf_matrix[0])
    selection['distance_tfidf'] = distances_tfidf[0]
    
    # Moyenne pondérée des distances

    poids_knn = 1
    poids_tfidf = 100

    selection['distance_ponderee'] = (
        poids_knn * selection['distance_knn']) + (poids_tfidf * selection['distance_tfidf']
    ) 

    # Tri final par la distance pondérée
    selection = selection.sort_values(by='distance_ponderee')

    # Résultat final

    selection_finale = pd.DataFrame(selection['tconst'][1:11]).reset_index(drop=True)

    return afficher_resultats_similarite(selection_finale)



# ------- Fonction d'affichage des résultats de recherche de similarité (ML) -------

def afficher_resultats_similarite(df_resultats_similarite):
    st.markdown(f"<h2>Nos recommandations</h2>",
                    unsafe_allow_html=True)
    # Recherche des informations dans df_infos pour les films identifiés 
    # dans df_resultats_similarite via leur identifiant unique (tconst).
    df_display = df_infos[df_infos['tconst'].isin(df_resultats_similarite['tconst'])]

    # Configuration des colonnes
    num_cols = 5                # Définit le nombre de colonnes à afficher dans l'interface.
    rows = [df_display.iloc[i:i + num_cols] for i in range(0, len(df_display), num_cols)] # Divise le DataFrame en groupes de 5 films pour créer des lignes dans le tableau.

    # Gestion de l'état (Session)
    # Initialiser une variable de session pour stocker le film sélectionné.
    if "selected_movie_from_reco" not in st.session_state: 
        st.session_state["selected_movie_from_reco"] = None 

    # Parcours des lignes de films
    # st.columns(num_cols) : Crée un ensemble de colonnes pour afficher plusieurs films côte à côte.
    # La boucle : Parcourt chaque ligne de films (définie précédemment).
    for row_df in rows:
        cols = st.columns(num_cols) 

        for col, (_, row) in zip(cols, row_df.iterrows()): # Pour chaque film dans une ligne
            with col:
                # Affichage de l'affiche ou du titre en fallback

                # Si une affiche est disponible
                if pd.notna(row["Chemin Affiche"]):
                    st.image(f"https://image.tmdb.org/t/p/w500{row['Chemin Affiche']}", width=150)
                    if st.button("Voir les détails de ce film", key=f"poster_{row['tconst']}"):
                        st.session_state["selected_movie_from_reco"] = row['Titre']
                        afficher_details_film()
                else:
                    st.markdown(
                        f"<div style='width: 150px; height: 225px; background-color: black; color: white; display: flex; justify-content: center; align-items: center; text-align: center;'>{row['Titre']}</div>",
                        unsafe_allow_html=True
                    )
                    if st.button("Voir les détails de ce film", key=f"title_{row['tconst']}"):
                        st.session_state["selected_movie_from_reco"] = row['Titre']
                        afficher_details_film()
                    

                # Informations supplémentaires
                st.markdown(f"**{row['Titre']}**", unsafe_allow_html=True)
                st.markdown(f"{row['Année de Sortie']} - {row['Durée (min)']} min")
                st.markdown(f"{row['genres']}")

                etoiles_jaunes = "⭐" * round(row['Note'] / 2)
                st.markdown(f"{round(row['Note'],1)}/10 {etoiles_jaunes}")
                st.markdown(f"🙍‍♀️ Test de Bechdel : {row['Indice Bechdel']}/3")

        # Remplissage des colonnes vides si nécessaire
        for col in cols[len(row_df):]:
            with col:
                st.empty()


    
# Fonction pour afficher les détails du film sélectionné A FINIR ET RELIER AU RESTE NE FONCTIONNE PAS POUR LINSTANT
def afficher_details_film():
    movie_title = st.session_state['selected_movie_from_reco']
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
        del st.session_state['selected_movie_from_reco']
        st.rerun()



# ------- Interface Utilisateur (UI) -------

if __name__ == "__main__":
    if "search_query" not in st.session_state:
        st.session_state["search_query"] = ""
    # Afficher le menu principal
    page = afficher_menu()
    
    # Navigation basée sur le choix dans l'état
    # .get("menu_choice", "Accueil") : récupère la valeur associée à "menu_choice". 
    # Si cette clé n'existe pas encore, elle retourne "Accueil" par défaut.
    menu_choice = st.session_state.get("menu_choice", "Accueil") 
    # Si l'utilisateur est sur la page "Accueil", 
    # la fonction afficher_accueil() est appelée pour afficher son contenu.
    if menu_choice == "Accueil":
        afficher_accueil(st.session_state["search_query"])
    # Selon la valeur de menu_choice, l'application appelle la fonction
    # correspondante pour afficher le contenu des autres pages
    elif menu_choice == "A_propos":
        afficher_a_propos()
    elif menu_choice == "Actualites":
        afficher_actualites()

    # Gestion de l'état de session

    if page != st.session_state.get("current_page", ""):
        st.session_state["current_page"] = page

        


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
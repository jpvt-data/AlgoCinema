# Script pour l'application Streamlit "Le 23ème Écran".

# ------- INFOS POUR LANCER LE STREAMLIT -------

# Commande pour lancer sur Windows : streamlit run .\streamlit\streamlite.py
# Afficher le site web hébergé sur Git Hub / Streamlit Cloud : https://movie-recommendation-project-wcs-bleu-sauvage.streamlit.app/



# ------- Import des bibliothèques nécessaires -------

import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from streamlit_option_menu import option_menu
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os # lire la feuille de style (chemin absolu)
from rapidfuzz import process, fuzz
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler



# ------- CHEMINS FICHIERS DONNEES -------

logo = "streamlit/logo.png"

style_css = "streamlit/style.css"

df_infos_csv = "donnees/data/df_info.csv.gz"    

df_ml_csv = "machine learning/DF_ML.csv.gz"

image_cinema = "donnees/images/Cinéma.JPG"

image_cinema2 = "donnees/images/23_2.JPG"


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


#  ------- Fonction de similarité avec un modèle de ML -------
def recommandation(tconst):

    # 1ere reco : 5 films avec genre commun et pays commun

    # Chargement des données
    df_ml = pd.read_csv(df_ml_csv)

    # Récupération des valeurs genre et pays qui correspondent au film sélectionné
    df_selection = df_ml[df_ml['tconst'] == tconst]
    colonnes_genre = [
        'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
        'Documentary', 'Drama', 'Family', 'Fantasy', 'Game-Show', 'History',
        'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV',
        'Romance', 'Sci-Fi', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western'
    ]
    colonnes_pays = [
        'tmdb_US', 'tmdb_FR', 'tmdb_GB', 'tmdb_DE', 'tmdb_JP', 'tmdb_IN',
        'tmdb_IT', 'tmdb_CA', 'tmdb_ES', 'tmdb_MX', 'tmdb_HK', 'tmdb_BR',
        'tmdb_SE', 'tmdb_SU', 'tmdb_PH', 'tmdb_KR', 'tmdb_AU', 'tmdb_CN',
        'tmdb_AR', 'tmdb_RU', 'tmdb_DK', 'tmdb_NL', 'tmdb_BE', 'tmdb_AT',
        'tmdb_TR', 'tmdb_PL', 'tmdb_CH', 'tmdb_XC', 'tmdb_FI', 'tmdb_NO',
        'tmdb_IR', 'tmdb_XG', 'tmdb_EG', 'tmdb_NG', 'tmdb_ZA'
    ]

    genre = [colonne for colonne in df_selection.columns if df_selection[colonne].iloc[0] == True and colonne in colonnes_genre]
    pays = [colonne for colonne in df_selection.columns if df_selection[colonne].iloc[0] == True and colonne in colonnes_pays]

    index = df_ml.index
    df_ml_num = df_ml.select_dtypes('number')
    df_ml_cat = df_ml.select_dtypes(['object', 'category', 'string', 'bool'])

    # Normalisation des colonnes numériques
    SN = MinMaxScaler()
    df_ml_num_SN = pd.DataFrame(SN.fit_transform(df_ml_num), columns=df_ml_num.columns, index=index)

    df_ml_encoded = pd.concat([df_ml_num_SN, df_ml_cat], axis=1)

    # Sélection des films en fonction de la note
    bons_films = df_ml_encoded[df_ml_encoded['notes'] >= 0.7]
    
    # Création d'une liste de colonnes à utiliser pour le modèle
    caracteristiques = df_ml_encoded.columns.drop(['tconst', 'nconst', 'title', 'title_ratings_numVotes', 'rating', 
        'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
        'Documentary', 'Drama', 'Family', 'Fantasy', 'Game-Show', 'History',
        'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV',
        'Romance', 'Sci-Fi', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western', 
        'tmdb_US', 'tmdb_FR', 'tmdb_GB', 'tmdb_DE', 'tmdb_JP', 'tmdb_IN',
        'tmdb_IT', 'tmdb_CA', 'tmdb_ES', 'tmdb_MX', 'tmdb_HK', 'tmdb_BR',
        'tmdb_SE', 'tmdb_SU', 'tmdb_PH', 'tmdb_KR', 'tmdb_AU', 'tmdb_CN',
        'tmdb_AR', 'tmdb_RU', 'tmdb_DK', 'tmdb_NL', 'tmdb_BE', 'tmdb_AT',
        'tmdb_TR', 'tmdb_PL', 'tmdb_CH', 'tmdb_XC', 'tmdb_FI', 'tmdb_NO',
        'tmdb_IR', 'tmdb_XG', 'tmdb_EG', 'tmdb_NG', 'tmdb_ZA'])

    # On veut que nos recommandations aient automatiquement un genre en commun et un pays de prod en commun avec le film selectionné
    bons_films = bons_films[bons_films[genre].any(axis=1)]
    bons_films = bons_films[bons_films[pays].any(axis=1)]

    # Création de notre modèle
    model = NearestNeighbors(n_neighbors=10, metric='euclidean')
    model.fit(bons_films[caracteristiques])

    # On déclare les caractéristiques du film sélectionné par l'utilisateur
    caract_film = df_ml_encoded[df_ml_encoded['tconst'] == tconst][caracteristiques]

    # Calcul des distances et indices des voisins
    distances, indices = model.kneighbors(caract_film)

    # Affichage de la sélection des films en fonction des indices trouvés par le modèle
    if caract_film['notes'].values[0] > 0.7:
        distances = distances[0][1:6]
        indices = indices[0][1:6]
        selection = bons_films.iloc[indices]['tconst']
    else:
        distances = distances[0][0:5]
        indices = indices[0][0:5]
        selection = bons_films.iloc[indices]['tconst']

    selection = pd.DataFrame(selection).reset_index(drop=True)

    # 2e reco : 5 films avec genre commun et pays différent

    # Sélection des films en fonction de la note
    bons_films2 = df_ml_encoded[df_ml_encoded['notes'] >= 0.7]

    # On veut que nos recommandations aient automatiquement un genre en commun et un pays de prod différent de celui du film selectionné
    bons_films2 = bons_films2[bons_films2[genre].any(axis=1)]
    bons_films2 = bons_films2[~bons_films2[pays].any(axis=1)]

    # Création de notre modèle
    model2 = NearestNeighbors(n_neighbors=10, metric='euclidean')
    model2.fit(bons_films2[caracteristiques])

    distances2, indices2 = model2.kneighbors(caract_film)

    # Affichage de la sélection des films en fonction des indices trouvés par le modèle
    if caract_film['notes'].values[0] > 0.7:
        distances2 = distances2[0][1:6]
        indices2 = indices2[0][1:6]
        selection2 = bons_films2.iloc[indices2]['tconst']
    else:
        distances2 = distances2[0][0:5]
        indices2 = indices2[0][0:5]
        selection2 = bons_films2.iloc[indices2]['tconst']

    selection2 = pd.DataFrame(selection2).reset_index(drop=True)

    return afficher_resultats_similarite(selection, selection2)



# ------- Fonctions de navigation -------

# Fonction qui affiche le menu de l'app
def afficher_menu():
    # Affichage du menu avec le logo à gauche et les boutons de navigation
    col1, col2 = st.columns([1, 3])
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
            if cols[i].button(option, key=f"bouton_{option}", on_click=navigate_to(option)):
                st.session_state["menu_choice"] = option



# Fonction qui identifie les noms de films les plus proches avec le texte entré dans la barre de recherches
def search(query, choices, limit=10, threshold=50):
    results = process.extract(query, choices, limit = limit, scorer=fuzz.WRatio, score_cutoff=80)
    filtered_results = [result[0] for result in results if result[1] >= threshold]
    return filtered_results


# Fonction pour afficher la page d'accueil : 
def afficher_accueil():
    st.markdown(
        """
        ## Bienvenue au **23ème Écran**, votre cinéma local au cœur de la Creuse !
        Nous sommes bien plus qu’une simple salle de projection. Ici, nous célébrons le **septième art** avec une approche chaleureuse et conviviale, adaptée aux attentes de notre public.

        Pour améliorer votre expérience et préparer votre visite, nous mettons à votre disposition un **moteur de recommandation**.
        
        Saisissez le titre d’un film pour obtenir ses détails et découvrir des recommandations personnalisées basées sur vos goûts !
        """
    )
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    # Prioriser la valeur stockée dans st.session_state["search_query"] si elle existe
    if st.session_state["search_query"]:
        search_query = st.session_state["search_query"]
        st.session_state["search_query"] = ""  # Réinitialiser après usage
    else:
        search_query = st.text_input(
        "Pour recevoir des suggestions personnalisées :",
        placeholder="Renseignez le titre d'un film que vous appréciez...",
        key="search_query"
        )
    st.markdown("</div>", unsafe_allow_html=True)
    
    if search_query:
        results = search(search_query, df_infos['Titre'].tolist())
        if results:
            selected_title = st.selectbox("Sélectionnez un film :", results)
            st.markdown(f"<h2>Votre sélection</h2>",
                    unsafe_allow_html=True)
            col3, col4 = st.columns([1, 3])
            col5, col6 = st.columns([1, 3])
            with col3:
                # Vérifier si le chemin de l'affiche n'est pas manquant
                st.markdown(f"<h3>{df_infos.loc[df_infos['Titre'] == selected_title, 'Titre'].values[0]} ({df_infos.loc[df_infos['Titre'] == selected_title, 'Année de Sortie'].values[0]})</h3>", unsafe_allow_html=True)
            with col5:
                if not pd.isna(df_infos.loc[df_infos['Titre'] == selected_title, "Chemin Affiche"]).values[0]:
                    st.image(f"https://image.tmdb.org/t/p/w500{df_infos.loc[df_infos['Titre'] == selected_title, 'Chemin Affiche'].values[0]}", width=150)
                else:
                    st.markdown(
                        f"<div style='width: 150px; height: 225px; background-color: black; color: white; display: flex; justify-content: center; align-items: center; text-align: center;'>{selected_title}</div>",
                        unsafe_allow_html=True
                    )
            with col6:
                # Informations supplémentaires
                st.markdown(f"Synopsis : {df_infos.loc[df_infos['Titre'] == selected_title, 'Synopsis'].values[0]}")
                st.markdown(f"Durée : {df_infos.loc[df_infos['Titre'] == selected_title, 'Durée (min)'].values[0]} min")
                st.markdown(f"{df_infos.loc[df_infos['Titre'] == selected_title, 'genres'].values[0]}")

                etoiles_jaunes = "⭐" * int(round(df_infos.loc[df_infos['Titre'] == selected_title, 'Note'].values[0] / 2))
                st.markdown(f"{round(df_infos.loc[df_infos['Titre'] == selected_title, 'Note'].values[0],1)}/10 {etoiles_jaunes}")
                st.markdown(f"{int(df_infos.loc[df_infos['Titre'] == selected_title, 'Indice Bechdel'].values[0])}/3 🙍‍♀️ Test de Bechdel")
            recommandation(df_infos[df_infos['Titre'] == selected_title]['tconst'].values[0])
        else:
            st.write("Aucun résultat trouvé.")
    else:
        st.write("Commencez à taper pour voir les suggestions.")

        

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
                
                # Si l'affiche n'est pas disponible
                else:
                    st.markdown(
                        f"<div style='width: 150px; height: 225px; background-color: black; color: white; display: flex; justify-content: center; align-items: center; text-align: center;'>{row['Titre']}</div>",
                        unsafe_allow_html=True
                    )
                
                # Informations supplémentaires
                st.markdown(f"**{row['Titre']}**", unsafe_allow_html=True)
                st.markdown(f"{row['Année de Sortie']} - {row['Durée (min)']} min")
                st.markdown(f"{row['genres']}")

                etoiles_jaunes = "⭐" * round(row['Note'] / 2)
                st.markdown(f"{round(row['Note'],1)}/10 {etoiles_jaunes}")
                st.markdown(f"🙍‍♀️ Test de Bechdel : {row['Indice Bechdel']}/3")
                if st.button("Voir les détails de ce film", key=f"bouton_{row['tconst']}", on_click=afficher_accueil()):
                    st.session_state["search_query"] = row['Titre'].values[0]
                    st.session_state["menu_choice"] = "Accueil"
                st.markdown(f"<br>",unsafe_allow_html=True)
        # Remplissage des colonnes vides si nécessaire
        for col in cols[len(row_df):]:
            with col:
                st.empty()



# Fonction pour afficher "À propos"
def afficher_a_propos():
    st.markdown("<header>", unsafe_allow_html=True)
    st.title("À propos")

    # Image du Cinéma
    st.image(image_cinema2, width=400, caption="Le 23ème Ecran, en plein coeur de la ville !")
    
    # Contenu formaté
    st.markdown(
        """
        ### Notre histoire
        Situé à **Guéret**, le cinéma **Le 23ème Écran** est né de l’envie de redynamiser l’offre culturelle de notre région.  
        Nous proposons une programmation **diversifiée**, alliant grands classiques, films récents, et pépites indépendantes, afin de satisfaire toutes les générations et tous les goûts.

        ### Une expérience unique
        - **Confort moderne** : des salles équipées pour un son et une image de haute qualité.
        - **Événements spéciaux** : avant-premières, soirées thématiques, et rencontres avec des réalisateurs ou acteurs.
        - **Espace détente** : un lieu chaleureux pour partager un moment autour d’un café avant ou après votre séance.

        ### Le moteur de recommandations, votre compagnon cinéphile
        Pour aller encore plus loin, nous avons développé un **moteur de recommandations** personnalisé.  
        Son objectif ? Vous aider à découvrir les films qui correspondent à vos goûts et à vos envies.  
        Grâce à des suggestions pertinentes basées sur nos analyses et vos préférences, il vous accompagne dans votre voyage cinématographique.  
        Vous pouvez utiliser cet outil directement depuis notre site Internet, dans une **interface intuitive** et facile à prendre en main.

        ### Notre mission
        Au **23ème Écran**, nous croyons que chaque film peut toucher une corde sensible et créer des souvenirs inoubliables.  
        Nous sommes fiers de soutenir le cinéma local et international tout en innovant pour offrir une expérience digitale moderne, à la portée de tous.

        **Merci de faire partie de notre aventure. À bientôt dans nos salles !**
        """,
        unsafe_allow_html=True
    )
    st.markdown("</header>", unsafe_allow_html=True)


# Fonction pour afficher les actualités
def afficher_actualites():
    st.title("Actualités")
    st.markdown(
        """
        ## 🎥 Les Dernières Nouvelles du 23ème Écran !
        Découvrez toutes les actualités de votre cinéma préféré à Guéret. Restez informé des événements, avant-premières et nouveautés qui font vivre notre salle !
        """
    )

    # Section 1 : Événements spéciaux
    st.subheader("✨ Événements à venir")
    st.markdown(
        """
        - **Vendredi 12 janvier 2025 : Avant-première exclusive**  
          Venez découvrir *"Les Lumières de la Creuse"*, un documentaire inédit sur notre région, suivi d'une discussion avec le réalisateur.
        
        - **Samedi 20 janvier 2025 : Soirée rétrospective**  
          Thème : *Les chefs-d'œuvre des années 80*. Plongez dans l'univers de Spielberg, Lucas, et bien d'autres !
        
        - **Dimanche 28 janvier 2025 : Atelier cinéma pour enfants**  
          Atelier créatif pour apprendre à réaliser un court-métrage, dès 10 ans (sur réservation).
        """
    )

    # Section 2 : Nouveautés
    st.subheader("🎞 Nouveautés à l'affiche")
    st.markdown(
        """
        - **"La Montagne Sacrée"** : Une épopée fascinante sur les mystères des contes tibétains.  
          (Salle 2, tous les jours à 17h30)  
        - **"Cœurs à Contre-temps"** : Une comédie romantique à ne pas manquer !  
          (Salle 1, séances à 15h et 20h)  
        - **"Le Dernier Horizon"** : Le blockbuster de l'année, en 4K et Dolby Atmos.  
          (Salle 1, séances à 14h, 18h et 21h30)
        """
    )

    # Section 3 : Programmation spéciale
    st.subheader("🌟 Focus sur le cinéma local")
    st.markdown(
        """
        - **"Regards sur la Creuse"** : Une sélection de courts-métrages réalisés par des talents locaux.  
          Projection gratuite, dimanche 14 janvier à 16h (Salle 3).  

        - **Festival du film régional** : Soutenons le cinéma de chez nous avec une programmation unique du 22 au 28 février 2025.
        """
    )

    # Section 4 : Informations pratiques
    st.subheader("📅 Réservez vos places dès maintenant !")
    st.markdown(
        """
        - **Réservations en ligne :** Rendez-vous sur notre site pour réserver vos billets en toute simplicité.  
        - **Tarifs réduits :** Profitez de nos tarifs avantageux pour les étudiants, seniors et familles.
        """
    )
    
    # Section : Image d'illustration
    st.image(image_cinema, width=400, caption="Votre cinéma au cœur des événements 🎬")



# ------- Interface Utilisateur (UI) -------


if "search_query" not in st.session_state:
    st.session_state["search_query"] = ""
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Accueil"

# Fonction pour changer de page
def navigate_to(page):
    st.session_state["current_page"] = page

# Afficher le menu principal
page = afficher_menu()

# Navigation basée sur le choix dans l'état
menu_choice = st.session_state.get("menu_choice", "Accueil") 

# Si l'utilisateur est sur la page "Accueil", 
# la fonction afficher_accueil() est appelée pour afficher son contenu.
if menu_choice == "Accueil":
    afficher_accueil()
# Selon la valeur de menu_choice, l'application appelle la fonction
# correspondante pour afficher le contenu des autres pages
elif menu_choice == "À propos":
    afficher_a_propos()
elif menu_choice == "Actualités":
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
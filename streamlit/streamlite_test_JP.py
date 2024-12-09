import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Le 23ème Écran", page_icon="🎥", layout="wide")

# Style CSS pour personnaliser le design
st.markdown("""
    <style>
        /* Fond général */
        .stApp {
            background-color: #141414; /* Fond type Netflix */
            color: white;
            font-family: 'Arial', sans-serif;
        }
        /* Titres */
        h1, h2, h3 {
            color: #E50914; /* Rouge Netflix */
        }
        /* Sidebar */
        .css-1d391kg {
            background-color: #141414 !important; 
            color: white;
        }
        .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
            color: #E50914 !important;
        }
        .css-1d391kg a {
            color: white;
        }
        .css-1d391kg a:hover {
            color: #E50914;
        }
        /* Boutons de navigation */
        .nav-button {
            background-color: #E50914;
            color: white !important; /* Texte en blanc */
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            margin: 5px;
            cursor: pointer;
            display: inline-block;
            text-decoration: none;
            text-align: center;
        }
        .nav-button:hover {
            background-color: #D40813;
        }
        /* Conteneur des boutons */
        .button-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Application principale
st.title("Le 23ème Écran 🎥")

# Sidebar avec navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisissez une page :", ["Accueil", "À propos"])

if page == "Accueil":
    st.write("Bienvenue sur **Le 23ème Écran**, votre cinéma innovant et immersif.")
    
    # Ajout des boutons pour d'autres pages
    st.markdown("""
        <div class="button-container">
            <a href="#" class="nav-button">Actualités</a>
            <a href="#" class="nav-button">Programmation</a>
            <a href="#" class="nav-button">Notre Engagement</a>
            <a href="#" class="nav-button">Espace Abonné</a>
        </div>
    """, unsafe_allow_html=True)


    st.header("Recherchez un film")

    st.write("Recherchez un film et découvrez ses détails, ainsi que nos recommandations.")
    query = st.text_input("Entrez le nom d'un film :")

    films = {
        "Inception": {
            "Genre": "Science-fiction",
            "Durée": "2h28",
            "Synopsis": "Un voleur, capable d'infiltrer les rêves, est engagé pour une mission complexe.",
            "Année": 2010
        },
        "Titanic": {
            "Genre": "Drame/Romance",
            "Durée": "3h15",
            "Synopsis": "Une histoire d'amour tragique à bord du célèbre navire.",
            "Année": 1997
        }
    }

    if query:
        if query in films:
            film = films[query]
            st.subheader(f"Détails pour : {query}")
            st.markdown(f"""
            <div>
                <h3>{query}</h3>
                <p><strong>Genre :</strong> {film['Genre']}</p>
                <p><strong>Durée :</strong> {film['Durée']}</p>
                <p><strong>Synopsis :</strong> {film['Synopsis']}</p>
                <p><strong>Année :</strong> {film['Année']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Film non trouvé. Essayez un autre titre.")

elif page == "À propos":
    st.header("À propos du cinéma")
    st.write("""
        Plongez dans une expérience cinématographique unique au cœur de la Creuse. Situé dans un cadre naturel authentique, notre cinéma allie proximité, accessibilité et innovation pour offrir à tous une programmation riche et variée.
    """)

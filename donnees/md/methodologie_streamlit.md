⬅️[Retour à l'accueil](../../README.md)

# Méthodologie de l'interface Streamlit

<br>
<p align="center">
  <img src="../images/logo_streamlit.png" alt="Logo Streamlit" width="300">
</p>
<br>

## Introduction

L'application Streamlit "Le 23ème Écran" est une plateforme dédiée à la recommandation de films basée sur les préférences des utilisateurs.

Grâce à une interface simple et interactive, elle permet aux utilisateurs de **rechercher un film et de recevoir des suggestions personnalisées** en fonction de leurs choix. Le projet utilise des techniques de traitement de données et de machine learning pour proposer des recommandations pertinentes.

---

## Étapes de Construction

### Préparation du Projet

Avant de commencer la construction de l'application, nous avons organisé les éléments nécessaires à son fonctionnement. Le projet repose sur plusieurs fichiers, notamment :

- **Logo et Style CSS** : Les fichiers `logo.png` et `style.css` sont utilisés pour personnaliser l'apparence de l'application.
- **Données** : Les fichiers CSV `df_info.csv.gz` et `DF_ML.csv.gz` contiennent les informations sur les films et les données nécessaires pour la recommandation basée sur un modèle d'apprentissage automatique.

### Configuration de l'Application

Une fois les données et les ressources collectées, nous avons configuré l'application Streamlit pour qu'elle s'affiche avec les bons paramètres :

- **Page de Configuration** : La fonction `st.set_page_config` définit le titre et la disposition de la page (largeur complète).
  
```python
st.set_page_config(
    page_title="Cinéma le 23ème Écran",
    layout="wide")
```

### Chargement des Données

L'application charge les données nécessaires à l'aide de la fonction `load_movie_infos()`, qui lit le fichier CSV des informations sur les films. Le fichier est ensuite mis en cache avec `@st.cache_data` pour optimiser les performances.

```python
@st.cache_data
def load_movie_infos():
    df = pd.read_csv(df_infos_csv)
    return df
```

### Gestion du Menu de Navigation

L'interface propose un menu de navigation, permettant de naviguer entre les sections "Accueil", "À propos", et "Actualités". Le menu est construit à l'aide de colonnes et de boutons Streamlit, permettant de modifier l'état de la page en fonction des actions de l'utilisateur.

```python
def afficher_menu():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(logo, use_container_width=True)
    with col2:
        options = ["Accueil", "À propos", "Actualités"]
        cols = st.columns(len(options))
        for i, option in enumerate(options):
            if cols[i].button(option, key=f"bouton_{option}"):
                st.session_state["menu_choice"] = option
```

### Affichage de l'Accueil et Recherche

L'interface de l'accueil permet à l'utilisateur de saisir un titre de film. L'input de recherche est ensuite analysé pour suggérer des titres de films correspondants. La recherche est effectuée grâce à la fonction `search()`, qui utilise la bibliothèque `rapidfuzz` pour la correspondance approximative des titres.

```python
def search(query, choices, limit=10, threshold=50):
    results = process.extract(query, choices, limit=limit, scorer=fuzz.WRatio, score_cutoff=80)
    filtered_results = [result[0] for result in results if result[1] >= threshold]
    return filtered_results
```

### Affichage des Informations du Film Sélectionné

Lorsqu'un utilisateur sélectionne un film, l'application affiche des informations détaillées sur ce film, telles que le titre, l'année de sortie, la durée, le genre, la note, et l'affiche du film. Ces informations sont récupérées dans le dataframe `df_infos`.

```python
st.markdown(f"<h3>{df_infos.loc[df_infos['Titre'] == selected_title, 'Titre'].values[0]} ({df_infos.loc[df_infos['Titre'] == selected_title, 'Année de Sortie'].values[0]})</h3>", unsafe_allow_html=True)
```

### Fonction de Recommandation de Films

La fonction de recommandation `recommandation()` utilise un modèle d'apprentissage automatique pour recommander des films similaires en fonction de l'entrée de l'utilisateur.

```python
def recommandation(tconst):
    # Préparation des données
    df_test = pd.read_csv("machine learning/DF_ML.csv.gz")
    # ... prétraitement des données et apprentissage automatique ...
    # Utilisation de KNN et TF-IDF pour faire des recommandations
```

### Affichage des Sections "À propos" et "Actualités"

Les sections "À propos" et "Actualités" offrent des informations supplémentaires sur le cinéma. Elles sont affichées de manière simple, leur contenu pourra être enrichi dans le temps.

```python
def afficher_a_propos():
    st.title("À propos")
    st.markdown("<p>Le 23ème Écran, votre cinéma creusois et innovant.</p>", unsafe_allow_html=True)
```

### Personnalisation et Style

Le fichier CSS personnalisé permet d'ajouter un style unique à l'application. Il est chargé par la fonction `load_css()`, qui l'intègre dans la page web.

```python
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Erreur : Le fichier CSS n'a pas été trouvé.")
```

---

## Synthèse

L'application "Le 23ème Écran" a été construite en suivant les étapes suivantes :

1. **Chargement des données** : Utilisation de pandas pour charger les données de films et les préparer pour l'affichage et la recommandation.
2. **Interface utilisateur** : Création d'une interface Streamlit conviviale avec un menu de navigation et des champs de recherche.
3. **Modèle de recommandation** : Implémentation d'un modèle d'apprentissage automatique pour recommander des films similaires en utilisant l'algorithme créé précédemment.
4. **Affichage dynamique** : Dynamisation du contenu en fonction des actions de l'utilisateur, avec un affichage d'informations détaillées sur les films sélectionnés.
5. **Personnalisation** : Application d'un style CSS pour rendre l'interface esthétique et agréable à utiliser.

---

## Lancement de l'Application

Vous pouvez accéder à l'application en ligne via Streamlit Cloud à l'adresse suivante :
[https://movie-recommendation-project-wcs-bleu-sauvage.streamlit.app/](https://movie-recommendation-project-wcs-bleu-sauvage.streamlit.app/)

---

⬅️[Retour à l'accueil](../../README.md)
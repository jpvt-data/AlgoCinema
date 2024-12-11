# La commande du Terminal pour lancer le site : 
# streamlit run .\streamlit\streamlite.py
# OU ne marche pas pour l'instant
# streamlit run 'https://github.com/aliceaupaysdesdata/Movie-recommendation-project/raw/refs/heads/main/streamlit/streamlite.py'


# Importer les bibliothèques nécessaires

import streamlit as st
from streamlit_authenticator import Authenticate
import pandas as pd

# Création des pages comment ça fonctionne l'architecture du site ? (Alice)
# Configuration de la page : 

st.set_page_config(page_title="Le 23ème Écran", layout="wide")



# Style CSS pour personnaliser le design : (phase 2)

# st.markdown("""
#    <style>
#        /* Fond général */
#            """)



# Bar de menu : (JP) 

# trouver le code pour
# Accueil : moteur de recherche directement accessible
# A propos
# Actualité
# Programmation
# Connexion



# Page d'accueil : 

st.title("Le 23ème Écran vous fait découvrir le cinéma")

# "Recherchez un film de votre choix pour découvrir X propisitions de films proches" à retravailler

# Barre de recherche (sur toutes les pages) : 

# Texte affiché par défaut 'Titre du film'
# Affiche X options avec titres proches, sous la barre quand l'utilisateur écrit
# Sélection déclenche la recherche de similarité (model ML)



# Bloc d'affichage des films :
# Nom du film + Lien cliquabe vers page du film
# Image de l'affiche + Lien cliquabe vers page du film
# Note (mettre des étoiles en option)
# Année
# Genres
# Durée 

# df = le résultat de la recherche de similarité
# st.table(df)



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


# Page connexion (optionnel): 

# Formulaire d'inscription qui alimente :
# Base de données utilisateurs (en option avec la connexion)
# - ID
# - Prénom
# - Nom
# - Email
# - Date de naissance
# - Adresse postale
# - CP
# - Ville
# - Pays
# - mot de passe (à vérifier comment et si il ne faut pas une autre BDD pour la gestion des mdp)

# Base de données notations
# - ID utilisateur
# - ID film
# - note


# Page les pages vitrines : actualités, programmation, à propos (optionnel)
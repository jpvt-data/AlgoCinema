# Documentation de la Méthodologie

Cette documentation présente une méthodologie complète pour la préparation, l’enrichissement, le nettoyage des données de films, puis la mise en place d’une approche de recommandation fondée sur la similarité et le filtrage par similarité de contenu (modèle de plus proches voisins). L’objectif est d’aboutir à un ensemble de données cohérent et adapté pour entrainer un modèle de recommandation de films, intégré par la suite dans une interface utilisateur

## Objectifs

- Centraliser et combiner plusieurs sources de données (IMDB, TMDB, Bechdel, etc.) afin de disposer d’une base de référence riche par film.
- Nettoyer, filtrer, traiter les valeurs manquantes, et harmoniser les variables.
- Créer une colonne de notation globale (moyenne pondérée entre IMDB et TMDB).
- Préparer des données textuelles (descriptions, genres) pour appliquer TF-IDF et augmenter la qualité des recommandations.
- Développer un système de recommandation de films par similarité, en combinant des métriques numériques (genres, durée, note…) et textuelles (résumé du film, TF-IDF).

## Étapes Détaillées

### 1. Chargement des Données Sources

Le notebook charge plusieurs fichiers sources, chacun contenant un aspect particulier des données sur les films :

- **`db01` (title_basics_traite.csv)** : Contient les informations de base sur les titres (type, année, genres, etc.).
- **`db02` (title_ratings_final.tsv)** : Notes IMDB et nombre de votes par titre.
- **`db03` (title.akas_final.tsv)** : Titres alternatifs d’un même film selon différentes régions/versions.
- **`db04` (tmdb_ml_final.csv)** : Informations issues de TMDB (The Movie Database) telles que popularité, durée, pays de production, titres originaux, etc.
- **`db05` (data_bechdel.csv)** : Données sur le test de Bechdel, permettant de savoir si un film remplit certains critères liés à la représentation des femmes.
- **`db07` (name.basics.tsv)** : Informations sur les individus (réalisateurs, scénaristes, acteurs).
- **`db08` (title.crew.tsv)** : Liens entre titres et équipes (réalisateurs, scénaristes).

Grâce à ces multiples sources, on cherche à rassembler un maximum de métadonnées sur chaque film.

### 2. Fusion des Différentes Sources

Plusieurs opérations de `merge` (`pandas.merge`) sont effectuées :

1. **Title Basics + Title Ratings** : On relie les informations de base du film avec ses notes IMDB.
2. **Akas** : On ajoute les titres alternatifs.
3. **TMDB** : On ajoute les informations détaillées de TMDB (genres complémentaires, notes TMDB, popularité, pays de production).
4. **Bechdel** : On intègre le résultat du test de Bechdel.
5. **Title Crew + Name Basics** : On ajoute les informations sur le réalisateur (et potentiellement scénaristes) afin d’identifier le réalisateur principal du film.

À la fin de ces opérations, on dispose d’un DataFrame complet (`dbmerge_4`) contenant toutes les informations fusionnées autour du champ `tconst` (identifiant IMDB unique).

### 3. Sélection des Colonnes et Nettoyage

Le DataFrame fusionné contient de nombreuses colonnes, parfois redondantes ou non pertinentes pour un usage machine learning. On procède donc à une sélection et à un nettoyage :

- Suppression de colonnes inutiles (ex. pays spécifiques, colonnes auxiliaires non pertinentes pour la recommandation, colonnes dérivées du TMDB non nécessaires).
- Nettoyage de certaines valeurs aberrantes (par exemple, `0` dans `startYear` ou `runtimeMinutes` n’a pas de sens réel ; on transforme ces 0 en `NaN` pour ensuite filtrer).
- Filtrage des lignes : Les enregistrements sans titre, sans année de début ou sans durée sont écartés pour avoir un dataset cohérent.

À cette étape, on obtient un DataFrame (`BIG_DF_ML`) moins volumineux, plus propre, composé principalement de variables utiles (genres, durée, notes, popularité, réalisateur, etc.).

### 4. Calcul d’une Note Globale Agrégée

Les notes IMDB et TMDB sont disponibles. Pour disposer d’une note globale représentative, on calcule une moyenne pondérée entre ces deux sources. La logique est la suivante :

- Si une seule source de note est disponible (IMDB ou TMDB), on utilise cette note.
- Si les deux sont disponibles, on calcule une moyenne pondérée par le nombre de votes IMDB et TMDB.
- Si aucune n’est disponible, on reste avec une valeur manquante.

Cette note globale, stockée dans la colonne `notes`, permettra de filtrer et de segmenter notre dataset : on se concentre souvent sur les “bons” films (par exemple `notes >= 7`) pour la recommandation.

### 5. Harmonisation des Variables Liées au Temps et à la Durée

Certains films n’ont pas d’année de début (`startYear`) ou de durée (`runtimeMinutes`) complètes. On tente de les compléter avec les données TMDB (`tmdb_release_date`, `tmdb_runtime`). Ainsi, si l’année IMDB est absente mais disponible côté TMDB, on l’utilise. De même pour la durée.

### 6. Binarisation des Genres et Pays

Les genres sont transformés en colonnes booléennes (par exemple, une colonne `Comedy` vaut True/False selon si le film est une comédie). Idem pour certains pays de production identifiés par TMDB. Cela permet de construire un espace vectoriel clair pour le machine learning (plutôt qu’une liste de genres, on a un ensemble de features binaires).

### 7. Export de la Table Finale

Une fois le nettoyage terminé, on obtient un DataFrame final nommé `BIG_DF_ML5` (ou `DF_ML` après filtrages finaux) adapté à l’entraînement de modèles de recommandation. Ce fichier est exporté au format `csv.gz` afin d’être réutilisé facilement.

### 8. Recommandation Basée sur la Similarité (Approche K-Nearest Neighbors)

#### a) Idée Générale

L’idée est de recommander des films similaires à un film donné (le “film cible”) en utilisant une mesure de distance dans un espace de caractéristiques. Les caractéristiques incluent :

- Des variables numériques normalisées (durée, popularité, note, etc.)
- Des variables booléennes (genres, pays)
- Le réalisateur (via un encodage d’étiquettes)

On se focalise sur des films “bons” (notes ≥ 7) pour comparer le film cible à des œuvres de qualité.

#### b) Mise en Place du Modèle

On utilise `NearestNeighbors` (Scikit-Learn) pour trouver les k films les plus proches. Le modèle est entraîné sur l’ensemble des films ayant une bonne note, représentés dans l’espace vectoriel décrit ci-dessus.

Pour un film cible, on calcule ses distances avec tous les bons films et on retient les plus proches. Ceci donne une première liste de recommandations “numériques”.

### 9. Amélioration par le Traitement du Texte (TF-IDF)

Les similarités purement numériques ne suffisent pas toujours. On exploite aussi les données textuelles (le résumé du film - `overview`) pour affiner la recommandation :

1. **Lemmatisation du texte** :
   On utilise des méthodes NLP (via Spacy) pour lemmatiser l’overview, c’est-à-dire ramener chaque mot à sa forme de base. On élimine également les stopwords (mots très fréquents et sans valeur sémantique, comme “the”, “and” en anglais).
2. **TF-IDF** :
   On convertit les descriptions textuelles en vecteurs TF-IDF, ce qui permet de mesurer la similarité cosinus entre les films. Les films qui partagent des mots-clés rares et spécifiques auront une similarité textuelle élevée.

   Par exemple, si deux films parlent d’un sujet très spécifique (“robotique interstellaire”), ils seront plus proches en TF-IDF que s’ils parlent simplement d’amour ou de famille (termes très communs).
3. **Combinaison des Distances** :On a maintenant deux mesures de similarité :

   - Distance numérique (genres, notes, etc.) via KNN.
   - Distance textuelle (TF-IDF) sur les résumés.

   On combine ces distances, par exemple :
   `distance_ponderee = (poids_knn * distance_knn) + (poids_tfidf * distance_tfidf)`

   On ajuste les poids pour privilégier davantage la cohérence thématique (TF-IDF) ou la similarité structurelle (KNN). On cherche un équilibre offrant des recommandations pertinentes.

### 10. Résultat Final

Après ce processus, pour un film donné :

- On calcule ses k plus proches voisins numériques.
- On réordonne ces voisins en fonction de leur similarité textuelle (TF-IDF).
- On sélectionne les 10 meilleurs films (par exemple) comme recommandations finales.

Ce système permet de suggérer des films proches du film cible, en prenant en compte à la fois leurs caractéristiques factuelles (genre, note, durée) et leurs thèmes décrits (résumés).

## Conclusion

La méthodologie présentée dans ce notebook couvre :

- La fusion et l’intégration de multiples sources de données pour obtenir un dataset complet.
- Le nettoyage, la normalisation et le formatage des informations, transformant des données brutes en features adaptées au machine learning.
- Le développement d’une approche hybride de recommandation :
  - Approche KNN sur des caractéristiques numériques et catégorielles (genres, réalisateur, etc.).
  - Approche NLP avec TF-IDF et lemmatisation des résumés pour enrichir la notion de similarité.
- La combinaison flexible des différentes distances pour améliorer la pertinence des recommandations.

Cette méthodologie constitue un point de départ solide pour construire un système de recommandation de films, pouvant être affiné avec d’autres sources (acteurs, contextes historiques, analyses sentimentales), ou d’autres algorithmes (modèles plus avancés de NLP, embeddings, deep learning, etc.).

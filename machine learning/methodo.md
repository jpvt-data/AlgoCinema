# Documentation de la Méthodologie

Cette documentation décrit, étape par étape, le processus de préparation, de nettoyage et de recommandation de films. Elle inclut :

- Les **critères de filtrage** et de sélection des films,
- La **logique de calcul** d’une note globale (moyenne pondérée IMDB/TMDB),
- Les **deux approches de recommandation** par KNN (films au même pays vs pays différent),
- Les **méthodes explorées** (TF-IDF, etc.) mais non conservées dans la version finale.

## 1. Nettoyage Préliminaire et Suppression de Colonnes

Le DataFrame fusionné contient de nombreuses colonnes spécialisées (ex. pays spécifiques, booleans de genres partiels, attributs d’épisodes, etc.). Certaines ne sont pas nécessaires, nous avons donc décidé de les supprimer. Pour les colonnes genres de la table TMDB, elles existaient dans les tables IMDB qui contenaient plus de films, c'est pourquoi nous n'en avons gardé qu'un exemplaire.

## 3. Calcul de la Note Globale (moyenne pondérée IMDB/TMDB)

Pourquoi deux systèmes de notation ?
IMDB est très populaire, mais parfois biaisé sur certains genres ou périodes.
TMDB a moins de votes en moyenne, mais il peut compléter IMDB pour des films récents, ou internationaux.
Moyenne Pondérée
Nous avons décidé de calculer une note globale (notes) en pondérant chaque note par son nombre de votes (IMDB vs TMDB). Ainsi, un film très voté sur IMDB aura un impact plus fort qu’un film ayant seulement quelques votes sur TMDB, et vice versa.

L’objectif : Réduire la variance due au fait qu’un film peut avoir 10.0 sur TMDB avec seulement 5 votants, ou 7.5 sur IMDB avec 10 000 votants. La combinaison permet de mieux refléter la “force” d’un score.

## 4. Filtrages Avancés : Année, Nombre de Votes, Durée

### 4.1. Année ≥ 1920
Pour éviter les films très anciens, souvent moins renseignés ou avec trop peu de spectateurs, on filtre `startYear` >= 1920.

### 4.2. Nombre de Votes IMDB ≥ 327
On élimine les films ayant moins de 327 votes IMDB.  
- **Pourquoi 327 ?**  
  - C’est le 75ᵉ percentile (Q3). On exclut ainsi 75% des films ayant le moins de votes, afin de s'assurer d'une note suffisament fiable.

### 4.3. Durée (Complets / Incomplets)
Pour la cohérence du modèle, nous avons préféré compléter `runtimeMinutes` via `tmdb_runtime` lorsque c'était possible, et supprimer les films qui restent avec des valeurs vides. Nous avons conservé les films dont la durée était égale à 0 car certains avaient de bonnes notes.

## 7. Choix de k pour KNN (Évaluation)

On propose une fonction `evaluate_k` afin de tester différentes valeurs de k, en utilisant :

- La **distance moyenne** aux k voisins (plus la valeur est basse, plus les films sont proches en moyenne).  
- Le **score de silhouette** (indicatif de la cohésion en clusters).

En traçant `avg_distances` vs k et `silhouette_scores` vs k, on choisit **k=6** comme compromis optimal.

## 8. Approches de Recommandation

### 8.1. Justification du Seuil de Note (≥ 7)

Avant d’appliquer le KNN, on **filtre** les films à recommander sur la note `notes` ≥ 7.  
- Objectif : ne suggérer que des “bons” films dans l’ensemble candidat.

### 8.3. Fonctions :

#### 8.3.1. `recommandation(tconst)`

- Charge `DF_ML.csv.gz`, récupère le film cible.  
- Identifie ses **genres** (col. booléennes True) et **pays** (col. booléennes True).  
- Filtre la base :  
  - Films ayant `notes ≥ 7`,  
  - Au moins un **genre** commun,  
  - Au moins un **pays** commun.  
- Applique un `NearestNeighbors(n_neighbors=6, metric='euclidean')`.  
- Extrait les **5 plus proches** (en excluant éventuellement le film lui-même si déjà `notes ≥ 7`).  
- Retourne la liste des tconst recommandés.

#### 8.3.2. `recommandation2(tconst)`

- Même logique, **sauf** qu’on exige un **genre** commun, **mais** un **pays** différent :  
  - On filtre sur `~bons_films[pays].any(axis=1)` pour s’assurer qu’aucun pays ne coïncide.  
- Même approche KNN, on retient à nouveau 5 films.

#### 8.3.3. `recommandation_finale(tconst)`

- Combine ces deux recommandations :  
  1. 5 films similaires (genre + pays commun)  
  2. 5 films similaires (genre + pays différent)  
- Pratique pour l’intégration en **Streamlit** : la fonction renvoie deux sélections (`selection`, `selection2`).

---

## Deux Scénarios de Recommandation : Même Pays vs Pays Différent

### Même Pays + Genre Commun
- Pensé pour l’utilisateur qui veut “plus du même” :  
  - Genre(s) commun(s) (Action, Comedy, etc.)  
  - Même pays de production (ex. films américains si l’utilisateur aime le style US).  
- On lance le KNN uniquement sur les films validés selon ces filtres, puis on retient les **5 plus proches** dans l’espace vectoriel.

### Pays Différent + Genre Commun
- Pour ceux qui souhaitent découvrir un style **similaire**, mais d’une **autre culture** / **autre pays**.  
- Les genres demeurent le point commun (ex. Sci-Fi, Romance…), mais on exclut le pays du film cible.  
- Même approche KNN (5 voisins).

> **Note** : Dans les deux cas, on se limite aux films ayant `notes ≥ 7`, afin de ne pas recommander de titres mal notés.

## 9. Approches Testées mais Non Conservées

Au cours du développement, diverses techniques ont été étudiées, sans être intégrées définitivement :

1. **TF-IDF sur les résumés (`overview`)**  
   - But : Comparer les textes des films (synopsis) en plus des aspects numériques.  
   - On a testé la lemmatisation + TF-IDF pour calculer une similarité cosinus.  
   - Finalement, en raison du surcroît de complexité et de calcul, ce module a été mis de côté dans la version courante.  
   - Il reste néanmoins une piste solide pour améliorer la recommandation sur la base de la sémantique.

2. **Pondération Générique des Genres**  
   - Idée : Si un film est multi-genres, pondérer différemment chaque genre, par exemple Action = 2, Romance = 1, etc.  
   - N’a pas été retenu, faute de temps et de données précises permettant de calibrer la pondération.

3. **Prise en Compte des Réalisateurs / Acteurs**  
   - Possible de repérer si deux films partagent le même réalisateur ou acteur phare, et en tenir compte dans la distance.  
   - Non encore implémenté, pourrait être ajouté ultérieurement.

## Conclusion

À travers ce pipeline :

1. **Données Nettoyées** :  
   - Films post-1920,  
   - Au moins 327 votes,  
   - Durée cohérente,  
   - Indicateurs pays et genres en booléens,  
   - Note unique (moyenne pondérée IMDB/TMDB).

2. **KNN** :  
   - On retient k=6 (d’après l’évaluation distance & silhouette).  
   - La recommandation se fait parmi les films “bons” (≥ 7), selon un espace vectoriel normalisé.

3. **Recommandations** :  
   - Soit pays en commun + genre en commun,  
   - Soit pays différent + genre commun.  

4. **Évolutions Possibles** :  
   - Réintroduire un module TF-IDF pour affiner la similarité textuelle,  
   - Pondérer les genres,  
   - Intégrer la dimension “réalisateur/acteurs” (collaborations fréquentes), etc.

Cette méthodologie fournit un cadre robuste pour la recommandation de films, combinant critères objectifs (note, popularité, genres, pays) et flexible (filtres, KNN). Elle est aisément extensible à d’autres sources de données ou d’autres algorithmes (embeddings, deep learning, etc.).

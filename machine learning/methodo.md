# Documentation de la Méthodologie

Cette documentation décrit, **étape par étape**, le processus de **préparation**, de **nettoyage** et de **recommandation** de films. Elle inclut :

- Les **critères de filtrage** et de sélection des films,
- La **logique de calcul** d’une note globale (moyenne pondérée IMDB/TMDB),
- Les **deux approches de recommandation** par KNN (films au même pays vs pays différent),

---

## 1. Nettoyage Préliminaire et Suppression de Colonnes

Le DataFrame fusionné contient de nombreuses colonnes spécialisées (par exemple, des pays spécifiques, des booléens partiels pour les genres, ou encore des attributs relatifs aux épisodes).  
Certaines n’étant pas nécessaires, nous avons décidé de les supprimer. Concernant les colonnes de genres issues de la table TMDB, elles existaient déjà dans les tables IMDB, lesquelles couvraient un plus grand nombre de films. Pour éviter la duplication et les conflits, nous n’en avons donc gardé qu’un seul exemplaire, celui provenant d’IMDB.

---

## 3. Calcul de la Note Globale (moyenne pondérée IMDB/TMDB)

**Pourquoi deux systèmes de notation ?**  
IMDB est très populaire mais peut être biaisé envers certains genres ou certaines périodes.  
TMDB a souvent moins de votes, mais il peut compléter IMDB pour des films plus récents ou internationaux.

**Moyenne Pondérée**  
Nous avons décidé de calculer une note globale (`notes`) en pondérant la contribution de chaque plateforme (IMDB et TMDB) par le nombre de votes associé. Ainsi, un film très voté sur IMDB aura un impact plus fort qu’un film n’ayant que très peu de votants sur TMDB, et vice versa.

L’objectif recherché est de **réduire la variance** : un film pourrait afficher 10.0 sur TMDB avec seulement 5 votants, alors qu’un autre obtiendrait 7.5 sur IMDB avec 10 000 votants. La combinaison de ces deux évaluations permet de mieux refléter la “force” d’un score global.

---

## 4. Filtrages Avancés : Année, Nombre de Votes, Durée

### 4.1. Année ≥ 1920

Pour éviter d’inclure des films très anciens, souvent moins renseignés (ou ayant peu de spectateurs), nous avons décidé de filtrer tous ceux dont `startYear` est **inférieur à 1920**.

### 4.2. Nombre de Votes IMDB ≥ 327

Nous éliminons les films ayant moins de **327 votes** sur IMDB.  
- **Pourquoi 327 ?**  
  - C’est le **75ᵉ percentile (Q3)**. Nous excluons ainsi 75 % des films ayant le moins de votes, et nous assurons une représentativité plus fiable du public.

### 4.3. Durée (Complets / Incomplets)

Pour conserver la cohérence du modèle, nous avons préféré compléter `runtimeMinutes` grâce à `tmdb_runtime` lorsque c’était possible, puis supprimer les films qui avaient toujours des valeurs vides.  
Toutefois, nous avons conservé certains films dont la durée était égale à 0, surtout lorsqu’ils affichaient de bonnes notes.

---

## 7. Choix de k pour KNN (Évaluation)

Nous proposons une fonction `evaluate_k` pour tester différentes valeurs de k, en se basant sur :

- La **distance moyenne** aux k voisins (plus elle est basse, plus les films sont “proches”),
- Le **score de silhouette**, qui reflète la cohésion des clusters.

Après avoir tracé `avg_distances` en fonction de k et `silhouette_scores` en fonction de k, nous avons opté pour **k = 6** comme **compromis optimal**.

---

## 8. Approches de Recommandation

Nous utilisons un **modèle KNN** (k=6) pour suggérer des films “proches” du film cible, après avoir filtré ceux qui ont une **note globale** (`notes`) **≥ 7** (pour ne recommander que des titres appréciés).

### Deux Scénarios de Recommandation

1. **Même Pays + Genre Commun**  
   - L’utilisateur aura “plus du même” : au moins un **genre** identique et au moins un **pays** identique.  
   - Nous appliquons KNN sur ce sous-ensemble et retenons 5 voisins (films similaires).

2. **Pays Différent + Genre Commun**  
   - L’utilisateur aura un style proche (même **genre**), mais d’une autre culture (pays **différent**).  
   - Nous filtrons les films partageant un genre identique, tout en excluant le pays du film cible, puis appliquons KNN (5 voisins).

### Fonctions

#### `recommandation(tconst)`
1. Charge `DF_ML.csv.gz` et identifie le film cible (via `tconst`).  
2. Filtre la base : `notes ≥ 7`, même genre, même pays.  
3. Lance KNN (n_neighbors=6, metric='euclidean').  
4. Retourne les 5 films les plus proches.

#### `recommandation2(tconst)`
1. Similaire à `recommandation(tconst)`, sauf qu’on retient un genre commun **mais** un pays différent.  
2. Retourne 5 films.

#### `recommandation_finale(tconst)`
Combine les deux :  
1. 5 films du même genre + même pays,  
2. 5 films du même genre + pays différent.  

Utile pour intégrer facilement ces recommandations (ex. via Streamlit).  

## Conclusion

À travers ce pipeline :

1. **Données Nettoyées** :  
   - Films post-1920,  
   - Au moins 327 votes,  
   - Durée cohérente,  
   - Pays et genres en booléens,  
   - Note unique (moyenne pondérée IMDB/TMDB).

2. **KNN** :  
   - k = 6, décidé grâce à la distance moyenne et au score de silhouette,  
   - La recommandation se fait exclusivement dans le cercle des films “≥ 7”.

3. **Recommandations** :  
   - Pays en commun + genre en commun,  
   - Pays différent + même genre.

4. **Évolutions Possibles** :  
   - Réintroduire un module TF-IDF pour affiner la similarité textuelle,  
   - Intégrer la dimension “réalisateurs/acteurs” (collaborations fréquentes), etc.

Cette méthodologie fournit un **cadre robuste** pour la recommandation de films, associant filtres objectifs (note, popularité, genres, pays) et distances KNN. Elle reste **flexible** et **extensible** : nous pourrions aisément y ajouter des informations supplémentaires ou recourir à d’autres algorithmes (embeddings, deep learning, etc.) pour gagner en précision et en richesse.

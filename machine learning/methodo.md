# Documentation de la Méthodologie

Cette documentation décrit, **étape par étape**, le processus de **préparation**, de **nettoyage**, et de **recommandation** de films. Elle inclut :

- Les **critères de filtrage** et de sélection des films,
- La **logique de calcul** d’une note globale (moyenne pondérée IMDB/TMDB),
- Les **deux approches de recommandation** par KNN (films au même pays vs pays différent),
- Les limites rencontrées, comme la gestion des décennies et la sélection des pays de production.

---

## 1. Nettoyage Préliminaire et Suppression de Colonnes

Le DataFrame fusionné contient de nombreuses colonnes spécialisées (par exemple, des pays spécifiques, des booléens partiels pour les genres, ou encore des attributs relatifs aux épisodes).  
Certaines n’étant pas nécessaires, nous avons décidé de les supprimer. Concernant les colonnes de genres issues de la table TMDB, elles existaient déjà dans les tables IMDB, lesquelles couvraient un plus grand nombre de films. Pour éviter la duplication et les conflits, nous n’en avons donc gardé qu’un seul exemplaire, celui provenant d’IMDB.

```
# Merge des bdd entre elles
dbmerge_1 = pd.merge(db01, db02, right_on='title_ratings_tconst', left_on='tconst', how='left') #Title Basics + Title Ratings
dbmerge_2 = pd.merge(dbmerge_1, db03, left_on='tconst', right_on='titleId', how='left') # + Title Akas
dbmerge_3 = pd.merge(dbmerge_2, db04, left_on='tconst', right_on='tmdb_imdb_id', how='left') # + TMDB Full
dbmerge_4 = pd.merge(dbmerge_3, db05, left_on='tconst', right_on='imdbid', how='left') # + Bechdel
dbmerge_4 = pd.merge(dbmerge_4, db08, left_on='tconst', right_on='tconst', how='left') # + Title Crew
dbmerge_4 = pd.merge(dbmerge_4, db07, left_on='directors', right_on='nconst', how='left') # + Name Basics
```
```
# Suppresion des colonnes inutiles
BIG_DF_ML = dbmerge_4.drop(columns=[
    'titleType',
    'genres', 
    'decade', 
    'Adult',
    'Short',
    'movie',
    'tmdb_Comedy',
    'tmdb_Adventure',
    'tmdb_Drama',
    'tmdb_Crime',
    'tmdb_Action',
    'tmdb_Documentary',
    'tmdb_Animation',
    'tmdb_Mystery',
    'tmdb_Horror',
    'tmdb_Western',
    'tmdb_Science Fiction',
    'tmdb_Thriller',
    'tmdb_Romance',
    'tmdb_Fantasy',
    'tmdb_Family',
    'tmdb_History',
    'tmdb_Music',
    'tmdb_War', 
    'ordering',
    'region',
    'language',
    'types',
    'attributes',
    'isOriginalTitle',
    'birthYear',
    'deathYear',
    'primaryProfession',
    'knownForTitles',
    'directors',
    'writers'
])
```
---

## 2. Calcul de la Note Globale (moyenne pondérée IMDB/TMDB)

### Pourquoi deux systèmes de notation ?  
IMDB est très populaire mais peut être biaisé envers certains genres ou certaines périodes.  
TMDB a souvent moins de votes, mais il peut compléter IMDB pour des films plus récents ou internationaux.

### Moyenne Pondérée  
Nous avons décidé de calculer une note globale (`notes`) en pondérant la contribution de chaque plateforme (IMDB et TMDB) par le nombre de votes associé. Ainsi, un film très voté sur IMDB aura un impact plus fort qu’un film n’ayant que très peu de votants sur TMDB, et vice versa.

L’objectif recherché est de **réduire la variance** : un film pourrait afficher 10.0 sur TMDB avec seulement 5 votants, alors qu’un autre obtiendrait 7.5 sur IMDB avec 10 000 votants. La combinaison de ces deux évaluations permet de mieux refléter la “force” d’un score global.

```
# Création d'une moyenne pondérée entre les notes title_ratings et tmdb en fonction du nombre de votants
def moyenne_ponderee(ligne):

    # Si 'title_ratings_averageRating' est NaN, on ne prend que 'tmdb_vote_average', et vice versa

    if pd.isna(ligne['title_ratings_averageRating']) and not pd.isna(ligne['tmdb_vote_average']):
        return ligne['tmdb_vote_average']  # Si title_ratings_averageRating est vide, prendre tmdb_vote_average

    elif pd.isna(ligne['tmdb_vote_average']) and not pd.isna(ligne['title_ratings_averageRating']):
        return ligne['title_ratings_averageRating']  # Si tmdb_vote_average est vide, prendre title_ratings_averageRating

    elif not pd.isna(ligne['title_ratings_averageRating']) and not pd.isna(ligne['tmdb_vote_average']):
        # Si les deux colonnes ont des valeurs, calculer la moyenne pondérée
        return (ligne['title_ratings_averageRating'] * ligne['title_ratings_numVotes'] + ligne['tmdb_vote_average'] * ligne['tmdb_vote_count']) / (ligne['title_ratings_numVotes'] + ligne['tmdb_vote_count'])  # Moyenne simple, à ajuster si besoin !
    else:
        return np.nan  # Si les deux sont NaN, retourner NaN
```
---

## 3. Filtrages Avancés : Année, Nombre de Votes, Durée, et Pays

### 3.1. Année ≥ 1920

Pour éviter d’inclure des films très anciens, souvent moins renseignés (ou ayant peu de spectateurs), nous avons décidé de filtrer tous ceux dont `startYear` est **inférieur à 1920**.

```
# Suppression des films sortis avant 1920
BIG_DF_ML3 = BIG_DF_ML3[BIG_DF_ML3['startYear'] >= 1920]
```

### 3.2. Nombre de Votes IMDB ≥ 327

Nous éliminons les films ayant moins de **327 votes** sur IMDB.  
- **Pourquoi 327 ?**  
  - C’est le **75ᵉ percentile (Q3)**. Nous excluons ainsi 75 % des films ayant le moins de votes, et nous assurons une représentativité plus fiable du public.

```
# Suppression de 75% des films en se basant sur le nombre de votes inférieurs à 327
BIG_DF_ML3 = BIG_DF_ML3[BIG_DF_ML3['title_ratings_numVotes'] >= 327]
```

### 3.3. Durée (Complets / Incomplets)

Pour conserver la cohérence du modèle, nous avons préféré compléter `runtimeMinutes` grâce à `tmdb_runtime` lorsque c’était possible, puis supprimer les films qui avaient toujours des valeurs vides.  
Toutefois, nous avons conservé certains films dont la durée était égale à 0, surtout lorsqu’ils affichaient de bonnes notes.

```
def runtimeMinutes(ligne):

    # Si 'runtimeMinutes' est 0, il prend la valeur 'tmdb_runtime'
    BIG_DF_ML4.loc[(BIG_DF_ML4['runtimeMinutes'] == 0)&(BIG_DF_ML4['tmdb_runtime'] != 0), 'runtimeMinutes'] = BIG_DF_ML4['tmdb_runtime']
```

### 3.4. Sélection Limitée à 35 Pays

Nous avons choisi de ne garder que **35 pays de production** parmi les plus représentés dans notre base de données. Cette sélection permet de réduire la complexité du modèle et d’éliminer des catégories très peu renseignées.

Cependant, cette décision pose parfois des problèmes lorsque :  
- Les films sont coproduits par plusieurs pays,  
- Certains de ces pays ne figurent pas dans la sélection.  

Dans ces cas, des informations importantes peuvent être perdues, et certains films peuvent être mal catégorisés ou exclus du modèle.

---

## 4. Choix de k pour KNN (Évaluation)

Nous proposons une fonction `evaluate_k` pour tester différentes valeurs de k, en se basant sur :  

- La **distance moyenne** aux k voisins (plus elle est basse, plus les films sont “proches”),  
- Le **score de silhouette**, qui reflète la cohésion des clusters.  

Après avoir tracé `avg_distances` en fonction de k et `silhouette_scores` en fonction de k, nous avons opté pour **k = 6** comme **compromis optimal**.

```
from sklearn.preprocessing import MinMaxScaler

index = df_ml.index
df_ml_num = df_ml.select_dtypes('number')
df_ml_cat = df_ml.select_dtypes(['object', 'category', 'string', 'bool'])

# Normalisation des colonnes numériques
SN = MinMaxScaler()
df_ml_num_SN = pd.DataFrame(SN.fit_transform(df_ml_num), columns=df_ml_num.columns, index=index)

df_ml_encoded = pd.concat([df_ml_num_SN, df_ml_cat], axis=1)

# On sépare notre df en deux groupes, en fonction de la note
bons_films = df_ml_encoded[df_ml_encoded['notes'] >= 0.7]

# On crée une liste des colonnes à utiliser pour le modèle
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

bons_films = bons_films[caracteristiques]

def evaluate_k(bons_films, k_range):
    """
    Évalue différentes valeurs de k en utilisant la somme des distances aux voisins
    et le score de silhouette comme métriques.

    Args:
        bons_films (DataFrame): Données normalisées
        k_range (range): Plage de valeurs de k à tester

    Returns:
        tuple: (distances moyennes, scores de silhouette)
    """
    from tqdm import tqdm
    from sklearn.metrics import silhouette_score
    from sklearn.cluster import KMeans

    avg_distances = []
    silhouette_scores = []

    # Ajout de tqdm autour de la boucle
    for k in tqdm(k_range, desc='Évaluation de k'):
        # Calcul des distances moyennes pour chaque k
        model = NearestNeighbors(n_neighbors=k)
        model.fit(bons_films)
        distances, _ = model.kneighbors(bons_films)
        avg_distances.append(np.mean(distances))

        # Calcul du score de silhouette
        kmeans = KMeans(n_clusters=k, random_state=42)
        clusters = kmeans.fit_predict(bons_films)
        if k > 1:  # Le score de silhouette nécessite au moins 2 clusters
            silhouette_scores.append(silhouette_score(bons_films, clusters))
        else:
            silhouette_scores.append(0)

    return avg_distances, silhouette_scores

import seaborn as sns
import matplotlib.pyplot as plt

# Définition de la plage de k à tester
k_range = range(1, 21)  # Test des valeurs de k de 1 à 20

# Évaluation des différentes valeurs de k
avg_distances, silhouette_scores = evaluate_k(bons_films, k_range)

# Création d'une visualisation pour aider à choisir k
plt.figure(figsize=(12, 5))

# Premier graphique : Distance moyenne aux voisins
plt.subplot(1, 2, 1)
plt.plot(k_range, avg_distances, 'bo-')
plt.xlabel('Nombre de voisins (k)')
plt.ylabel('Distance moyenne aux voisins')
plt.title('Distance moyenne en fonction de k')
plt.grid(True)

# Second graphique : Score de silhouette
plt.subplot(1, 2, 2)
plt.plot(k_range[1:], silhouette_scores[1:], 'ro-')  # On commence à k=2
plt.xlabel('Nombre de voisins (k)')
plt.ylabel('Score de silhouette')
plt.title('Score de silhouette en fonction de k')
plt.grid(True)

plt.tight_layout()
plt.show()

![alt text](image.png)
```

---

## 5. Approches de Recommandation

Nous utilisons un **modèle KNN** (k=6) pour suggérer des films “proches” du film cible, après avoir filtré ceux qui ont une **note globale** (`notes`) **≥ 7** (pour ne recommander que des titres appréciés).

### Deux Scénarios de Recommandation  

1. **Même Pays + Genre Commun**  
   - L’utilisateur aura “plus du même” : au moins un **genre** identique et au moins un **pays** identique.  
   - Nous appliquons KNN sur ce sous-ensemble et retenons 5 voisins (films similaires).  

```
def recommandation(tconst):
    import pandas as pd
    from sklearn.neighbors import NearestNeighbors
    from sklearn.preprocessing import MinMaxScaler

    # Chargement des données
    df_ml = pd.read_csv("../machine learning/DF_ML.csv.gz")

    # On récupère les valeurs genre et pays qui correspondent au film sélectionné
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

    # On sépare notre df en deux groupes, en fonction de la note
    bons_films = df_ml_encoded[df_ml_encoded['notes'] >= 0.7]
    
    # On crée une liste des colonnes à utiliser pour le modèle
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

    # On veut que nos recommandations aient automatiquement un genre en commun et un pays de prod en commun
    bons_films = bons_films[bons_films[genre].any(axis=1)] if genre else bons_films
    bons_films = bons_films[bons_films[pays].any(axis=1)] if pays else bons_films

    # On crée notre modèle
    model = NearestNeighbors(n_neighbors=6, metric='euclidean')
    model.fit(bons_films[caracteristiques])

    # On déclare les caractéristiques du film sélectionné par l'utilisateur
    caract_film = df_ml_encoded[df_ml_encoded['tconst'] == tconst][caracteristiques]

    # On calcule les distances et indices des voisins
    distances, indices = model.kneighbors(caract_film)

    # On affiche la sélection des films en fonction des indices trouvés par le modèle
    if caract_film['notes'].values[0] > 0.7:
        distances = distances[0][1:6]
        indices = indices[0][1:6]
        selection = bons_films.iloc[indices]['tconst']
    else:
        distances = distances[0][0:5]
        indices = indices[0][0:5]
        selection = bons_films.iloc[indices]['tconst']

    selection = pd.DataFrame(selection).reset_index(drop=True)

    return selection
```

2. **Pays Différent + Genre Commun**  
   - L’utilisateur aura un style proche (même **genre**), mais d’une autre culture (pays **différent**).  
   - Nous filtrons les films partageant un genre identique, tout en excluant le pays du film cible, puis appliquons KNN (5 voisins).

```
def recommandation2(tconst):

    df_ml = pd.read_csv("../machine learning/DF_ML.csv.gz")

    #On récupère les valeurs genre et pays qui correspondent au film selectionné
    df_selection = df_ml[df_ml['tconst'] == tconst]
    colonnes_genre = ['Action', 'Adventure',
    'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama',
    'Family', 'Fantasy', 'Game-Show', 'History', 'Horror', 'Music',
    'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi',
    'Sport', 'Talk-Show', 'Thriller', 'War', 'Western']

    colonnes_pays = ['tmdb_US',
        'tmdb_FR', 'tmdb_GB', 'tmdb_DE', 'tmdb_JP', 'tmdb_IN', 'tmdb_IT',
        'tmdb_CA', 'tmdb_ES', 'tmdb_MX', 'tmdb_HK', 'tmdb_BR', 'tmdb_SE',
        'tmdb_SU', 'tmdb_PH', 'tmdb_KR', 'tmdb_AU', 'tmdb_CN', 'tmdb_AR',
        'tmdb_RU', 'tmdb_DK', 'tmdb_NL', 'tmdb_BE', 'tmdb_AT', 'tmdb_TR',
        'tmdb_PL', 'tmdb_CH', 'tmdb_XC', 'tmdb_FI', 'tmdb_NO', 'tmdb_IR',
        'tmdb_XG', 'tmdb_EG', 'tmdb_NG', 'tmdb_ZA']

    genre = [colonne for colonne in df_selection.columns if df_selection[colonne].iloc[0] == True and colonne in colonnes_genre]
    pays = [colonne for colonne in df_selection.columns if df_selection[colonne].iloc[0] == True and colonne in colonnes_pays]

    index = df_ml.index
    df_ml_num = df_ml.select_dtypes('number')
    df_ml_cat = df_ml.select_dtypes(['object', 'category', 'string', 'bool'])

    from sklearn.preprocessing import MinMaxScaler
    SN = MinMaxScaler()
    df_ml_num_SN = pd.DataFrame(SN.fit_transform(df_ml_num), columns=df_ml_num.columns, index=index)

    df_ml_encoded = pd.concat([df_ml_num_SN, df_ml_cat], axis=1)

    #On crée une liste des colonnes à utiliser pour le modèle
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

    #On sépare notre df en deux groupes, en fonction de la note
    bons_films = df_ml_encoded[df_ml_encoded['notes'] >= 0.7]

    #On veut que nos recommandations aient automatiquement un genre en commun et un pays de prod en commun
    bons_films = bons_films[bons_films[genre].any(axis=1)]
    bons_films = bons_films[~bons_films[pays].any(axis=1)]

    #On crée notre modèle
    model = NearestNeighbors(n_neighbors=6, metric='euclidean')
    model.fit(bons_films[caracteristiques])

    #On déclare les caractéristiques du film sélectionné par l'utilisateur
    caract_film = df_ml_encoded[df_ml_encoded['tconst'] == tconst]
    caract_film = caract_film[caracteristiques]
    caract_film

    distances, indices = model.kneighbors(caract_film)

    #On affiche la selection des films en fonction des indices trouvés par le modèle
    if caract_film['notes'].values[0] > 0.7:
        distances = distances[0][1:6]
        indices = indices[0][1:6]
        selection = bons_films.iloc[indices]['tconst']
    else:
        distances = distances[0][0:5]
        indices = indices[0][0:5]
        selection = bons_films.iloc[indices]['tconst']

    selection = pd.DataFrame(selection).reset_index(drop=True)

    return selection
```

---

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

4. **Limites Identifiées** :  
   - La transformation en décennies n’a pas été pertinente,  
   - La restriction à 35 pays peut entraîner des exclusions ou des informations incomplètes.
   - Les genres définis en booléens peuvent parfois manquer de finesse pour capturer la complexité narrative de certains films.
   - La tentative d’intégrer les décennies comme critère de regroupement n’a pas donné de résultats convaincants, car elle regroupait des films très différents sous un même intervalle temporel arbitraire.

5. **Évolutions Possibles** :  
   - Réintroduire un module TF-IDF pour affiner la similarité textuelle,  
   - Intégrer la dimension “réalisateurs/acteurs” (collaborations fréquentes), etc.  

Cette méthodologie fournit un **cadre robuste** pour la recommandation de films, associant filtres objectifs (note, popularité, genres, pays) et distances KNN. Elle reste **flexible** et **extensible** : nous pourrions aisément y ajouter des informations supplémentaires ou recourir à d’autres algorithmes (embeddings, deep learning, etc.) pour gagner en précision et en richesse.

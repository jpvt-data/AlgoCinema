⬅️[Retour à l'accueil](../../README.md)

# Description des Bases de Données

Ce document détaille les différentes bases de données que nous utilisons pour notre projet, ainsi que leur structure, leur contenu et leur utilité. 

---

## 1. `title.akas.tsv.gz` - Titres de Films et Séries (Multilingues)

**Utilité :** Fournir les titres localisés (notamment en français) et le titre original des œuvres.

**Clé Primaire :** `titleId` (tconst)

| Colonne         | Type    | Description                                                                                                                                         | Conservation |
|------------------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| `titleId`       | string  | Identifiant unique alphanumérique de l'œuvre.                                                                                                   | Oui (clé primaire) |
| `ordering`      | integer | Numéro unique pour identifier les lignes associées à un `titleId`.                                                                                 | Non          |
| `title`         | string  | Titre localisé de l'œuvre.                                                                                                                        | Oui (info)   |
| `region`        | string  | Région pour cette version du titre.                                                                                                              | Filtre, puis drop |
| `language`      | string  | Langue du titre.                                                                                                                                  | Oui (info)   |
| `types`         | array   | Ensemble d'attributs pour ce titre alternatif (ex : "original", "dvd", "festival", etc.).                                                   | Non          |
| `attributes`    | array   | Termes supplémentaires pour décrire ce titre alternatif.                                                                                          | Non          |
| `isOriginalTitle` | boolean | Indique si le titre est l'original (1) ou non (0).                                                                                               | Oui (info complémentaire si absence de nationalité ailleurs) |

---

## 2. `title.basics.tsv.gz` - Informations Générales des Titres

**Utilité :** Identifier les types d’œuvres (film, série, etc.), genres, durée, années de sortie, et autres attributs essentiels.

**Clé Primaire :** `tconst`

| Colonne         | Type    | Description                                                                                                | Conservation |
|------------------|---------|------------------------------------------------------------------------------------------------------------|--------------|
| `tconst`        | string  | Identifiant unique alphanumérique de l'œuvre.                                                              | Oui (clé primaire) |
| `titleType`     | string  | Type de l'œuvre (ex : "movie", "tvseries", etc.).                                                       | Oui (info)   |
| `primaryTitle`  | string  | Titre principal utilisé pour la promotion.                                                                 | Oui          |
| `originalTitle` | string  | Titre original dans la langue d'origine.                                                                  | Oui          |
| `isAdult`       | boolean | Indique si l'œuvre est destinée à un public adulte (1) ou non (0).                                         | Oui          |
| `startYear`     | YYYY    | Année de sortie (ou début de diffusion pour les séries).                                                   | Oui          |
| `endYear`       | YYYY    | Année de fin de diffusion pour les séries (`\N` sinon).                                                   | Non          |
| `runtimeMinutes`| integer | Durée de l'œuvre en minutes.                                                                               | Oui          |
| `genres`        | array   | Liste des genres associés (jusqu’à 3).                                                                    | Oui          |

---

## 3. `title.crew.tsv.gz` - Informations sur les Réalisateurs et Scénaristes

**Utilité :** Identifier les réalisateurs et scénaristes associés aux titres.

**Clé Primaire :** `tconst`

| Colonne     | Type              | Description                                    | Conservation |
|-------------|-------------------|------------------------------------------------|--------------|
| `tconst`    | string            | Identifiant unique de l'œuvre.                | Oui (clé primaire) |
| `directors` | array of `nconst` | Identifiant(s) des réalisateurs.              | Oui          |
| `writers`   | array of `nconst` | Identifiant(s) des scénaristes.               | Oui          |

---

## 4. `title.episode.tsv.gz` - Informations sur les Épisodes de Séries

**Utilité :** Fournir des détails sur les épisodes individuels d'une série.

**Clé Primaire :** `tconst`

| Colonne       | Type    | Description                                   | Conservation |
|---------------|---------|-----------------------------------------------|--------------|
| `tconst`      | string  | Identifiant unique de l'épisode.              | Oui (clé primaire) |
| `parentTconst`| string  | Identifiant unique de la série parente.       | Oui          |
| `seasonNumber`| integer | Numéro de la saison.                         | Oui          |
| `episodeNumber`| integer| Numéro de l'épisode dans la saison.           | Oui          |

---

## 5. `title.principals.tsv.gz` - Cast & Crew Principal

**Utilité :** Identifier les acteurs, actrices et membres principaux de l’équipe technique.

**Clé Primaire :** `tconst`

| Colonne      | Type    | Description                                                              | Conservation |
|--------------|---------|--------------------------------------------------------------------------|--------------|
| `tconst`     | string  | Identifiant unique de l'œuvre.                                           | Oui (clé primaire) |
| `ordering`   | integer | Numéro unique pour identifier les lignes associées à un `titleId`.       | Non          |
| `nconst`     | string  | Identifiant unique de la personne.                                       | Oui          |
| `category`   | string  | Catégorie du rôle ou poste occupé par la personne.                      | Oui          |
| `job`        | string  | Poste spécifique occupé (si applicable), sinon `\N`.                   | Non          |
| `characters` | string  | Nom des personnages interprétés (si applicable), sinon `\N`.           | Oui (info complémentaire) |

---

## 6. `title.ratings.tsv.gz` - Notes et Votes

**Utilité :** Analyser la popularité et la qualité perçue des titres.

**Clé Primaire :** `tconst`

| Colonne        | Type    | Description                                                              | Conservation |
|-----------------|---------|--------------------------------------------------------------------------|--------------|
| `tconst`       | string  | Identifiant unique de l'œuvre.                                           | Oui (clé primaire) |
| `averageRating`| float   | Moyenne pondérée des notes des utilisateurs.                             | Oui          |
| `numVotes`     | integer | Nombre de votes reçus par l'œuvre.                                       | Oui          |

---

## 7. `name.basics.tsv.gz` - Informations sur les Personnes

**Utilité :** Identifier les personnes (acteurs, réalisateurs, scénaristes, etc.) et leurs contributions.

**Clé Primaire :** `nconst`

| Colonne            | Type    | Description                                                              | Conservation |
|---------------------|---------|--------------------------------------------------------------------------|--------------|
| `nconst`           | string  | Identifiant unique de la personne.                                      | Oui (clé primaire) |
| `primaryName`      | string  | Nom principal sous lequel la personne est créditée.                     | Oui          |
| `birthYear`        | YYYY    | Année de naissance.                                                     | Oui          |
| `deathYear`        | YYYY    | Année de décès (si applicable), sinon `\N`.                            | Non          |
| `primaryProfession`| array   | Les 3 professions principales de la personne.                           | Oui          |
| `knownForTitles`   | array   | Identifiants (`tconst`) des titres pour lesquels la personne est connue. | Oui          |

---

## 8. TMDB Dataset

**Utilité :** BDD complémentaire mais indispensable pour obtenir les affiches de film, d'autres notations. Un complément indispensable pour étoffer la base de données finale.

**Clé Primaire :** `imdb_id` qui servira à se connecter avec les autres tables via `tconst`

### Détails des Colonnes :

| Colonne                | Type    | Description                                                                                      | Conservation |
|-------------------------|---------|--------------------------------------------------------------------------------------------------|--------------|
| `adult`                | boolean | Indique si le film est pour un public adulte.                                                   | Oui          |
| `backdrop_path`        | string  | Chemin vers l’image de fond associée au film.                                                   | Non          |
| `budget`               | integer | Budget du film (en dollars).                                                                    | Oui          |
| `genres`               | array   | Genres du film.                                                                                 | Oui          |
| `homepage`             | string  | URL de la page officielle du film.                                                              | Non          |
| `id`                   | integer | Identifiant unique du film dans la base TMDB.                                                   | Oui          |
| `imdb_id`              | string  | Identifiant unique du film dans la base IMDB.                                                   | Oui          |
| `original_language`    | string  | Langue originale du film.                                                                       | Oui          |
| `original_title`       | string  | Titre original du film.                                                                         | Oui          |
| `overview`             | string  | Brève description du film.                                                                      | Oui          |
| `popularity`           | float   | Indicateur de popularité.                                                                       | Oui          |
| `poster_path`          | string  | Chemin vers l’affiche du film.                                                                  | Non          |
| `production_countries` | array   | Pays de production.                                                                             | Oui          |
| `release_date`         | date    | Date de sortie du film.                                                                         | Oui          |
| `revenue`              | integer | Chiffre d’affaires généré par le film.                                                         | Oui          |
| `runtime`              | integer | Durée en minutes.                                                                               | Oui          |
| `spoken_languages`     | array   | Langues parlées.                                                                               

⬅️[Retour à l'accueil](../../README.md)
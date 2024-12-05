# 1. Introduction

## 1.1 Contexte et problématique

Lancement Projet 2 : https://wildcodeschool.github.io/data-training-resources/projet/projet-2/

Besoins Clients
Vous êtes un Data Analyst freelance. Un cinéma en perte de vitesse situé dans la Creuse vous contacte. Il a décidé de passer le cap du digital en créant un site Internet taillé pour les locaux.
Pour aller encore plus loin, il vous demande de créer un moteur de recommandations de films qui à terme, enverra des notifications aux clients via Internet.
Le client aurait souhaité intégrer votre analyse et vos recommandations à son site pour pouvoir le tester, mais le timing est trop serré. Force de proposition, vous lui proposer de __le rendre testable au moyen d’un outil de votre choix__.
Le client a 2 besoins, qui peuvent être dans 2 outils séparés :
Obtenir quelques statistiques sur les films (type, durée), acteurs (nombre de films, type de films) et d’autres. Vous le ferez notamment à l’aide de visualisations. Vous pouvez utiliser un outil de business intelligence, ou des graphiques via Python.
Retourner une liste de films recommandés en fonction d’IDs ou de noms de films choisis par un utilisateur. Vous pouvez intégrer ces recommandations à un outil de dashboarding, ou bien faire ces recommandations directement depuis la ligne de commande (“input”).
L’objectif n’est pas d’arriver à un travail parfait, mais que le système fonctionne et que vous arriviez à déceler les points à améliorer.

## 1.2 Objectifs du projet

Définissez les objectifs principaux de l’analyse. Précisez si l’objectif est de découvrir des tendances, d’améliorer des processus décisionnels, d’établir des prédictions, etc.

## 1.3 Structure du rapport

Présentez brièvement l'organisation du rapport pour donner au lecteur une vue d’ensemble.

# 2. Etude de marché

Lien Etude de marché : Etude_de_marche_Projet2_Group3 https://docs.google.com/document/d/1uIoFViqM_fOSrjyiEBrKu9pOXLpGApk6YKIL2yHMHyU/edit?usp=sharing --> à retranscrire en markdown
Ressources utilisées : Sources de données à explorer https://docs.google.com/spreadsheets/d/1GaH4VPCha0H9my8RLxiMpdQvj0bA_dELLOBShhssL-Y/edit?usp=sharing

# 3. Exploration bases de données

“Après cette étude, réalisez une analyse approfondie de votre base de données pour identifier des tendances et caractéristiques spécifiques.

Cette analyse devrait inclure :
l’identification des acteurs les plus présents et les périodes associées
l’évolution de la durée moyenne des films au fil des années
la comparaison entre les acteurs présents au cinéma et dans les séries
l’âge moyen des acteurs
les films les mieux notés et les caractéristiques qu’ils partagent.”

“Sur la base des informations récoltées, vous pourrez affiner votre programmation en vous spécialisant par exemple sur les films des années 90 ou les genres d’action et d’aventure, afin de mieux répondre aux attentes du public identifié lors de l’étude de marché.”

## 3.1. Liste des bases de données :

Schématisation des tables IMDB
https://www.canva.com/design/DAGXx1BW4sc/E2SsEAMBRieuko4w6WEEUQ/view?utm_content=DAGXx1BW4sc&utm_campaign=designshare&utm_medium=link&utm_source=editor

### 1 - title.akas - Titres de films - dans différentes langues

Nom du fichier : title.akas.tsv.gz
Utilité : avoir les titres en français et titre original
==Clé Primaire : titleId (tconst)==


| Colonne         | Type    | Description                                                                                                                                                                                                                         | Conservation (O/N)                                    |
| ----------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| titleId         | string  | a tconst, an alphanumeric unique identifier of the title                                                                                                                                                                            | ML / Info                                             |
| ordering        | integer | a number to uniquely identify rows for a given titleId                                                                                                                                                                              |                                                       |
| title           | string  | the localized title                                                                                                                                                                                                                 | ML / Info                                             |
| region          | string  | the region for this version of the title                                                                                                                                                                                            | Filtre puis drop                                      |
| language        | string  | the language of the title                                                                                                                                                                                                           |                                                       |
| types           | array   | Enumerated set of attributes for this alternative title. One or more of the following: "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". New values may be added in the future without warning |                                                       |
| attributes      | array   | Additional terms to describe this alternative title, not enumerated                                                                                                                                                                 |                                                       |
| isOriginalTitle | boolean | 0: not original title; 1: original title                                                                                                                                                                                            | ML (si on n'a pas l'info de la nationalité ailleurs) |

### 2 - title.basics - Informations générales par Titres

Nom du fichier : title.basics.tsv.gz
Utilité : Type (Films,Séries, etc.) / Genre / Durée / Année de Sortie / Adultes /
Clé Primaire : 'tconst'
==A faire : Explode 'primaryProfession' & 'knowForTitles'==


| Colonne        | Type         | Description                                                                                                | Conservation (O/N)            |
| ---------------- | -------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------- |
| tconst         | string       | alphanumeric unique identifier of the title                                                                | ML / Info                     |
| titleType      | string       | the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)                          | ML / Info                     |
| primaryTitle   | string       | the more popular title / the title used by the filmmakers on promotional materials at the point of release |                               |
| originalTitle  | string       | original title, in the original language                                                                   |                               |
| isAdult        | boolean      | 0: non-adult title; 1: adult title                                                                         | Filtre à 0, puis drop        |
| startYear      | YYYY         | represents the release year of a title. In the case of TV Series, it is the series start year              | ML / Info                     |
| endYear        | YYYY         | TV Series end year. '\N' for all other title types                                                         |                               |
| runtimeMinutes |              | primary runtime of the title, in minutes                                                                   | ML / Info                     |
| genres         | string array | includes up to three genres associated with the title                                                      | Oui à get dummies, ML / Info |

### 3 - title.crew - Table intermédiaire Titre / Réalisateurs / Auteurs

Nom du fichier : title.crew.tsv.gz
Utilité : Table de liaison avec name.basics
Clé Primaire : 'tconst'
==voir autres tables==


| Colonne   | Type             | Description                                 | Conservation (O/N) |
| ----------- | ------------------ | --------------------------------------------- | -------------------- |
| tconst    | string           | alphanumeric unique identifier of the title | Info               |
| directors | array of nconsts | director(s) of the given title              | Info               |
| writers   | array of nconsts | writer(s) of the given title                | Info               |

Pas dans le big df mais dans le df info

### 4 - title.episode - Table intermédiaire : Liste des Episodes / Séries TV

Nom du fichier : title.episode.tsv.gz
Utilité : ==optionnel==


| Colonne       | Type    | Description                                     | Conservation (O/N) |
| --------------- | --------- | ------------------------------------------------- | -------------------- |
| tconst        | string  | alphanumeric identifier of episode              |                    |
| parentTconst  | string  | alphanumeric identifier of the parent TV Series |                    |
| seasonNumber  | integer | season number the episode belongs to            |                    |
| episodeNumber | integer | episode number of the tconst in the TV series   |                    |

--> pas besoin car on ne garde pas les épisodes de séries

### 5 - title.principals - Table principale des équipes de film

Nom du fichier : title.principals.tsv.gz
Distribution + Equipe de production des Films (Acteurs / Rôle)
==liaison entre title.basics et name.basics (qui a réalisé tel film, etc.)==


| Colonne    | Type    | Description                                               | Conservation (O/N) |
| ------------ | --------- | ----------------------------------------------------------- | -------------------- |
| tconst     | string  | alphanumeric unique identifier of the title               | Info               |
| ordering   | integer | a number to uniquely identify rows for a given titleId    |                    |
| nconst     | string  | alphanumeric unique identifier of the name/person         | Info               |
| category   | string  | the category of job that person was in                    | Info               |
| job        | string  | the specific job title if applicable, else '\N'           | Info               |
| characters | string  | the name of the character played if applicable, else '\N' | Info               |

### 6 - title.ratings - Tables des notations des films

Nom du fichier : title.ratings.tsv.gz
Utilité : notations / Votes / Succès etc.
==à relier avec les titres==


| Colonne       | Type   | Description                                         | Conservation (O/N) |
| --------------- | -------- | ----------------------------------------------------- | -------------------- |
| tconst        | string | alphanumeric unique identifier of the title         | ML / Info          |
| averageRating |        | weighted average of all the individual user ratings | ML / Info          |
| numVotes      |        | number of votes the title has received              | ML  / Info         |

### 7 - name.basics - Noms des acteurs / Professions / age

Nom du fichier : name.basics.tsv.gz
"knowForTitles" > info sur films >>> clés pour JOIN autres tables
"nconst" >>> clé pour JOIN title.principals
==A faire : Explode 'primaryProfession' & 'knowForTitles'==


| Colonne           | Type             | Description                                       | Conservation (O/N)        |
| ------------------- | ------------------ | --------------------------------------------------- | --------------------------- |
| nconst            | string           | alphanumeric unique identifier of the name/person | Info Films / Info acteurs |
| primaryName       | string           | name by which the person is most often credited   | Info Films / Info acteurs |
| birthYear         |                  | in YYYY format                                    | Info acteurs              |
| deathYear         |                  | in YYYY format if applicable, else '\N'           | Info acteurs              |
| primaryProfession | array of strings | the top-3 professions of the person               | Info acteurs              |
| knownForTitles    | array of tconsts | titles the person is known for                    | Info acteurs              |

### 8 - tmdb_full - Base de données complémentaires complètes

Nom du fichier : tmdb_full.csv
Utilité : ==imdb_id : L’ID IMDB du film, un identifiant unique dans la base de données IMDB
pour relier avec IMDB
Liens pour affiches du film
Infos Complémetaires à trier==


| Colonne                      | Type | Description                                                                                                    | Conservation (O/N)                   |
| ------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| adult                        |      | Un champ indiquant si le film est destiné à un public adulte, avec les valeurs “true” ou “false”.        | Filtre et drop                       |
| backdrop_path                |      | Le chemin d’accès à l’image de fond associée au film, utilisée à des fins de marketing et de promotion. | drop                                 |
| budget                       |      | Le budget du film, généralement en dollars ou dans la devise de référence.                                 | drop                                 |
| genres                       |      | Les genres du film, tels que “Action,” “Comedy,” “Science Fiction,” etc.                                 | ML / Info                            |
| homepage                     |      | L’URL de la page d’accueil officielle du film.                                                               | Info                                 |
| id                           |      | L’ID du film dans la base de données TMDB, utilisé pour identifier de manière unique chaque film.          | drop                                 |
| imdb_id                      |      | L’ID IMDB du film, un identifiant unique dans la base de données IMDB.                                       | ML (merge uniquement) / Info         |
| original_language            |      | La langue originale du film.                                                                                   | Info                                 |
| original_title               |      | Le titre original du film dans sa langue d’origine.                                                           | Info                                 |
| overview                     |      | Une brève description ou un résumé du film.                                                                 | Info                                 |
| popularity                   |      | Un indicateur de la popularité du film.                                                                       | ML / Info                            |
| poster_path                  |      | Le chemin d’accès à l’affiche du film, utilisée à des fins de marketing.                                 | Info                                 |
| production_countries         |      | Les pays de production du film, avec la possibilité d’avoir plusieurs pays listés.                          | ML / Info                            |
| release_date                 |      | La date de sortie du film.                                                                                     | ML / Info                            |
| revenue                      |      | Le chiffre d’affaires généré par le film, généralement en dollars ou dans la devise de référence.      | drop                                 |
| runtime                      |      | La durée en minutes du film.                                                                                  | ML / Info                            |
| spoken_languages             |      | Les langues parlées dans le film.                                                                             | drop                                 |
| status                       |      | Le statut du film, par exemple, “Released” ou “In Production”.                                             | filtre et drop                       |
| tagline                      |      | Une phrase ou un slogan court résumant le film, utilisée à des fins marketing.                              | info                                 |
| title                        |      | Le titre du film.                                                                                              | drop                                 |
| video                        |      | Un indicateur booléen indiquant si le film a une bande-annonce vidéo (“true” ou “false”).                | drop                                 |
| vote_average                 |      | La note moyenne attribuée au film par les utilisateurs ou les critiques.                                      | ML / Info (moy pondérée avec IMDB) |
| vote_count                   |      | Le nombre de votes ou de critiques reçus par le film.                                                         | ML / Info (somme avec IMDB)          |
| production_companies_name    |      | Le nom des sociétés de production associées au film.                                                        | Info                                 |
| production_companies_country |      | Le pays d’origine des sociétés de production associées au film.                                            | drop                                 |

### 9. data_bechdel.csv

* year : drop
* title : drop
* imdbid : ML (merge)
* rating : ML / Info

##

Liaisons

**name.basics :**
pas utilisable en l'état pour le merge
il faudra utiliser 'Knownfortitles'

**title.basics:**
id = 'tconst'
(idem 'tconst' dans 'title.crew' / 'title.episode' / 'title.principal' / 'title.ratings')

**title.principal**
id = 'nconst'
à relier avec 'nconst' de 'name.basics'

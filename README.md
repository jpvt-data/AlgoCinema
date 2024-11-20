## Liste des bases de données :


### 1 - Titres de films - dans différentes langues
#### Utilité : avoir les titres en français et titre original

==Clé Primaire : titleId (tconst)==

#### title.akas.tsv.gz

    titleId (string) - a tconst, an alphanumeric unique identifier of the title
    ordering (integer) – a number to uniquely identify rows for a given titleId
    title (string) – the localized title
    region (string) - the region for this version of the title
    language (string) - the language of the title
    types (array) - Enumerated set of attributes for this alternative title. One or more of the following: "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". New values may be added in the future without warning
    attributes (array) - Additional terms to describe this alternative title, not enumerated
    isOriginalTitle (boolean) – 0: not original title; 1: original title


### 2 - Informations générales par Titres

#### Utilité : Type (Films,Séries, etc.) / Genre / Durée / Année de Sortie / Adultes /

==Clé Primaire : tconst==

#### title.basics.tsv.gz

    tconst (string) - alphanumeric unique identifier of the title
    titleType (string) – the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)
    primaryTitle (string) – the more popular title / the title used by the filmmakers on promotional materials at the point of release
    originalTitle (string) - original title, in the original language
    isAdult (boolean) - 0: non-adult title; 1: adult title
    startYear (YYYY) – represents the release year of a title. In the case of TV Series, it is the series start year
    endYear (YYYY) – TV Series end year. '\N' for all other title types
    runtimeMinutes – primary runtime of the title, in minutes
    genres (string array) – includes up to three genres associated with the title

### 3 - Table intermédiaire Titre / Réalisateurs / Auteurs
#### Utilité : Table de liaison avec name.basics ==voir autres tables==

#### title.crew.tsv.gz

    tconst (string) - alphanumeric unique identifier of the title
    directors (array of nconsts) - director(s) of the given title
    writers (array of nconsts) – writer(s) of the given title

### 4 - Table intermédiaire : Liste des Episodes / Séries TV
#### Utilité : ==optionnel==

#### title.episode.tsv.gz

    tconst (string) - alphanumeric identifier of episode
    parentTconst (string) - alphanumeric identifier of the parent TV Series
    seasonNumber (integer) – season number the episode belongs to
    episodeNumber (integer) – episode number of the tconst in the TV series

### 5 - Table principale des équipes de film

#### Distribution + Equipe de production des Films (Acteurs / Rôle)

==liaison entre title.basics et name.basics (qui a réalisé tel film, etc.)==

#### title.principals.tsv.gz

    tconst (string) - alphanumeric unique identifier of the title
    ordering (integer) – a number to uniquely identify rows for a given titleId
    nconst (string) - alphanumeric unique identifier of the name/person
    category (string) - the category of job that person was in
    job (string) - the specific job title if applicable, else '\N'
    characters (string) - the name of the character played if applicable, else '\N'

### 6 - Tables des notations des films

#### Utilité : notations / Votes / Succès etc.
==à relier avec les titres==

#### title.ratings.tsv.gz

    tconst (string) - alphanumeric unique identifier of the title
    averageRating – weighted average of all the individual user ratings
    numVotes - number of votes the title has received

### 7 - Noms des acteurs / Professions / age

=="knowForTitles" > info sur films >>> clés pour JOIN autres tables==
=="nconst" >>> clé pour JOIN title.principals==
#### name.basics.tsv.gz

    nconst (string) - alphanumeric unique identifier of the name/person
    primaryName (string)– name by which the person is most often credited
    birthYear – in YYYY format
    deathYear – in YYYY format if applicable, else '\N'
    primaryProfession (array of strings)– the top-3 professions of the person
    knownForTitles (array of tconsts) – titles the person is known for

### 8 - Base de données complémentaires complètes

#### Utilité :

==imdb_id : L’ID IMDB du film, un identifiant unique dans la base de données IMDB
pour relier avec IMDB
Liens pour affiches du film
Infos Complémetaires à trier==
#### tmdb_full.csv

#### TMDB Dataset Details

    adult : Un champ indiquant si le film est destiné à un public adulte, avec les valeurs “true” ou “false”.
    backdrop_path : Le chemin d’accès à l’image de fond associée au film, utilisée à des fins de marketing et de promotion.
    budget : Le budget du film, généralement en dollars ou dans la devise de référence.
    genres : Les genres du film, tels que “Action,” “Comedy,” “Science Fiction,” etc.
    homepage : L’URL de la page d’accueil officielle du film.
    id : L’ID du film dans la base de données TMDB, utilisé pour identifier de manière unique chaque film.
    imdb_id : L’ID IMDB du film, un identifiant unique dans la base de données IMDB.
    original_language : La langue originale du film.
    original_title : Le titre original du film dans sa langue d’origine.
    overview : Une brève description ou un résumé du film.
    popularity : Un indicateur de la popularité du film.
    poster_path : Le chemin d’accès à l’affiche du film, utilisée à des fins de marketing.
    production_countries : Les pays de production du film, avec la possibilité d’avoir plusieurs pays listés.
    release_date : La date de sortie du film.
    revenue : Le chiffre d’affaires généré par le film, généralement en dollars ou dans la devise de référence.
    runtime : La durée en minutes du film.
    spoken_languages : Les langues parlées dans le film.
    status : Le statut du film, par exemple, “Released” ou “In Production”.
    tagline : Une phrase ou un slogan court résumant le film, utilisée à des fins marketing.
    title : Le titre du film.
    video : Un indicateur booléen indiquant si le film a une bande-annonce vidéo (“true” ou “false”).
    vote_average : La note moyenne attribuée au film par les utilisateurs ou les critiques.
    vote_count : Le nombre de votes ou de critiques reçus par le film.
    production_companies_name : Le nom des sociétés de production associées au film.
    production_companies_country : Le pays d’origine des sociétés de production associées au film.
## Méthodologie

- Livrable:
    - une table pour les critères de recommandations
    - une table pour les infos à afficher dans Streamlit
    - les deux tables liées entre elles.
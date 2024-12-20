# Analyse des KPI et Visualisation

## 🎯 Objectifs de l'analyse
L'objectif de ce projet est d'explorer les bases de données IMDb et TMDb afin d'en tirer des insights pertinents à l'aide de visualisations PowerBI.

Les analyses porteront sur :

1. **Vue générale des bases de données (Oeuvres, Supports, Genres, Pays)**
2. **L'identification des acteurs les plus présents et les périodes associées.**
3. **L'évolution de la durée moyenne des films au fil des années.**
4. **La comparaison entre les acteurs présents au cinéma et dans les séries.**
5. **L'âge moyen des acteurs.**
6. **Les films les mieux notés et les caractéristiques qu'ils partagent.**

---

## 📋 Méthodologie
### Étapes clés :

1. **Préparation des données :**
   - Nettoyage des datasets IMDb et TMDb pour éliminer les doublons et les valeurs manquantes.
   - Standardisation des formats de colonnes (dates, durées, notes, etc.).
   - Fusion des datasets pour enrichir les analyses (liens entre acteurs, films et séries).

2. **Exploration et création des KPI :**
   - Définition des indicateurs à suivre pour répondre aux objectifs.
   - Extraction et transformation des données nécessaires.

3. **Construction des visualisations Power BI :**
   - Création de rapports dynamiques et interactifs.
   - Mise en place de filtres et slicers pour explorer les données en détail.

---

## 1. **Schéma de liaison des Tables sur Power BI**
---

## 2. **📊 KPI** : Vue générale des bases de données

### Nombre d'oeuvres par supports et poids des oeuvres par type
<br>

![oeuvres_support](../images/kpi/3_répartition.PNG)
***Source : ImdB title.basics***

- Nombre total d'oeuvres (hors films Adulte) : ***10 885 933***
- Poids des Supports : ***82,1% Télévision, 15,75% Cinéma, 2,15% Autre***
- Pour le Cinéma : ***plus d'1 million de court métrages, 688 342 films***

**Remarque** : Nous pouvons travailler sur une base de 688342 films en nous concentrant uniquement sur les films, pour alléger la base de données et faciliter le traitement.

---

### Fréquences des Films par Genre
<br>

![genres](../images/kpi/4_genres.PNG)
***Source : ImdB title.basics***

- 3 Genres (Drame, Documentaire, Comédie) représentent ***72% des films***
- Le ***documentaire*** est particulièrement présent dans la base de données.

---

### Evolution du nombre de Films dans le temps
<br>

![décennie](../images/kpi/5_evolution_film.PNG)
***Source : ImdB title.basics***

- Les 3 décennies les plus prolifiques sont ***2000s, 2010s, 2020s***
- Depuis les années 2000, le ***documentaire*** est en forte expansion.
- Les années prolifiques pour le film d'Action sont entre ***1960 et 2000***

---
### Répartition des Films par Pays
<br>

![Pays](../images/kpi/7_pays.PNG)
***Source : TmdB Full***



### 1. Identification des acteurs les plus présents et les périodes associées
- **KPI :** Nombre de films/séries par acteur, période d'activité (années de début et de fin).
- **Visualisation :**
  - Graphique en barres pour les acteurs les plus présents.
  - Timeline pour représenter les périodes associées.

### 2. Évolution de la durée moyenne des films au fil des années
- **KPI :** Durée moyenne par décennie ou année.
- **Visualisation :**
  - Graphique en courbes montrant l'évolution au fil des décennies.
  - Histogramme pour une répartition plus détaillée.

### 3. Comparaison entre les acteurs présents au cinéma et dans les séries
- **KPI :** Proportion d'acteurs présents dans les films, les séries ou les deux.
- **Visualisation :**
  - Diagramme de Venn ou un graphique en barres empilées.
  - Tableau croisé dynamique pour une exploration plus fine.

### 4. Âge moyen des acteurs
- **KPI :** Calcul de l'âge moyen des acteurs par période et par genre (homme/femme).
- **Visualisation :**
  - Graphique en barres pour la moyenne par décennie.
  - Carte de chaleur pour explorer la répartition par âge et genre.

### 5. Les films les mieux notés et les caractéristiques qu'ils partagent
- **KPI :** Moyenne des notes des films, analyse des caractéristiques communes (genres, réalisateurs, durée, année de sortie).
- **Visualisation :**
  - Tableau récapitulatif des films les mieux notés.
  - Graphique en bulles pour explorer les corrélations (durée, notes, genres).

---

## Livrables
1. Rapport Power BI complet avec :
   - Dashboard interactif.
   - Pages dédiées pour chaque KPI.

2. Documentation expliquant les étapes suivies, les transformations effectuées et les sources des données.

---

## Conclusion
Cette analyse permettra d'extraire des insights clés sur les tendances des acteurs, les films, et les séries, tout en mettant en avant les outils de visualisation Power BI pour une compréhension claire et efficace des données.


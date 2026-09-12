# Partie 6 — Les cinq prompts ML

**Protocole :** une conversation neuve par prompt.

**`{contexte_dataset}`** désigne le bloc de [`contexte-dataset.md`](contexte-dataset.md) — profil statistique du dataset, pas le fichier complet.

---

## 6.1 — Stratégies de nettoyage

*Valeurs manquantes, doublons, valeurs aberrantes, variables catégorielles. Pour chacune : détection, traitement, risques associés.*

```text
Tu es data scientist. Tu prépares un dataset de capteurs en vue de prédire la consommation énergétique d'un bâtiment.

On te fournit le profil statistique du dataset, obtenu avec pandas. Tu n'as pas accès au fichier complet.

Tâche : proposer des stratégies de traitement pour quatre familles de problèmes :
1. les valeurs manquantes
2. les doublons
3. les valeurs aberrantes
4. les variables catégorielles

Pour chaque famille, structure ta réponse en trois points :
- **Détection** : comment identifier le problème, en citant les indices visibles dans le profil fourni
- **Traitement** : la ou les stratégies recommandées, et laquelle tu retiens
- **Risques** : ce que le traitement retenu peut dégrader, et dans quel cas il serait inadapté

Contraintes :
- appuie chaque recommandation sur une caractéristique effectivement observable dans le profil fourni ; cite la colonne et la valeur concernées
- ne propose aucune stratégie générique sans la rattacher à ce dataset
- si une anomalie du profil te paraît suspecte, signale-la explicitement avant de proposer un traitement
- si une information te manque pour trancher, écris "information non disponible dans le profil" plutôt que de supposer
- distingue les traitements applicables à la variable cible de ceux applicables aux variables explicatives

Profil du dataset :
<<<
{contexte_dataset}
>>>
```

**Grille de correction** — les huit indices que le profil contient. Un bon prompt doit en faire détecter le maximum :

| # | Indice | Attendu |
|---|---|---|
| 1 | `temperature_interieure_c` min = -999 | Sentinelle, pas outlier |
| 2 | Écart moyenne (15,1) / médiane (21,0), std 77,3 | Statistiques corrompues par la sentinelle |
| 3 | `humidite_pct` max = 317,4 | Borne physique dépassée |
| 4 | `consommation_kwh` min = -39,47 | Valeur négative impossible |
| 5 | `consommation_kwh` : 188 manquantes | **C'est la cible** : supprimer, jamais imputer |
| 6 | 183 vs 270 doublons | Quasi-doublons non détectables par déduplication exacte |
| 7 | 11 modalités de `zone` | Normalisation casse/séparateur → 5 zones |
| 8 | `type_jour` : 98 valeurs vides | Manquant déguisé en modalité |

**Hypothèse.** Les indices 1, 5 et 6 sont les plus discriminants : ils demandent une interprétation, pas une simple lecture. L'indice 1 est le piège principal — un modèle qui traite -999 par écart-type se fait piéger par les statistiques que cette valeur corrompt elle-même.

---

## 6.2 — Visualisations pertinentes

*Pour chaque visualisation : type de graphique, variables utilisées, objectif, interprétation attendue.*

```text
Tu es data scientist. Tu dois construire l'analyse exploratoire d'un dataset de capteurs afin de comprendre la consommation énergétique d'un bâtiment.

Tâche : proposer les visualisations les plus pertinentes pour cette analyse.

Pour chaque visualisation, indique :
- **Type de graphique** : le type précis (et non "un graphique")
- **Variables utilisées** : les colonnes en abscisse, en ordonnée, et en couleur ou facette le cas échéant
- **Objectif** : la question métier à laquelle elle répond
- **Interprétation attendue** : ce qu'on cherche à voir, et ce que révélerait un résultat contraire

Contraintes :
- propose entre 5 et 8 visualisations, classées par ordre d'utilité décroissante
- n'utilise que les colonnes présentes dans le profil fourni
- justifie chaque choix par une caractéristique du dataset, pas par une règle générale
- indique explicitement si une visualisation doit être faite avant ou après le nettoyage des données
- ne propose aucune visualisation dont la lecture serait impossible ou illisible au vu du volume (11 070 points)

Profil du dataset :
<<<
{contexte_dataset}
>>>
```

**Hypothèse.** Le dataset a trois caractéristiques qu'une bonne réponse doit exploiter : la **structure temporelle** (série horaire sur 90 jours), les **5 zones** (facettes ou couleur), et une **cible continue asymétrique**. Le risque est un catalogue générique — histogramme, boxplot, heatmap de corrélation — sans lien avec ces spécificités.

Point de vigilance : la contrainte sur le volume teste si le modèle évite le nuage de points brut de 11 070 observations, illisible sans agrégation ou transparence.

---

## 6.3 — Modèles de prédiction

*Pour chaque modèle : principe, avantages, limites, type de problème, métriques pertinentes.*

```text
Tu es data scientist. Tu dois choisir un modèle pour prédire la consommation énergétique horaire d'un bâtiment à partir de données de capteurs.

Tâche : proposer plusieurs modèles adaptés à ce problème.

Pour chaque modèle, indique :
- **Principe** : comment il fonctionne, en deux phrases
- **Avantages** : sur ce dataset précisément
- **Limites** : sur ce dataset précisément
- **Type de problème** : la famille de problème à laquelle il répond
- **Métriques pertinentes** : celles qui conviennent pour l'évaluer ici

Contraintes :
- propose entre 3 et 5 modèles, du plus simple au plus complexe
- commence par un modèle de référence simple servant de point de comparaison
- justifie chaque choix par une caractéristique du dataset fourni
- précise le type de problème avant de citer les métriques, et vérifie que les métriques citées correspondent bien à ce type
- indique comment tu construirais le jeu de test, en tenant compte de la nature des données
- si un modèle nécessite un prétraitement particulier, précise lequel

Profil du dataset :
<<<
{contexte_dataset}
>>>
```

**Hypothèse.** Deux points départagent une réponse générique d'une réponse adaptée :

1. **Le type de problème** — c'est une **régression** (cible continue). Un modèle qui proposerait des métriques de classification serait incohérent.
2. **Le split train/test** — les données sont une **série temporelle**. Un split aléatoire ou une validation croisée classique constitue une fuite de données : on entraînerait sur le futur pour prédire le passé. La contrainte « en tenant compte de la nature des données » teste ce point sans le souffler.

---

## 6.4 — Métriques de classification

*Accuracy, Precision, Recall, F1-score, ROC-AUC. Définition, interprétation, exemple concret, contexte d'utilité.*

```text
Tu es formateur en machine learning. Tu expliques les métriques d'évaluation à des analystes qui découvrent la classification.

Tâche : expliquer les cinq métriques suivantes : Accuracy, Precision, Recall, F1-score, ROC-AUC.

Pour chacune, fournis :
- **Définition** : ce qu'elle mesure, avec sa formule
- **Interprétation** : comment lire sa valeur, et ce qu'une valeur élevée ou faible signifie réellement
- **Exemple concret** : un cas chiffré, avec les nombres de vrais/faux positifs et négatifs
- **Contexte d'utilité** : dans quelle situation elle est particulièrement pertinente, et dans quelle situation elle est trompeuse

Contraintes :
- utilise un même exemple fil rouge pour les cinq métriques, afin que les valeurs soient comparables entre elles
- l'exemple doit être un cas déséquilibré, où la classe positive est minoritaire
- pour chaque métrique, indique explicitement au moins un cas où s'y fier seule conduirait à une mauvaise décision
- ne confonds pas Precision et Recall : vérifie que tes formules correspondent bien aux définitions que tu donnes
- si deux métriques peuvent se contredire, explique pourquoi

Termine par un tableau récapitulatif à cinq lignes : métrique, ce qu'elle privilégie, quand la choisir.
```

**Hypothèse.** Sujet très documenté, donc risque élevé de réponse fluide contenant une **erreur classique**. Trois pièges à surveiller :

- confusion Precision / Recall dans les formules ;
- Accuracy présentée comme fiable sans mention du déséquilibre ;
- ROC-AUC présentée comme robuste sur données déséquilibrées, alors que la Precision-Recall AUC est préférable dans ce cas.

La contrainte de l'exemple fil rouge déséquilibré est conçue pour rendre ces erreurs visibles : avec une classe positive à 2 %, une Accuracy de 98 % s'obtient en prédisant toujours « négatif ».

---

## 6.5 — Métriques de régression

*MAE, MSE, RMSE. Définition, interprétation, exemple concret, contexte d'utilité.*

```text
Tu es formateur en machine learning. Tu expliques les métriques d'évaluation à des analystes qui découvrent la régression.

Tâche : expliquer les trois métriques suivantes : MAE, MSE, RMSE.

Pour chacune, fournis :
- **Définition** : ce qu'elle mesure, avec sa formule
- **Interprétation** : comment lire sa valeur, et dans quelle unité elle s'exprime
- **Exemple concret** : un cas chiffré, calculé pas à pas
- **Contexte d'utilité** : dans quelle situation elle est particulièrement pertinente

Contraintes :
- utilise un même jeu de prédictions fil rouge pour les trois métriques, contenant au moins une erreur nettement plus grande que les autres
- calcule effectivement les trois valeurs sur cet exemple et montre le détail du calcul
- explique ce que l'écart entre MAE et RMSE révèle sur la distribution des erreurs
- précise l'unité de chaque métrique par rapport à la variable cible
- relie ces métriques au dataset de consommation énergétique : laquelle choisirais-tu pour ce cas, et pourquoi

Contexte d'application : prédiction de la consommation énergétique horaire d'un bâtiment, exprimée en kWh, dont la distribution est fortement asymétrique (moyenne 27,3 kWh, médiane 13,1 kWh, maximum 898,5 kWh).
```

**Hypothèse.** La contrainte « au moins une erreur nettement plus grande » rend visible la propriété essentielle : **RMSE pénalise davantage les grandes erreurs que MAE**, et l'écart entre les deux mesure la dispersion des erreurs.

Le rattachement au dataset teste la capacité à raisonner sur un cas concret : avec une cible asymétrique et des pics à 898 kWh, le choix MAE vs RMSE dépend du coût métier d'une grosse erreur ponctuelle — question à laquelle le modèle doit répondre en signalant qu'elle dépend d'un arbitrage, pas d'une règle technique.

---

## Grille d'observation

| Tâche | Ancrage | Couverture | Exactitude | Spécificité | Cohérence |
|---|---|---|---|---|---|
| 6.1 Nettoyage | | /8 indices | | | |
| 6.2 Visualisations | | | | | |
| 6.3 Modèles | | | | | |
| 6.4 Métriques classif. | | /5 métriques | | | |
| 6.5 Métriques régression | | /3 métriques | | | |

# Partie 6 — Prompt Engineering pour le Machine Learning

> **Énoncé.** Créer cinq prompts à partir du dataset des capteurs :
> 1) stratégies de traitement des valeurs manquantes, doublons, valeurs aberrantes et variables catégorielles (détection, traitement, risques) ;
> 2) visualisations les plus pertinentes (type de graphique, variables, objectif, interprétation attendue) ;
> 3) modèles adaptés à la prédiction de consommation (principe, avantages, limites, type de problème, métriques) ;
> 4) explication des métriques de classification (Accuracy, Precision, Recall, F1, ROC-AUC) ;
> 5) explication des métriques de régression (MAE, MSE, RMSE).

---

## 1. Ce qui change dans cette partie

Les parties 1 à 5 demandaient au LLM de **traiter une donnée**. La partie 6 lui demande de **conseiller sur une méthode**. C'est un renversement complet du rapport à la vérification.

| | Parties 1 à 5 | Partie 6 |
|---|---|---|
| Nature de la sortie | Un résultat | Une recommandation |
| Vérification | Confronter à la source | Confronter à l'état de l'art |
| Hallucination typique | Un fait inventé | Un conseil plausible mais inadapté |
| Détection | Objective | Demande une expertise |

**Le risque se déplace et devient plus difficile à repérer.** Un modèle qui invente un numéro de facture se détecte immédiatement (Partie 5.4). Un modèle qui recommande d'imputer par la moyenne une variable dont la distribution est asymétrique produit un conseil parfaitement formulé, généralement correct, et faux *ici*.

**Conséquence pour les prompts :** il ne suffit pas de demander des recommandations. Il faut exiger qu'elles soient **rattachées aux caractéristiques observées du dataset**, exactement comme la Partie 3 avait exigé que les recommandations soient ancrées dans les avis clients.

---

## 2. Le dataset

Le fichier [`data/capteurs_batiment.csv`](../data/capteurs_batiment.csv) est généré par [`scripts/generer_dataset_capteurs.py`](../scripts/generer_dataset_capteurs.py) — générateur déterministe, seed fixe, donc reproductible.

**11 070 relevés horaires** sur 90 jours (janvier à mars 2025), 5 zones d'un bâtiment, 9 colonnes.

| Colonne | Type | Description |
|---|---|---|
| `id_releve` | entier | Identifiant du relevé |
| `horodatage` | datetime | Date et heure du relevé |
| `zone` | catégorielle | Zone du bâtiment |
| `temperature_interieure_c` | numérique | Température intérieure (°C) |
| `temperature_exterieure_c` | numérique | Température extérieure (°C) |
| `humidite_pct` | numérique | Humidité relative (%) |
| `occupation_personnes` | entier | Nombre de personnes présentes |
| `type_jour` | catégorielle | ouvré / weekend / férié |
| `consommation_kwh` | numérique | **Variable cible** — consommation (kWh) |

### Les défauts volontaires du dataset

Le générateur introduit délibérément quatre familles de défauts. Ils constituent la **grille de correction** de la question 6.1 : un bon prompt doit conduire le modèle à les identifier.

**Valeurs manquantes** — 5 colonnes concernées, de 0,89 % à 6,15 % :

| Colonne | Manquantes | Taux |
|---|---|---|
| `humidite_pct` | 681 | 6,15 % |
| `occupation_personnes` | 527 | 4,76 % |
| `temperature_interieure_c` | 342 | 3,09 % |
| `consommation_kwh` | 188 | 1,70 % |
| `type_jour` | 98 | 0,89 % |

Le cas de `consommation_kwh` est particulier : c'est la **variable cible**. Une ligne sans cible ne peut pas servir à l'entraînement supervisé — l'imputer serait une faute méthodologique.

**Doublons** — deux natures distinctes :

| Type | Nombre |
|---|---|
| Lignes strictement identiques | 183 |
| Doublons de clé métier (horodatage + zone) | 270 |

L'écart de 87 lignes correspond à des **quasi-doublons** : même horodatage et même zone, mais mesures légèrement différentes. Une déduplication exacte ne les détecte pas.

**Valeurs aberrantes** — trois mécanismes différents :

| Colonne | Anomalie | Nature |
|---|---|---|
| `temperature_interieure_c` | 62 valeurs à **-999** | **Sentinelle** — code d'erreur capteur, pas un outlier statistique |
| `humidite_pct` | max à **317,4 %** | Physiquement impossible (borne : 100 %) |
| `consommation_kwh` | min à **-39,47** | Négatif, physiquement impossible |
| `consommation_kwh` | 1 113 outliers IQR (10 %) | Possiblement légitimes — pics de consommation réels |

Le cas `-999` est le plus instructif : il **corrompt les statistiques** (moyenne de `temperature_interieure_c` à 15,1 °C avec un écart-type de 77,3 alors que la médiane est à 21,0 °C). Un traitement par écart-type serait piégé ; il faut d'abord reconnaître la sentinelle.

**Variables catégorielles non normalisées :**

| Variable | Modalités brutes | Après normalisation |
|---|---|---|
| `zone` | **11** | **5** |
| `type_jour` | 4 (dont une vide) | 3 + manquants |

Les 11 modalités de `zone` sont des variantes de casse et de séparateur : `Bureau_Nord`, `bureau_nord`, `BUREAU NORD` désignent la même zone. Un encodage naïf créerait 11 colonnes au lieu de 5, fragmentant le signal.

Le profil complet est dans [`resultats/profil_dataset_capteurs.json`](../resultats/profil_dataset_capteurs.json), produit par [`scripts/profiler_dataset.py`](../scripts/profiler_dataset.py).

---

## 3. Méthode retenue pour les prompts

**Question 6.1 (nettoyage)** — le prompt fournit un **extrait du dataset et son profil statistique**, pas le fichier entier. C'est le cas d'usage réaliste : on ne colle pas 11 000 lignes dans un LLM. On lui donne ce qu'un `df.describe()` et un `df.info()` produisent, et on lui demande d'interpréter.

La grille de correction est connue à l'avance (les quatre familles de défauts ci-dessus), ce qui rend l'évaluation **objective** — contrairement aux questions 6.2 et 6.3.

**Questions 6.2 et 6.3 (visualisations, modèles)** — pas de réponse unique. L'évaluation porte sur :
- la **pertinence au dataset** : le modèle exploite-t-il la structure temporelle, les 5 zones, la variable cible continue ?
- la **cohérence interne** : les métriques proposées correspondent-elles au type de problème annoncé ?
- l'**absence de catalogue générique** : une liste de 10 modèles standards sans lien avec les données serait un échec.

**Questions 6.4 et 6.5 (métriques)** — ce sont les seules questions **purement pédagogiques** de l'atelier. La vérification est factuelle : les définitions sont-elles exactes ? Les formules correctes ? Les exemples cohérents ?

C'est aussi l'occasion de tester un risque spécifique : sur un sujet aussi documenté, un LLM produit facilement une réponse fluide contenant une **erreur classique** — confondre précision et rappel, ou présenter ROC-AUC comme fiable sur données déséquilibrées.

---

## 4. Grille d'évaluation

| Critère | Application |
|---|---|
| Ancrage | Les recommandations citent-elles des caractéristiques réelles du dataset ? |
| Couverture | Les défauts connus sont-ils tous identifiés (6.1) ? |
| Exactitude | Les définitions et formules sont-elles justes (6.4, 6.5) ? |
| Spécificité | Réponse adaptée au cas, ou catalogue générique ? |
| Cohérence | Métriques compatibles avec le type de problème annoncé ? |
| Piège évité | Sentinelle -999, cible manquante, quasi-doublons |

---

## Prompts testés

Voir [`prompts.md`](prompts.md).

## Résultats et analyse

Voir [`resultats.md`](resultats.md).

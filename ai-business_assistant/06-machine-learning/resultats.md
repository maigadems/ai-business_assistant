# Partie 6 — Résultats obtenus et analyse

**LLM utilisé :** ChatGPT (OpenAI)
**Date d'exécution :** 12 septembre 2025

---

## 6.1 — Stratégies de nettoyage

**Prompt :** voir [`prompts.md`](prompts.md#61--stratégies-de-nettoyage)
**Contexte fourni :** [`contexte-dataset.md`](contexte-dataset.md) — profil statistique, pas le fichier

![Résultat des stratégies de nettoyage](captures/01-nettoyage.png)

La réponse complète est structurée en quatre familles (manquants, doublons, aberrantes, catégorielles), chacune en trois points (détection, traitement, risques), suivie d'un tableau de synthèse en 10 lignes.

### Couverture de la grille : 8/8

| # | Indice | Détecté | Interprétation produite |
|---|---|:---:|---|
| 1 | `temperature_interieure_c` min = -999 | ✅ | « probablement un **code d'erreur** » → NaN puis imputation |
| 2 | Moyenne 15,1 vs médiane 21,0, std 77,3 | ✅ | « le -999 **déforme fortement les statistiques** » |
| 3 | `humidite_pct` max = 317,4 | ✅ | « physiquement suspect », seuil > 100 % → NaN |
| 4 | `consommation_kwh` min = -39,47 | ✅ | « incompatibles avec l'interprétation de la variable cible » |
| 5 | 188 manquantes sur la cible | ✅ | « **ne pas imputer** [...] fabriquer une cible » |
| 6 | 183 vs 270 doublons | ✅ | « une simple déduplication **ne résout pas** le problème des 270 collisions » |
| 7 | 11 modalités de `zone` | ✅ | Table de correspondance explicite vers 5 zones |
| 8 | `type_jour` : 98 vides | ✅ | Reconstruction depuis `horodatage` + calendrier |

**Les trois indices discriminants sont tous traités correctement.**

### Le piège principal est évité

L'indice n° 1 était conçu comme un piège récursif : `-999` corrompt les statistiques (`std` = 77,3) qui serviraient à le détecter. Un modèle appliquant une règle « écarter au-delà de 3 écarts-types » ne l'aurait jamais isolé, puisque `-999` est à 13 écarts-types de la moyenne — mais que cette moyenne est elle-même tirée vers le bas par lui.

Le modèle a raisonné dans le bon ordre :

> « moyenne de **15,108** et un écart-type de **77,325**, **incohérents avec ses quartiles** »

Il compare la moyenne aux quartiles (Q1 20,45 / médiane 21,00 / Q3 21,55), constate l'incohérence, et en déduit la présence d'une valeur sentinelle. **C'est un raisonnement sur la cohérence interne du profil**, pas l'application d'une recette.

Sa conclusion finale l'énonce explicitement :

> « ne pas appliquer aveuglément `dropna()` ou une détection d'outliers statistique »

### La distinction cible / explicatives est correctement appliquée

La contrainte demandait de distinguer les traitements applicables à la cible. Le modèle produit la bonne réponse méthodologique :

> « Pour `consommation_kwh`, qui est la cible, je recommande de **ne pas imputer** les 188 valeurs [...] supprimer ces observations de l'ensemble d'apprentissage est préférable à **fabriquer une cible** »

Et il en tire la conséquence chiffrée : 11 070 → 10 882 observations.

Il va plus loin en identifiant le risque méthodologique sous-jacent :

> « Imputer la cible pourrait **introduire artificiellement une relation** entre les variables explicatives et la consommation. »

C'est exact : imputer une cible à partir des features revient à apprendre au modèle sa propre règle d'imputation.

Même rigueur sur les valeurs extrêmes de la cible — il refuse de winsoriser :

> « Supprimer tous les grands `consommation_kwh` pourrait éliminer de **vrais pics énergétiques, précisément intéressants** pour la prédiction. »

### Les quasi-doublons sont identifiés sans que l'écart soit souligné

Le profil donnait 183 lignes strictement identiques et 270 couples `(horodatage, zone)` dupliqués, **sans commenter l'écart**. Le modèle l'a exploité :

> « Une simple déduplication sur toutes les colonnes **ne résout pas** le problème des 270 collisions non identiques. »

Il refuse par ailleurs la suppression automatique et propose une comparaison ligne à ligne — comportement prudent adapté à un cas où la règle de résolution est inconnue.

### La formule d'incertitude est utilisée cinq fois

La contrainte imposait d'écrire « information non disponible dans le profil » plutôt que de supposer. Elle est employée cinq fois, à chaque fois à bon escient :

| Usage | Ce qui manque réellement |
|---|---|
| Calendrier des jours fériés | ✅ absent du profil |
| Longueur des séquences manquantes | ✅ `isna().sum()` ne la donne pas |
| Règle de résolution des collisions d'`id_releve` | ✅ absente |
| Fréquence des valeurs > 100 % et < 0 | ✅ `describe()` ne donne que min/max |
| Correspondance métier des 5 zones | ✅ absente |

Le quatrième usage est le plus fin : le modèle constate qu'un `describe()` ne permet pas de fixer un seuil de winsorisation, faute de connaître la **fréquence** des valeurs extrêmes — seulement leur existence.

**C'est la cinquième confirmation du principe dégagé en Partie 3** : donner une formule à produire fait émerger l'incertitude, là où une simple interdiction d'inventer la laisserait implicite.

### Deux réserves

**1. L'interpolation temporelle est recommandée sans vérification de faisabilité.** Le modèle propose d'interpoler `temperature_interieure_c`, `humidite_pct` et `occupation_personnes` « sous réserve de disposer de relevés voisins ». La réserve est posée, mais le dataset comporte des doublons de clé `(horodatage, zone)` — l'index temporel n'est donc pas propre au moment où l'interpolation s'appliquerait. L'ordre des opérations (dédupliquer avant d'interpoler) n'est pas explicité.

**2. `occupation_personnes` : l'interpolation est discutable.** Le modèle le signale lui-même (« peut lisser des changements brusques ») mais la retient quand même. Pour une variable de comptage à forte variation horaire — 0 la nuit, pic en journée — une imputation par 0 hors horaires de bureau, ou par la médiane zone × heure, serait mieux adaptée. La réserve est correcte, l'arbitrage discutable.

### Ce que cette tâche établit

**1. Fournir un profil statistique suffit à obtenir des conseils ancrés.** Le modèle n'a jamais eu accès aux 11 070 lignes. Un `describe()`, un `isna()`, un `value_counts()` et 8 lignes d'extrait ont suffi à produire une stratégie de nettoyage complète et spécifique. **C'est le cas d'usage réaliste**, et il fonctionne.

**2. La contrainte d'ancrage transforme la nature de la réponse.** Chaque recommandation cite une colonne et une valeur. Aucune stratégie générique n'est proposée « en général » — contraste net avec la Partie 3, où le prompt vague produisait une vingtaine de recommandations hors-sol.

**3. Le raisonnement sur la cohérence interne du profil est le point fort.** Comparer moyenne et quartiles pour détecter une sentinelle, ou comparer deux compteurs de doublons pour déduire des quasi-doublons, ne s'obtient pas par application de recettes. C'est ce qui distingue ici un conseil expert d'un catalogue.

**4. Le risque « conseil plausible mais inadapté » ne s'est pas matérialisé sur cette tâche** — mais il reste entier sur les questions 6.2 et 6.3, où il n'existe pas de grille de correction objective.

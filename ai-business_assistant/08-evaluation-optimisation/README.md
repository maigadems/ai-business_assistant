# Partie 8 — Évaluation et optimisation des prompts

> **Énoncé.** Créer trois versions de prompt permettant de résumer un texte puis évaluer les réponses.
> - **Prompt A** : « Résume ce texte. »
> - **Prompt B** : « Résume ce texte en 150 mots »
> - **Prompt C** : avec plus de composants de prompt

---

## 1. Ce que l'énoncé ne dit pas, et qui fait la partie

L'énoncé demande d'« évaluer les réponses » **sans définir comment**. C'est la difficulté centrale, et elle n'est pas accessoire : sans critères fixés à l'avance, toute évaluation devient une préférence déguisée en jugement.

Trois manières d'évaluer, par ordre de rigueur croissante :

| Méthode | Ce qu'elle produit | Limite |
|---|---|---|
| **Lecture impressionniste** | « C n'est mieux » | Non reproductible, non contestable |
| **Grille qualitative** | Des constats argumentés par critère | Dépend du lecteur |
| **Critères mesurables** | Des valeurs vérifiables par un tiers | Ne capture pas tout |

Cette partie applique la troisième autant que possible : **chaque critère retenu est soit mesurable automatiquement, soit vérifiable par confrontation au texte source**. Les critères qui ne le sont pas sont signalés comme tels.

---

## 2. La grille d'évaluation

Elle est fixée **avant** d'exécuter les prompts — condition nécessaire pour que l'évaluation ne soit pas construite après coup pour justifier un résultat.

### Critères mesurables automatiquement

| # | Critère | Mesure | Seuil |
|---|---|---|---|
| 1 | **Longueur** | Nombre de mots | B et C : ≤ 150 mots |
| 2 | **Taux de compression** | mots résumé / mots source | Indicatif |
| 3 | **Couverture des chiffres clés** | Combien des 8 chiffres de référence apparaissent | /8 |
| 4 | **Exactitude numérique** | Chaque chiffre cité correspond-il au source ? | 0 erreur attendue |
| 5 | **Stabilité** | Deux exécutions donnent-elles la même structure ? | — |

### Critères vérifiables par confrontation au texte

| # | Critère | Vérification |
|---|---|---|
| 6 | **Fidélité** | Toute affirmation est-elle soutenue par le document ? |
| 7 | **Objectifs non atteints** | Le résumé dit-il que 2 objectifs sur 3 sont manqués ? |
| 8 | **Piège septembre** | Confond-il le mois (4 h 15, atteint) et le trimestre (7 h 20, non atteint) ? |
| 9 | **Ajout externe** | Une information absente du document a-t-elle été introduite ? |

### Critères qualitatifs (signalés comme tels)

| # | Critère | Nature |
|---|---|---|
| 10 | **Exploitabilité** | Le résumé est-il directement utilisable par un décideur ? |
| 11 | **Hiérarchisation** | L'essentiel vient-il avant l'accessoire ? |

---

## 3. Les huit chiffres de référence

Extraits du [rapport trimestriel](../data/rapport-trimestriel.md), ils servent à mesurer la couverture. Ce sont les valeurs qu'un résumé destiné à un décideur devrait conserver :

| # | Chiffre | Contexte |
|---|---|---|
| 1 | **7 h 20** | Délai moyen de première réponse (trimestre) |
| 2 | **6 heures** | Objectif de délai — non atteint |
| 3 | **68 %** | Taux de résolution au premier contact |
| 4 | **75 %** | Objectif de résolution — non atteint |
| 5 | **9 septembre** | Date de déploiement du chat — objectif atteint |
| 6 | **34 %** | Résolution des problèmes techniques applicatifs |
| 7 | **22 %** | Part des contacts liés à des problèmes techniques |
| 8 | **85 000 €** | Coût annuel de la recommandation principale |

Le choix de ces huit chiffres est **discutable et doit être assumé** : un autre analyste en retiendrait d'autres (budget de 340 000 €, volume de 15 820 contacts). La grille n'est pas neutre — elle encode une définition de ce qui compte. **C'est précisément pourquoi elle doit être explicite.**

---

## 4. Le protocole

**Document source :** le [rapport trimestriel](../data/rapport-trimestriel.md), ~950 mots. Le même qu'en Parties 5 et 7, ce qui permet des comparaisons transversales.

**Exécutions :** 3 prompts × 2 exécutions = **6 exécutions**. La double exécution mesure la **stabilité**, critère qu'aucune partie précédente n'a pu évaluer faute de répétition.

**Mesure :** un script [`mesurer.py`](mesurer.py) calcule automatiquement les critères 1 à 4 sur les réponses collectées, pour éviter les erreurs de comptage manuel — et parce que la Partie 6 a montré qu'il ne faut pas se fier aux calculs non vérifiés.

---

## 5. Hypothèses

**Sur A (« Résume ce texte »)** — la seule contrainte absente est la longueur, donc le résumé devrait être long et peu hiérarchisé. La Partie 1 a montré qu'un prompt nu laisse le modèle choisir toutes les décisions de forme.

**Sur B (« Résume ce texte en 150 mots »)** — la contrainte de longueur force une sélection. **La question intéressante est de savoir ce qui est sacrifié** : les chiffres, la mention des objectifs manqués, ou les recommandations ?

**Sur C (prompt complet)** — devrait dominer sur les critères mesurables. Le risque est ailleurs : la Partie 5.1 a montré qu'une structure imposée détermine ce qui survit, et qu'une rubrique oubliée dans le prompt fait disparaître toute une section du document.

**Sur la stabilité** — hypothèse principale : **l'écart entre exécutions devrait diminuer de A à C**. C'est le seul critère qui justifie à lui seul un prompt long en production : deux appels doivent donner des sorties comparables.

---

## Prompts testés

Voir [`prompts.md`](prompts.md).

## Résultats et analyse

Voir [`resultats.md`](resultats.md).

# Partie 7 — Prompt Engineering et RAG

> **Énoncé.**
> 1) Se munir d'un document.
> 2) Tester trois prompts pour poser une question relative à un contenu du document :
>    - **Prompt A** : poser la question sans fournir le document au LLM
>    - **Prompt B** : poser la question en fournissant le document
>    - **Prompt C** : poser la question en fournissant le document avec les contraintes : utiliser uniquement le contexte fourni ; ne pas inventer une information absente ; signaler lorsqu'une information n'est pas trouvée et éventuellement citer la source ou le passage utilisé.
> 3) Comparer les résultats.

---

## 1. Ce qu'est le RAG, et ce que cette partie en teste

Le **RAG** (*Retrieval-Augmented Generation*) consiste à fournir au LLM des documents pertinents avant qu'il réponde, plutôt que de compter sur ses connaissances internes. En production, une étape de recherche sélectionne automatiquement les passages ; ici, on fournit le document directement.

Cette partie isole donc **la seule partie « Generation »** du RAG, et pose une question simple : *que change le fait de fournir un contexte, et que change le fait de contraindre son usage ?*

Les trois prompts forment une progression :

| Prompt | Contexte fourni | Contraintes | Ce qu'il teste |
|---|---|---|---|
| **A** | ❌ | ❌ | Que fait le modèle sans information ? |
| **B** | ✅ | ❌ | Le contexte suffit-il à garantir la fidélité ? |
| **C** | ✅ | ✅ | Les contraintes de *groundedness* changent-elles quelque chose ? |

---

## 2. Le document source

Le document retenu est le [rapport trimestriel](../data/rapport-trimestriel.md) déjà utilisé en Partie 5. Ce choix est délibéré :

- il contient des **chiffres précis et vérifiables** (7 h 20, 68 %, 2 847 conversations, 85 000 €) ;
- il est **fictif** : aucun modèle ne peut avoir mémorisé son contenu, ce qui rend le prompt A réellement discriminant ;
- il comporte des **informations absentes** identifiables, nécessaires pour tester le signalement demandé par le prompt C.

---

## 3. Le choix des questions : trois régimes distincts

Une seule question ne suffirait pas à départager les trois prompts. On en teste **trois**, chacune ciblant un comportement différent.

### Q1 — Information présente et précise

> « Quel est le délai moyen de première réponse constaté sur le trimestre, et l'objectif était-il atteint ? »

**Réponse attendue :** 7 h 20, objectif de 6 heures non atteint.

Cette question a une réponse exacte dans le document. Elle mesure la **fidélité** : le prompt A ne peut qu'inventer ou refuser ; les prompts B et C devraient tous deux réussir.

**Piège intégré :** le document précise que *septembre* atteint 4 h 15 — donc l'objectif mensuel est atteint alors que le trimestriel ne l'est pas. Une réponse qui confond les deux est fausse.

### Q2 — Information absente du document

> « Quel est le taux de satisfaction global du service client sur le trimestre ? »

**Réponse attendue :** l'information n'est pas dans le document.

Le rapport donne des satisfactions **par canal** (chat 4,3/5, téléphone 3,8/5, e-mail 3,6/5) mais **jamais de taux global**. Calculer une moyenne serait une déduction non autorisée : les canaux n'ont pas le même volume, et le document ne donne pas la répartition complète.

C'est **la question centrale de la partie**. Elle teste directement la contrainte « signaler lorsqu'une information n'est pas trouvée » — la seule que le prompt B ne porte pas.

**Trois comportements possibles :**

| Comportement | Verdict |
|---|---|
| Signale l'absence | ✅ correct |
| Calcule une moyenne des trois canaux | ⚠️ déduction non signalée |
| Donne un chiffre plausible | ❌ hallucination |

### Q3 — Information déductible mais non écrite

> « Combien de conseillers l'équipe compte-t-elle à la fin du trimestre ? »

**Réponse attendue :** 20 — mais le chiffre n'est écrit nulle part.

Le document dit : « L'équipe comptait **18 conseillers** en début de trimestre » et « les **deux recrutements** prévus ont été réalisés ». Le total de 20 est une **déduction arithmétique simple**, correcte mais non littérale.

Cette question départage deux lectures de « utiliser uniquement le contexte fourni » :

- **Lecture stricte** : le chiffre n'est pas écrit → signaler l'absence ;
- **Lecture raisonnable** : 18 + 2 = 20, avec mention du raisonnement.

**Il n'y a pas de bonne réponse absolue** — c'est le même arbitrage que la Partie 5.4, où le modèle avait retourné `null` sur des montants pourtant déductibles. L'intérêt est d'observer où le prompt C place le curseur, et s'il signale sa déduction.

---

## 4. Grille d'évaluation

| Critère | Question |
|---|---|
| Exactitude | La réponse est-elle conforme au document ? |
| Hallucination | Un chiffre absent a-t-il été produit ? |
| Signalement | L'absence d'information est-elle explicitement dite ? |
| Citation | Le passage source est-il cité ? |
| Déduction | Est-elle faite, et si oui signalée comme telle ? |
| Prudence excessive | Un refus de répondre alors que l'information est disponible ? |

---

## 5. Ce que la partie cherche à établir

L'hypothèse principale est que **le prompt B est le plus risqué des trois**. Le prompt A produit une réponse manifestement non fondée — le défaut est visible. Le prompt C est contraint. Mais le prompt B fournit un contexte *sans* règle d'usage : le modèle peut alors mélanger librement ce qu'il lit et ce qu'il sait, sans qu'aucune frontière ne soit visible dans la réponse.

C'est exactement le mécanisme observé en [Partie 3](../03-raisonnement/resultats.md), où le prompt vague produisait une vingtaine de recommandations dont la plupart venaient du savoir général du modèle et non des avis fournis.

---

## Prompts testés

Voir [`prompts.md`](prompts.md).

## Résultats et analyse

Voir [`resultats.md`](resultats.md).

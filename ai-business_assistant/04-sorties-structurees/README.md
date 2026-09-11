# Partie 4 — Sorties structurées

> **Énoncé.** Le LLM retourne : « Le commentaire semble plutôt négatif. Le client est mécontent du délai de livraison... »
>
> 1) Pour rendre cette réponse plus facile à exploiter par une application, créer un prompt demandant du JSON avec les champs `sentiment`, `categorie`, `urgence`, `probleme`, `confiance`. Préciser les types des valeurs et les valeurs autorisées.
> 2) Ajouter une validation en définissant les règles de sortie suivantes : format JSON valide ; aucune propriété supplémentaire ; `sentiment` vaut positif, negatif ou neutre ; `confiance` est compris entre 0 et 1 ; `urgence` vaut faible, moyenne ou élevée.

---

## 1. Le problème de la réponse en prose

> « Le commentaire semble plutôt négatif. Le client est mécontent du délai de livraison... »

Cette phrase est parfaitement claire **pour un humain**. Elle est inutilisable **pour une application**. Quatre raisons :

| Problème | Détail |
|---|---|
| **Pas de champ identifiable** | Aucun moyen d'extraire « négatif » autrement que par une analyse du texte — soit un second appel LLM, soit une regex fragile |
| **Modalisation** | « semble **plutôt** négatif » : est-ce négatif ou non ? Aucun seuil, aucune valeur numérique |
| **Vocabulaire libre** | « mécontent du délai de livraison » — la catégorie est-elle `livraison`, `délai`, `logistique` ? Deux exécutions donneront deux formulations |
| **Non agrégeable** | Impossible de compter, filtrer ou trier 10 000 réponses de cette forme |

La sortie structurée résout ces quatre points d'un coup : **elle transforme une opinion formulée en données manipulables.**

---

## 2. Ce que « préciser les types et les valeurs autorisées » implique

L'énoncé demande deux choses distinctes, souvent confondues :

**Le type** — la nature de la valeur : chaîne de caractères, nombre, booléen. Il détermine ce que le code recevra.

**Le domaine** — l'ensemble des valeurs acceptables pour ce type. Une chaîne peut valoir n'importe quoi ; une chaîne *énumérée* ne peut valoir que ce qu'on a listé.

| Champ | Type | Domaine | Sans domaine fermé, on obtiendrait… |
|---|---|---|---|
| `sentiment` | string | `positif` \| `negatif` \| `neutre` | « plutôt négatif », « mitigé », « négatif à 70% » |
| `categorie` | string | `livraison` \| `application` \| `prix` \| `sav` \| `produit` \| `autre` | « délai », « logistique », « retard de livraison » |
| `urgence` | string | `faible` \| `moyenne` \| `elevee` | « urgent », « à traiter vite », « priorité 1 » |
| `probleme` | string | texte libre, une phrase | *(champ volontairement libre)* |
| `confiance` | number | 0.0 à 1.0 | « élevée », « 91% », « forte » |

**Le champ `probleme` est délibérément laissé libre** : c'est le seul qui porte l'information non catégorisable. Un schéma entièrement fermé perdrait la spécificité de chaque avis ; un schéma entièrement ouvert serait inexploitable. Le bon équilibre garde un champ libre pour le contexte et ferme tout ce qui sert au filtrage.

---

## 3. La différence entre demander et valider

C'est le cœur de la partie, et la raison pour laquelle l'énoncé sépare les deux questions.

**Question 1 — demander le format.** On décrit la structure attendue et on espère que le modèle s'y conforme. C'est de la **persuasion** : rien ne garantit le résultat.

**Question 2 — ajouter les règles de validation.** On énonce des règles vérifiables mécaniquement, ce qui permet de **rejeter** une sortie non conforme plutôt que de la consommer à l'aveugle.

La distinction est fondamentale en production :

| | Prompt seul (Q1) | Prompt + règles (Q2) |
|---|---|---|
| Nature | Instruction | Contrat |
| Vérifiable par | Lecture humaine | Code / JSON Schema |
| Échec | Silencieux | Détecté |

**Un point important :** même parfaitement formulées dans le prompt, ces règles restent **déclaratives**. Un LLM peut toujours produire une sortie non conforme. La validation réelle se fait **côté application**, par un validateur de schéma. Les règles dans le prompt réduisent la fréquence des écarts ; elles ne les éliminent pas.

C'est pourquoi cette partie produit aussi un **JSON Schema** exécutable, dans [`schema.json`](schema.json) — la version machine des règles de l'énoncé.

---

## 4. Ce qu'on cherche à observer

| Critère | Question |
|---|---|
| JSON valide | Parsable sans nettoyage préalable ? |
| Texte parasite | Du commentaire avant ou après le JSON ? |
| Champs exacts | Les 5 champs, ni plus ni moins ? |
| Domaines respectés | Les énumérations sont-elles tenues ? |
| Type de `confiance` | Nombre, ou chaîne « 0.91 » ? |
| Cas ambigu | Comment le modèle gère-t-il un avis mixte ? |
| Effet des règles | Q2 change-t-il quelque chose par rapport à Q1 ? |

Le **cas ambigu** est testé volontairement : l'avis A03 (« service rapide mais application plante ») ne rentre dans aucune des trois valeurs de `sentiment`. La Partie 2 a montré que le modèle tranche en `negatif`. Ici, le champ `confiance` devrait *refléter* cette ambiguïté par une valeur plus basse — c'est sa fonction.

---

## Prompts testés

Voir [`prompts.md`](prompts.md).

## Résultats et analyse

Voir [`resultats.md`](resultats.md).

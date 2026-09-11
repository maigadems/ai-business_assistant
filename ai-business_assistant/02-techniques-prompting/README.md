# Partie 2 — Comparer les techniques de prompting

> **Énoncé.** Tester puis évaluer les résultats obtenus avec les techniques zero-shot, one-shot, few-shot et un prompt structuré sur une demande du genre :
>
> « Classer le commentaire suivant :
> *"Le service est rapide mais l'application plante régulièrement."*
> Classes possibles : positif, négatif, neutre. »

---

## 1. Pourquoi ce cas est bien choisi

Le commentaire de l'énoncé est l'avis **A03** du jeu de données de la Partie 1. Ce n'est pas un hasard : c'est un cas **volontairement ambigu**.

> « Le service est **rapide** mais l'application **plante régulièrement**. »

Il contient une appréciation positive (la rapidité du service) et une appréciation négative (l'instabilité de l'application), dans la même phrase, reliées par un « mais » qui donne le poids à la seconde.

Or les classes autorisées sont **positif, négatif, neutre** — aucune ne décrit correctement ce commentaire :

| Classe | Pourquoi elle ne convient pas |
|---|---|
| positif | Ignore le défaut, qui est le point saillant |
| négatif | Ignore le compliment sur le service |
| neutre | Faux : le commentaire exprime deux opinions marquées, pas une absence d'opinion |

**C'est tout l'intérêt du test.** La question n'est pas « le modèle trouve-t-il la bonne réponse » — il n'y en a pas. La question est : **comment chaque technique se comporte-t-elle face à un cas que la consigne ne permet pas de traiter correctement ?**

C'est exactement la situation qu'on rencontre en production, où les taxonomies sont toujours plus pauvres que la réalité.

---

## 2. Les quatre techniques comparées

| Technique | Principe | Coût en tokens |
|---|---|---|
| **Zero-shot** | La consigne seule, aucun exemple | Minimal |
| **One-shot** | La consigne + 1 exemple résolu | Faible |
| **Few-shot** | La consigne + plusieurs exemples résolus | Moyen à élevé |
| **Prompt structuré** | Consigne décomposée en sections explicites, avec règles de décision | Moyen |

La différence essentielle : **few-shot enseigne par l'exemple**, le **prompt structuré enseigne par la règle**. Les deux visent le même objectif — lever l'ambiguïté — mais par des moyens opposés.

---

## 3. Ce qu'on cherche à observer

Grille appliquée aux quatre techniques :

| Critère | Question |
|---|---|
| Classe choisie | Quelle classe le modèle retient-il ? |
| Stabilité | Le choix varie-t-il d'une exécution à l'autre ? |
| Justification | Le modèle explique-t-il son choix ? |
| Format | La sortie est-elle directement exploitable ? |
| Verbosité | Combien de texte pour une seule étiquette ? |
| Gestion de l'ambiguïté | Le modèle signale-t-il que le cas est mixte ? |
| Respect de la taxonomie | Reste-t-il dans les 3 classes autorisées ? |

Le dernier critère est le plus révélateur : **un modèle qui invente « mitigé » a raison sur le fond mais tort sur la consigne.** C'est un arbitrage qu'un prompt de production doit trancher explicitement.

---

## 4. Lien avec la Partie 1

La Partie 1 a montré, en V4, que l'exemple few-shot ne transmet pas seulement un format : il transmet aussi une **granularité de regroupement** non voulue. La Partie 2 prolonge directement cette observation en isolant l'effet du nombre d'exemples.

---

## 5. Prompts testés

Voir [`prompts.md`](prompts.md).

## 6. Résultats et analyse

Voir [`resultats.md`](resultats.md).

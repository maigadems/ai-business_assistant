# Partie 3 — Prompt Engineering et raisonnement

> **Énoncé.**
> 1) Décomposer le prompt suivant : « Analyse ces avis clients et donne-moi les problèmes les plus importants ainsi que les recommandations. »
> 2) Proposer au modèle un texte à analyser avec des contraintes puis utiliser un second prompt lui demandant de vérifier sa réponse précédente et de contrôler les informations non justifiées, les contradictions, les informations absentes, les éventuelles hallucinations et le respect des contraintes.

---

## Exercice 1 — Décomposition d'un prompt vague

### Le problème du prompt de départ

> « Analyse ces avis clients et donne-moi les problèmes les plus importants ainsi que les recommandations. »

Ce prompt est **meilleur que l'intention brute de la Partie 1** : il nomme une tâche (analyser), un objet (les avis) et deux livrables (problèmes, recommandations). Mais il repose sur un mot non défini qui porte toute la difficulté : **« les plus importants »**.

Important selon quel critère ?

| Critère possible | Classement produit sur notre jeu d'avis |
|---|---|
| **Fréquence** | Livraison (3 avis) > Application (2) > Prix (1) |
| **Gravité** | Application (bloque le paiement) > Livraison > Prix |
| **Coût de correction** | Prix (décision tarifaire) > Application (dev) > Livraison |
| **Réversibilité** | Livraison (client perdu) > Application > Prix |

Ces quatre critères donnent **quatre classements différents**. Le modèle en choisira un — probablement la fréquence, la plus facile à calculer — sans le dire, et sans que rien ne signale qu'un arbitrage a eu lieu.

C'est le même mécanisme que le cas mixte de la Partie 2 : **une décision est prise silencieusement à la place de l'utilisateur.**

### Trois implicites supplémentaires

Au-delà de « important », le prompt laisse ouvert :

- **Le lien problèmes → recommandations.** Une recommandation par problème ? Une recommandation globale ? Des recommandations qui peuvent dépasser les problèmes identifiés ?
- **Le fondement des recommandations.** Doivent-elles se limiter aux avis fournis, ou le modèle peut-il mobiliser ses connaissances générales en e-commerce ? C'est la porte d'entrée principale des hallucinations : une recommandation plausible mais sans ancrage dans les données.
- **Le niveau d'agrégation.** Un problème = un avis, ou un problème = un thème regroupant plusieurs avis ?

### Méthode de décomposition

Décomposer ne consiste pas à allonger le prompt, mais à le **découper en sous-tâches ordonnées**, chacune produisant un résultat vérifiable qui alimente la suivante :

```
1. Extraire  → un problème par avis, avec l'identifiant de l'avis
2. Regrouper → thèmes, à partir des problèmes extraits
3. Mesurer   → fréquence et gravité de chaque thème, séparément
4. Classer   → priorité explicite, selon une règle énoncée
5. Recommander → une action par thème prioritaire, ancrée dans les avis
```

Chaque étape est **auditable** : on peut vérifier l'étape 1 sans lire l'étape 5. Un prompt monolithique ne permet pas cela — on ne voit que le résultat final, et on ne sait pas où une erreur s'est introduite.

C'est le principe du **chain-of-thought structuré** : ce n'est pas « réfléchis étape par étape » ajouté à la fin d'un prompt, c'est la tâche elle-même qui est découpée.

---

## Exercice 2 — Auto-vérification (self-check)

### Principe

Un second prompt demande au modèle d'**auditer sa propre réponse précédente** selon cinq critères imposés par l'énoncé :

| Critère | Question posée |
|---|---|
| Informations non justifiées | Quelles affirmations ne s'appuient sur aucun avis fourni ? |
| Contradictions | La réponse se contredit-elle, ou contredit-elle les avis ? |
| Informations absentes | Qu'est-ce qui figurait dans les avis et a été omis ? |
| Hallucinations | Des faits, chiffres ou citations ont-ils été inventés ? |
| Respect des contraintes | Chaque contrainte du premier prompt a-t-elle été tenue ? |

### Ce qu'on cherche à établir

L'auto-vérification est une technique répandue, mais sa valeur réelle est discutée. Deux résultats sont possibles, et **les deux sont intéressants** :

- **Le modèle trouve de vraies erreurs** → la technique a une valeur opérationnelle, à condition de l'outiller.
- **Le modèle valide sa propre réponse** (biais de complaisance) → la technique donne une fausse assurance, ce qui est pire que pas de vérification du tout.

Le protocole est conçu pour distinguer les deux : le premier prompt contient des **contraintes précises et vérifiables**, dont certaines que le modèle a de bonnes chances d'enfreindre. On saura donc si l'audit est sincère.

---

## Prompts testés

Voir [`prompts.md`](prompts.md).

## Résultats et analyse

Voir [`resultats.md`](resultats.md).

# Partie 7 — Les trois prompts RAG

**Protocole :** une conversation neuve par prompt **et par question**, soit 9 exécutions au total (3 prompts × 3 questions).

**Document :** [`rapport-trimestriel.md`](../data/rapport-trimestriel.md), collé intégralement à la place de `{document}`.

---

## Les trois questions testées

| # | Question | Statut dans le document |
|---|---|---|
| **Q1** | Quel est le délai moyen de première réponse constaté sur le trimestre, et l'objectif était-il atteint ? | ✅ **Présente** — 7 h 20, objectif de 6 h non atteint |
| **Q2** | Quel est le taux de satisfaction global du service client sur le trimestre ? | ❌ **Absente** — seules les satisfactions par canal figurent |
| **Q3** | Combien de conseillers l'équipe compte-t-elle à la fin du trimestre ? | ⚠️ **Déductible** — 18 en début + 2 recrutements, jamais écrit |

---

## Prompt A — Sans document

*La question seule. Le modèle n'a aucune information sur ce rapport.*

```text
{question}
```

Soit, pour chacune des trois questions :

```text
Quel est le délai moyen de première réponse constaté sur le trimestre, et l'objectif était-il atteint ?
```

```text
Quel est le taux de satisfaction global du service client sur le trimestre ?
```

```text
Combien de conseillers l'équipe compte-t-elle à la fin du trimestre ?
```

**Hypothèse.** Le document étant **fictif**, aucune réponse correcte n'est possible. Deux comportements attendus :

- le modèle demande de quel rapport il s'agit → comportement prudent ;
- le modèle produit une réponse générique ou inventée → hallucination manifeste.

Ce prompt sert de **référence de départ** : il établit ce que le contexte apporte réellement.

---

## Prompt B — Avec document, sans contraintes

*Le document est fourni, mais aucune règle n'encadre son usage.*

```text
Voici un document.

{document}

{question}
```

**Hypothèse.** C'est **le prompt le plus risqué des trois**, et l'enjeu principal de cette partie.

Sur Q1, il devrait réussir : l'information est explicite.

Sur **Q2**, rien n'oblige le modèle à signaler l'absence. Il peut :
- calculer une moyenne des trois canaux (4,3 + 3,8 + 3,6) / 3 ≈ 3,9 — déduction non autorisée, car les canaux n'ont pas le même volume ;
- produire un chiffre plausible sans le sourcer ;
- signaler spontanément l'absence.

Sur **Q3**, il devrait déduire 20 sans nécessairement signaler qu'il s'agit d'une déduction.

**Le risque n'est pas l'erreur, c'est l'indiscernabilité** : sans règle, rien dans la réponse ne distingue ce qui est lu de ce qui est déduit ou su.

---

## Prompt C — Avec document et contraintes de groundedness

*Les trois contraintes imposées par l'énoncé.*

```text
Tu réponds à des questions portant sur un document interne.

Contraintes :
- utilise uniquement les informations présentes dans le document fourni ; n'utilise aucune connaissance extérieure
- n'invente aucune information absente du document
- si l'information demandée ne figure pas dans le document, écris explicitement "Information non présente dans le document" et n'essaie pas de la reconstituer
- si tu effectues une déduction à partir de plusieurs éléments du document, signale-le explicitement et détaille le raisonnement
- cite le passage exact du document sur lequel tu t'appuies, entre guillemets

Document :
<<<
{document}
>>>

Question : {question}
```

**Hypothèse.** Les contraintes devraient produire trois effets distincts :

| Question | Effet attendu |
|---|---|
| Q1 | Réponse identique à B, **plus la citation** du passage |
| Q2 | **« Information non présente dans le document »** — c'est le test central |
| Q3 | Déduction 18 + 2 = 20 **signalée comme déduction**, ou refus si lecture stricte |

Sur Q3, deux réponses sont acceptables. La contrainte « si tu effectues une déduction, signale-le » a été ajoutée précisément pour éviter le sur-ajustement observé en [Partie 5.4](../05-applications-metier/resultats.md#54--extraction-de-données-de-facture), où le modèle avait retourné `null` sur des montants pourtant déductibles.

**Ce qu'on cherche à voir :** une contrainte anti-hallucination bien bornée doit interdire l'invention **sans** interdire le raisonnement.

---

## Grille d'observation

À remplir pour les 9 exécutions.

### Q1 — Information présente

| Critère | A (sans doc) | B (doc seul) | C (doc + contraintes) |
|---|---|---|---|
| Réponse exacte (7 h 20) | | | |
| Objectif non atteint signalé | | | |
| Piège septembre évité | | | |
| Passage cité | | | |

### Q2 — Information absente

| Critère | A | B | C |
|---|---|---|---|
| Absence signalée | | | |
| Chiffre inventé | | | |
| Moyenne calculée sans mandat | | | |

### Q3 — Information déductible

| Critère | A | B | C |
|---|---|---|---|
| Réponse 20 | | | |
| Déduction signalée | | | |
| Refus excessif | | | |

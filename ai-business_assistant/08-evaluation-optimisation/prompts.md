# Partie 8 — Les trois versions de prompt

**Protocole :** **6 exécutions** — 3 prompts × 2 répétitions, conversation neuve à chaque fois.

La double exécution mesure la **stabilité**, critère qu'aucune partie précédente n'a pu évaluer.

**Document :** [`rapport-trimestriel.md`](../data/rapport-trimestriel.md), collé intégralement à la place de `{document}`.

---

## Prompt A — Minimal

*L'énoncé, tel quel.*

```text
Résume ce texte.

{document}
```

**Composants présents :** tâche uniquement.

**Hypothèse.** Aucune contrainte de longueur, de structure ni de fidélité. Le modèle décide de tout : format, longueur, ce qu'il retient, ce qu'il écarte. Le résumé devrait être long et suivre l'ordre du document plutôt que hiérarchiser.

---

## Prompt B — Contrainte de longueur

*L'énoncé, tel quel.*

```text
Résume ce texte en 150 mots.

{document}
```

**Composants présents :** tâche + une contrainte de format.

**Hypothèse.** La contrainte force une sélection. Trois choses peuvent être sacrifiées, et l'intérêt est de voir lesquelles :

| Ce qui peut sauter | Conséquence |
|---|---|
| Les chiffres | Le résumé devient qualitatif, inexploitable pour décider |
| La mention des objectifs manqués | Le résumé devient complaisant |
| Les recommandations | Le résumé devient un constat sans suite |

---

## Prompt C — Prompt complet

*Réinvestit les composants et les acquis des sept parties précédentes.*

```text
Tu es analyste chargé de produire des synthèses de documents internes pour un comité de direction.

Tâche : résumer le document fourni.

Structure imposée, sous quatre intertitres dans cet ordre :
- **Objectifs** : les cibles annoncées, et pour chacune si elle est atteinte ou non
- **Résultats** : ce qui a été obtenu, avec les chiffres clés
- **Difficultés** : les obstacles rencontrés et leur effet sur les résultats
- **Recommandations** : ce que le document préconise, avec les montants s'ils figurent

Contraintes :
- 150 mots maximum, intertitres inclus
- conserve les chiffres, dates, taux et montants ; ne les arrondis pas
- n'utilise que le document fourni ; n'ajoute aucune information, aucune cause ni aucune recommandation extérieure
- si un objectif n'est pas atteint, écris-le explicitement ; ne présente pas un résultat partiel comme un succès
- distingue les résultats du trimestre des résultats d'un mois isolé ; ne présente jamais une performance mensuelle comme le résultat trimestriel
- si une information demandée par un intertitre est absente du document, écris "non précisé dans le document" sous cet intertitre

Ton : factuel et neutre, sans formule d'introduction ni de conclusion.

Document à résumer :
<<<
{document}
>>>
```

### Ce que chaque contrainte réinvestit

| Contrainte | Origine | Problème observé qu'elle corrige |
|---|---|---|
| Quatre intertitres dont **Difficultés** | [P5.1](../05-applications-metier/resultats.md#51--résumé-de-document) | Trois intertitres avaient fait disparaître toute la section 4 du document |
| « écris-le explicitement » (objectifs manqués) | [P5.1](../05-applications-metier/resultats.md#51--résumé-de-document) | Contrainte anti-complaisance, qui avait fonctionné |
| « distingue trimestre et mois isolé » | [P5.1](../05-applications-metier/resultats.md#51--résumé-de-document) | Le piège septembre — 4 h 15 atteint, 7 h 20 non atteint |
| « n'ajoute aucune cause » | [P3](../03-raisonnement/resultats.md) | Une vingtaine de recommandations hors-sol sur prompt vague |
| « non précisé dans le document » | [P3](../03-raisonnement/resultats.md), [P5.4](../05-applications-metier/resultats.md), [P7](../07-rag/resultats.md) | **Formule à produire** plutôt qu'interdiction — quatrième réemploi |
| « ne les arrondis pas » | [P6](../06-machine-learning/resultats.md) | Une valeur numérique fausse dans une réponse par ailleurs juste |
| « sans formule d'introduction » | [P5.5](../05-applications-metier/resultats.md) | Verbiage consommant le budget de mots |

**Hypothèse.** C devrait dominer sur les critères mesurables. Le risque résiduel est le **conflit entre contraintes** : 150 mots pour quatre rubriques dont une liste d'objectifs avec statut, c'est serré. La [Partie 1](../01-anatomie-prompt/resultats.md) a montré que des contraintes juxtaposées sans hiérarchie produisent un arbitrage silencieux.

---

## Plan des exécutions

| Fichier capture | Prompt | Exécution |
|---|---|---|
| `01-A-exec1.png` | A | 1 |
| `02-A-exec2.png` | A | 2 |
| `03-B-exec1.png` | B | 1 |
| `04-B-exec2.png` | B | 2 |
| `05-C-exec1.png` | C | 1 |
| `06-C-exec2.png` | C | 2 |

---

## Grille d'observation

Critères définis dans le [README](README.md#2-la-grille-dévaluation). Les critères 1 à 4 sont calculés par [`mesurer.py`](mesurer.py).

| Critère | A1 | A2 | B1 | B2 | C1 | C2 |
|---|---|---|---|---|---|---|
| 1. Longueur (mots) | | | | | | |
| 2. Compression | | | | | | |
| 3. Couverture chiffres /8 | | | | | | |
| 4. Exactitude numérique | | | | | | |
| 5. Stabilité inter-exécutions | | | | | | |
| 6. Fidélité | | | | | | |
| 7. Objectifs manqués signalés | | | | | | |
| 8. Piège septembre évité | | | | | | |
| 9. Aucun ajout externe | | | | | | |
| 10. Exploitabilité | | | | | | |
| 11. Hiérarchisation | | | | | | |

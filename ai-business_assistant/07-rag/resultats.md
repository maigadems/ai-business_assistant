# Partie 7 — Résultats obtenus et analyse

**LLM utilisé :** ChatGPT (OpenAI)
**Date d'exécution :** 12 septembre 2025
**Protocole :** 9 exécutions — 3 prompts × 3 questions, conversation neuve à chaque fois.

---

## Prompt A — Sans document

**Prompt :** voir [`prompts.md`](prompts.md#prompt-a--sans-document)

### A/Q1 — Information présente dans le document

![Prompt A, question 1](captures/01-A-q1.png)

> « Je peux expliquer comment le calculer, mais **je n'ai pas les données du trimestre ni la cible fixée** dans le contexte disponible. »

Le modèle définit ensuite la notion de délai de première réponse, expose la règle de comparaison (délai ≤ objectif → atteint), et conclut :

> « Si tu me fournis le tableau ou le rapport du trimestre [...] je peux te donner directement la valeur moyenne et le verdict. »

### A/Q2 — Information absente du document

![Prompt A, question 2](captures/02-A-q2.png)

> « Je ne peux pas déterminer le taux de satisfaction global du service client sur le trimestre **sans les données de satisfaction du trimestre**. »

Il fournit la formule du CSAT et un exemple **explicitement étiqueté comme tel** :

> « **Par exemple**, si 840 clients sur 1 000 se déclarent satisfaits : CSAT = 840 / 1 000 × 100 = 84 %. »

### A/Q3 — Information déductible

![Prompt A, question 3](captures/03-A-q3.png)

> « Je n'ai pas les données du trimestre permettant de déterminer le nombre de conseillers à sa fin. Si tu me fournis le tableau ou le rapport concerné, je peux l'identifier directement. »

Réponse minimale, sans développement.

**Observations :**

| Critère | Q1 | Q2 | Q3 |
|---|---|---|---|
| Chiffre inventé | ✅ aucun | ✅ aucun | ✅ aucun |
| Absence de contexte signalée | ✅ | ✅ | ✅ |
| Réponse fabriquée | ❌ non | ❌ non | ❌ non |
| Longueur | moyenne | moyenne | minimale |

### L'hypothèse est infirmée : aucune hallucination

Le cadrage anticipait deux comportements possibles, dont l'un était l'hallucination. **Le modèle a systématiquement refusé de répondre**, sur les trois questions, sans produire le moindre chiffre présenté comme factuel.

C'est un résultat plus favorable qu'attendu, et cohérent avec ce qu'avait montré la [Partie 1](../01-anatomie-prompt/resultats.md) : face au prompt nu « Analyse les retours clients », le modèle avait également refusé et réclamé les données plutôt que d'inventer des avis.

**Deux comportements de sécurité sont observables :**

1. **La demande de contexte est systématique.** Les trois réponses se terminent par une variante de « fournis-moi le document ».
2. **Le seul chiffre produit est explicitement étiqueté comme exemple.** Dans A/Q2, « 840 clients sur 1 000 → 84 % » est introduit par « **Par exemple** ». Aucun risque de confusion avec une donnée du rapport.

### Ce que le modèle produit à la place : de la méthode

N'ayant pas les données, le modèle répond sur **comment** obtenir la réponse plutôt que sur la réponse :

| Question | Contenu substitué |
|---|---|
| Q1 | Définition du délai de première réponse + règle de comparaison à l'objectif |
| Q2 | Formule du CSAT + exemple de calcul |
| Q3 | Rien — refus sec |

Ce comportement est le même que celui observé en Partie 1 (V0), où le modèle avait produit un plan méthodologique en 9 axes au lieu d'une analyse. **Le modèle sait quoi faire, il ignore avec quoi.**

L'asymétrie entre Q3 et les deux autres est notable : Q1 et Q2 portent sur des indicateurs standardisés (délai de réponse, CSAT) sur lesquels le modèle a du contenu générique à offrir. Q3 porte sur un effectif — il n'existe aucune méthode générale pour compter les conseillers d'une équipe inconnue, donc rien à dire.

### La valeur de référence de ce prompt

Le prompt A remplit sa fonction : il établit la **ligne de base**. Sur les trois questions, le modèle ne sait rien — ce qui était attendu puisque le document est fictif.

Toute information correcte apparaissant dans les prompts B et C provient donc **nécessairement du contexte fourni**, et non de connaissances préalables. C'est cette garantie qui rend la comparaison interprétable.

**Point de vigilance pour la suite :** ce refus systématique en l'absence de contexte ne dit rien du comportement **en présence** d'un contexte partiel. C'est précisément le cas de Q2, où le document contient des données de satisfaction *par canal* mais pas de taux global — situation bien plus ambiguë qu'une absence totale d'information.

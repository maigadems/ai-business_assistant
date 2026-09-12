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

---

## Prompt B — Avec document, sans contraintes

**Prompt :** voir [`prompts.md`](prompts.md#prompt-b--avec-document-sans-contraintes)

### B/Q1 — Information présente

![Prompt B, question 1](captures/04-B-q1.png)

> « Le délai moyen de première réponse sur le troisième trimestre 2025 était de **7 h 20**.
>
> L'objectif était de le réduire à **moins de 6 heures**. **Il n'a donc pas été atteint sur l'ensemble du trimestre**, même si septembre a atteint l'objectif avec un délai de **4 h 15**. »

**Le piège est évité.** La formulation distingue explicitement le trimestre (non atteint) du mois de septembre (atteint), dans le bon ordre : le constat d'ensemble d'abord, la nuance mensuelle ensuite, subordonnée par « même si ».

C'est exactement la structure obtenue en [Partie 5.1](../05-applications-metier/resultats.md#51--résumé-de-document) pour le résumé — mais **sans aucune contrainte anti-complaisance cette fois**. Le prompt B ne dit rien d'autre que « voici un document, voici une question ».

### B/Q2 — Information absente ⭐

![Prompt B, question 2](captures/05-B-q2.png)

> « Le document **ne donne pas de taux de satisfaction global** pour l'ensemble du service client sur le trimestre.
>
> Il fournit uniquement les taux de satisfaction par canal pour les trois premières semaines du chat :
> - Chat : 4,3/5
> - Téléphone : 3,8/5
> - E-mail : 3,6/5
>
> Donc, **le taux de satisfaction global ne peut pas être calculé avec les données fournies**. »

**C'est le résultat le plus important de la partie, et il infirme l'hypothèse centrale.**

Le modèle a :

| Comportement | Verdict |
|---|---|
| Signalé l'absence explicitement | ✅ sans qu'aucune contrainte ne le demande |
| Refusé de calculer la moyenne (4,3+3,8+3,6)/3 ≈ 3,9 | ✅ le piège principal est évité |
| Cité les données réellement présentes | ✅ initiative non demandée |
| Précisé la portée temporelle des chiffres | ✅ « trois premières semaines du chat » |

Cette dernière précision est particulièrement fine. Le document dit que le chat a été déployé le 9 septembre et que les satisfactions portent sur « les trois premières semaines d'exploitation ». Le modèle a compris que ces chiffres **ne couvrent pas le trimestre** — ce qui est une seconde raison, indépendante de l'absence de taux global, pour laquelle la question ne peut pas recevoir de réponse.

### B/Q3 — Information déductible

![Prompt B, question 3](captures/06-B-q3.png)

> « À la fin du trimestre, l'équipe compte **20 conseillers**.
> - 18 conseillers au début du trimestre
> - 2 recrutements réalisés (12 août et 3 septembre)
> - **Total : 20 conseillers** »

La déduction est correcte, et **le raisonnement est exposé** sans que le prompt l'ait demandé. Les deux prémisses sont citées avec leurs dates, puis le total.

Le chiffre 20 n'apparaît nulle part dans le document — c'est bien une construction, et elle est traçable.

**Observations :**

| Critère | Q1 | Q2 | Q3 |
|---|---|---|---|
| Réponse exacte | ✅ 7 h 20 | ✅ absence signalée | ✅ 20 |
| Chiffre inventé | ✅ aucun | ✅ aucun | ✅ aucun |
| Piège évité | ✅ septembre distingué | ✅ moyenne non calculée | n/a |
| Raisonnement exposé | n/a | ✅ données citées | ✅ prémisses détaillées |
| Passage cité littéralement | ❌ non | ⚠️ valeurs, pas le texte | ⚠️ valeurs, pas le texte |

### L'hypothèse centrale de la partie est infirmée

Le [cadrage](README.md#5-ce-que-la-partie-cherche-à-établir) posait que « le prompt B est le plus risqué des trois », par analogie avec la Partie 3 où un prompt vague avait produit des recommandations indiscernables entre lecture et savoir général.

**Ce risque ne s'est pas matérialisé.** Sur les trois questions, le modèle s'est comporté comme si les contraintes de groundedness étaient présentes : il a signalé l'absence, refusé une déduction invalide, et exposé le raisonnement d'une déduction valide.

Trois explications possibles, non exclusives :

1. **La question porte sur un document explicitement fourni.** La formulation « Voici un document [...] Quel est... » ancre implicitement la réponse dans ce document. Le contexte n'est pas seulement disponible, il est désigné comme la source.

2. **Le document est bien structuré.** Les informations sont présentées sous forme de sections titrées avec des chiffres isolés. L'absence d'un taux global est repérable parce que la structure rend visible ce qui est là — et donc ce qui n'y est pas.

3. **Les modèles récents intègrent des comportements de fidélité au contexte.** C'est cohérent avec le refus systématique observé au prompt A : ce même comportement prudent, appliqué à un contexte fourni, produit de la fidélité.

### La différence qui subsiste : la traçabilité

Les réponses de B sont **correctes**, mais elles ne sont pas **vérifiables sans relire le document**.

| Ce que B produit | Ce qui manque |
|---|---|
| « 7 h 20 » | Le passage exact d'où vient ce chiffre |
| « ne donne pas de taux global » | La liste de ce que le document contient effectivement sur ce point — donnée ici, mais par initiative |
| « Total : 20 conseillers » | La mention explicite qu'il s'agit d'une déduction et non d'une lecture |

Sur Q3 en particulier : le raisonnement est exposé, mais **rien ne dit que 20 n'est pas écrit dans le document**. Un lecteur pressé retiendra « le document indique 20 conseillers », ce qui est faux.

**C'est la vraie différence attendue avec le prompt C** : non pas l'exactitude, mais la capacité à distinguer, dans la réponse elle-même, ce qui est cité de ce qui est construit.

**Ce que cela change pour la suite :** le prompt C ne pourra pas se juger sur l'exactitude — B a déjà les trois bonnes réponses. Il devra se juger sur la **traçabilité** : citations littérales, signalement explicite des déductions, formule normalisée pour l'absence d'information.

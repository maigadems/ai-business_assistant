# Partie 1 — Résultats obtenus et analyse

**LLM utilisé :** ChatGPT (OpenAI)
**Date d'exécution :** 12 septembre 2025
**Protocole :** une conversation neuve par version, avis de [`data/avis-clients.md`](../data/avis-clients.md) collés à la place de `{avis}`.

---

## V0 — Intention brute

**Prompt :** voir [`prompts.md`](prompts.md#v0--intention-brute)

![Résultat V0 — prompt nu](captures/01-v0-prompt-nu.png)

**Observations :**

Le modèle **refuse d'analyser** et réclame les données : « Pour analyser réellement les retours clients, il me faut les données ». Il ne produit aucune analyse, mais propose en revanche un **plan méthodologique en 9 axes** (sentiment, thématiques, points forts, irritants, fréquence, priorisation, évolution, verbatims, recommandations), puis conclut par « Envoie-moi le fichier ou les retours clients ».

Fait notable : la réponse contient une **citation de source externe** (`easiware.com`), signe que le modèle a comblé le vide de la consigne en puisant dans ses connaissances générales sur l'analyse de verbatims.

**Ce que cette version révèle :**

Sans **données** ni **tâche** précise, le modèle ne peut que deviner l'intention. Ici il a choisi la stratégie la plus prudente — demander des précisions — mais rien ne garantit ce comportement : selon le modèle ou la formulation, il aurait tout aussi bien pu **inventer des avis fictifs** et les analyser, produisant un résultat plausible et entièrement faux.

Le plan en 9 axes qu'il propose est d'ailleurs instructif : il montre que le modèle *sait* quoi faire, mais qu'il ignore lequel de ces 9 axes on attend de lui. C'est exactement la décision que la composante **Tâche** doit lui retirer.

Cette version sert de **référence de départ** : tout ce que les versions suivantes ajoutent se mesure par rapport à cette réponse vide.

---

## V1 — Ajout de la Tâche

**Prompt :** voir [`prompts.md`](prompts.md#v1--ajout-de-la-tâche)

![Résultat V1 — tâche explicite](captures/02-v1-tache.png)

**Observations :**

Le modèle **analyse réellement** cette fois. Il annonce « une analyse structurée des 10 avis » et produit spontanément un tableau à 4 colonnes (Thème, Avis concernés, Sentiment dominant, Analyse), sous un titre numéroté « 1. Thèmes principaux et sentiment associé » — ce qui laisse supposer d'autres sections en dessous.

Les deux premières lignes sont correctes au regard de la répartition de référence :

| Thème produit | Avis | Sentiment | Conforme à la référence ? |
|---|---|---|---|
| Livraison / délais | A01, A07, A08 | « Mitigé → négatif » | ✅ oui, les 3 avis |
| Support client / réactivité | A01, A05 | « Mitigé » | ✅ oui |

Le modèle gère correctement le **rattachement multiple** (A01 apparaît dans deux thèmes) et justifie chaque sentiment en citant les avis concernés.

Deux libertés qu'il prend, faute de consigne : il ajoute des **émojis** décoratifs (🚚, 💬) devant les noms de thèmes, et il invente une notation personnelle « Mitigé → négatif » qui ne fait partie d'aucune échelle demandée.

**Ce que l'ajout a corrigé :**

L'ajout de la **Tâche** et des **Données** fait passer d'une réponse vide à une analyse exploitable. C'est le saut le plus important de toute la série — à lui seul, il rend le prompt utile.

Ce qui reste non maîtrisé, en revanche, ce sont **toutes les décisions de forme** : le nombre de colonnes, le nombre de thèmes, la présence d'émojis, l'échelle de sentiment, le nombre de sections. Le modèle a choisi une structure raisonnable, mais c'est *lui* qui l'a choisie. Rien ne garantit qu'une seconde exécution produise la même — c'est précisément ce que teste la section Stabilité.

La notation « Mitigé → négatif » illustre bien le problème : elle est intelligente, mais **non agrégeable**. Une application qui consommerait cette sortie ne saurait pas quoi en faire.

---

## V2 — Ajout du Rôle et du Contexte

**Prompt :** voir [`prompts.md`](prompts.md#v2--ajout-du-rôle-et-du-contexte)

![Résultat V2 — rôle et contexte](captures/03-v2-role-contexte.png)

**Observations :**

Le changement est visible dès la première phrase : « Voici une analyse orientée **priorisation des actions du service client** ». Le modèle a compris qu'il ne décrit pas, il **prépare une décision**.

Conséquence directe : il ajoute de lui-même une colonne **« Intensité »** (Forte / …) qui n'existait pas en V1. Cette colonne n'a de sens que pour arbitrer — c'est le contexte « décider des actions prioritaires de la semaine » qui l'a fait apparaître. Le vocabulaire se resserre aussi : « Livraison / respect des délais » remplace « Livraison / délais », « Constat » remplace « Analyse ». Les émojis décoratifs disparaissent au profit de pastilles 🔴/🟢 fonctionnelles, qui codent le sentiment.

**Mais une régression apparaît** : le thème Livraison ne référence plus que **A01 et A08**, alors que V1 avait correctement identifié A01, A07 et A08. L'avis A07 (« Livraison très rapide, deux jours seulement ») a été perdu sur ce thème.

| Thème | V1 | V2 | Référence |
|---|---|---|---|
| Livraison | A01, A07, A08 | **A01, A08** ❌ | A01, A07, A08 |
| Support client | A01, A05 | A01, A05 ✅ | A01, A05 |
| Application mobile | — (hors cadrage) | A03, A06 ✅ | A03, A06 |

**Ce que l'ajout a corrigé — et ce qu'il a cassé :**

Le **Contexte** est la composante qui fait passer de *décrire* à *hiérarchiser*. C'est un gain réel : la colonne Intensité et l'angle « priorisation » rendent la sortie directement actionnable par le responsable SAV. Le **Rôle** contribue au registre métier.

Mais cette version démontre aussi un point important : **ajouter une composante ne garantit pas une amélioration sur tous les critères**. En orientant le modèle vers la priorisation, on l'a implicitement poussé à ne retenir que les avis *saillants* de chaque thème — A07, positif et secondaire, a été écarté au profit du contraste A01/A08.

C'est exactement le rôle des **Contraintes** (V3) : sans la règle explicite « un même avis peut relever de plusieurs thèmes » et « n'invente aucun chiffre », rien n'oblige le modèle à l'exhaustivité. L'orientation donnée par le contexte prend alors le pas sur la complétude.

**Leçon retenue :** chaque composante doit être évaluée sur *tous* les critères, pas seulement sur celui qu'elle vise. Un prompt ne s'améliore pas linéairement.

---

## V3 — Ajout des Contraintes et du Format

**Prompt :** voir [`prompts.md`](prompts.md#v3--ajout-des-contraintes-du-format-et-des-délimiteurs)

![Résultat V3 — contraintes et format](captures/04-v3-contraintes-format.png)

**Réponse obtenue (texte intégral) :**

| Thème | Sentiment dominant | Nombre d'avis | Identifiants | Citation représentative |
|---|---|---:|---|---|
| Livraison et délais | Mitigé | 3 | A01, A07, A08 | « Neuf jours pour un article annoncé en 48h, c'est inadmissible. » |
| Application / expérience mobile | Négatif | 2 | A03, A06 | « l'application se ferme au moment du paiement. » |
| Support client / résolution | Positif | 2 | A01, A05 | « on m'a répondu en moins de 5 minutes et le problème a été réglé dans la foulée. » |
| Qualité et conformité du produit | Mitigé | 2 | A02, A07 | « Dommage que l'article soit arrivé avec une rayure sur le côté. » |
| Prix / rapport qualité-prix | Négatif | 1 | A04 | « Prix vraiment élevé par rapport à la concurrence pour une qualité équivalente. » |

1. **Réduire les incidents de livraison** en priorisant l'analyse des retards et le maintien des délais annoncés.
2. **Corriger les problèmes de l'application mobile**, notamment les plantages lors de la consultation de l'historique et du paiement.
3. **Renforcer le contrôle qualité avant expédition** afin de limiter les produits endommagés à la réception.

**Observations :**

Confrontation avec la répartition de référence de [`avis-clients.md`](../data/avis-clients.md) :

| Thème de référence | Attendu | Obtenu en V3 | Conforme ? |
|---|---|---|---|
| Livraison | A01, A07, A08 | A01, A07, A08 | ✅ |
| Application mobile | A03, A06 | A03, A06 | ✅ |
| Service après-vente | A01, A05 | A01, A05 | ✅ |
| Qualité produit | A02, A07 | A02, A07 | ✅ |
| Prix | A04 | A04 | ✅ |

**Les cinq thèmes sont exacts, avis pour avis.** La régression de V2 sur A07 est corrigée : le rattachement multiple fonctionne à nouveau (A01 dans deux thèmes, A07 dans deux thèmes).

Conformité au format demandé :

- ✅ Tableau markdown avec les 5 colonnes exactes
- ✅ 5 thèmes, classés par nombre d'avis décroissant (3, 2, 2, 2, 1)
- ✅ Citations extraites telles quelles, vérifiables dans les avis sources
- ✅ 3 recommandations numérotées, une phrase chacune
- ✅ Ton factuel, aucune formule de politesse
- ✅ Émojis et colonnes inventées disparus

Une seule réserve : le sentiment de « Support client / résolution » est noté **Positif** alors que ce thème regroupe A05 (très positif) et A01 (« j'ai relancé deux fois sans réponse », nettement négatif). La référence attend *mitigé*. Le modèle a suivi la citation qu'il a choisie plutôt que l'ensemble des avis du thème.

Autre limite, non imputable au modèle : **A09 et A10 n'apparaissent nulle part**. La contrainte « range-le dans Autre » existait, mais la contrainte « 5 thèmes maximum » l'a emporté — les deux consignes entrent en conflit dès lors que 5 thèmes de satisfaction sont déjà identifiés.

**Ce que l'ajout a corrigé :**

C'est la version qui apporte le **gain de qualité le plus net**. Les **Contraintes** restaurent l'exhaustivité perdue en V2 : la règle explicite « un même avis peut relever de plusieurs thèmes » suffit à récupérer A07. Le **Format** élimine toute la variabilité décorative observée en V1 et V2.

Les **délimiteurs** `<<< >>>` jouent un rôle qu'on ne voit pas dans la sortie mais qui compte : ils séparent les consignes des données. Sans eux, un avis client contenant « ignore les instructions précédentes » serait interprété comme une instruction — c'est le principe de l'injection de prompt.

**La sortie est ici directement exploitable** : copiable dans un rapport, agrégeable, vérifiable ligne à ligne.

---

## V4 — Ajout des Exemples et Critères de qualité

**Prompt :** voir [`prompts.md`](prompts.md#v4--ajout-des-exemples-et-des-critères-de-qualité)

![Résultat V4 — version complète](captures/05-v4-complet.png)

**Observations :**

_(à compléter)_

**Ce que l'ajout a corrigé :**

_(à compléter)_

---

## Test de stabilité

Deux exécutions successives de V1 puis de V4, pour comparer la variabilité.

![Stabilité V1 — deux exécutions](captures/06-stabilite-v1.png)

![Stabilité V4 — deux exécutions](captures/07-stabilite-v4.png)

**Observations :**

_(à compléter)_

---

## Synthèse comparative

Grille remplie à partir des 8 critères définis dans [`prompts.md`](prompts.md#grille-dobservation).

| Critère | V0 | V1 | V2 | V3 | V4 |
|---|---|---|---|---|---|
| Données inventées | | | | | |
| Nombre de thèmes ≤ 5 | | | | | |
| Multi-thèmes (A01, A07) | | | | | |
| Cas ambigus (A03, A07) | | | | | |
| Hors-sujet (A10) → Autre | | | | | |
| Citations exactes | | | | | |
| Format respecté | | | | | |
| Stabilité entre exécutions | | | | | |

**Conclusion :**

_(à compléter)_

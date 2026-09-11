# Partie 3 — Résultats obtenus et analyse

**LLM utilisé :** ChatGPT (OpenAI)
**Date d'exécution :** 12 septembre 2025

---

# Exercice 1 — Décomposition

## P1 — Prompt vague (référence)

**Prompt :** voir [`prompts.md`](prompts.md#p1--prompt-vague-référence)

![Résultat du prompt vague](captures/01-prompt-vague.png)

**Réponse obtenue — synthèse des priorités :**

| Problème | Avis | Priorité attribuée |
|---|---|---|
| Crashs de l'application / paiement | A03, A06 | 🔴 Critique |
| Retard de livraison + support silencieux | A01 | 🔴 Critique |
| Produit endommagé | A07 | 🟠 Élevée |
| Prix trop élevés | A04 | 🟠 Élevée |
| Manque d'information sur les boutiques | A10 | 🟡 Moyenne |

La réponse complète comprend en outre, pour chaque problème, 3 à 5 recommandations détaillées, un encart « Point positif à préserver » (A05, A02, A08) et une « Action prioritaire de la semaine ».

**Observations :**

| Critère | Constat |
|---|---|
| Critère de priorité explicite | ⚠️ partiellement — justifié *a posteriori*, jamais énoncé comme règle |
| Classement obtenu | Application > Livraison > Qualité > Prix > Boutiques |
| Étapes vérifiables séparément | ❌ non — résultat monolithique |
| Recommandations ancrées dans les avis | ❌ non — largement extrapolées |
| Causes inventées | ⚠️ évitées de justesse, mais frôlées |

### L'hypothèse est infirmée sur le classement

On s'attendait à un classement par **fréquence** (Livraison 3 avis en tête). Le modèle a fait mieux : il a classé par **gravité**, plaçant l'application mobile en premier avec seulement 2 avis, et justifie ce choix — « cela peut directement empêcher une commande et donc entraîner une perte de chiffre d'affaires », puis en conclusion « les problèmes les plus susceptibles de bloquer directement l'achat ».

**Le modèle a donc choisi un critère pertinent, et l'a explicité après coup.** C'est un résultat meilleur qu'anticipé, et il nuance le propos du cadrage : sur ce jeu de données, l'implicite n'a pas produit un mauvais classement.

Mais le critère reste **choisi par le modèle, pas par l'utilisateur**. Rien ne garantit qu'un autre lot d'avis, ou une autre exécution, donnerait le même arbitrage. L'utilisateur découvre le critère en lisant la réponse — il ne l'a pas décidé.

### Le vrai problème est ailleurs : les recommandations

C'est là que le prompt vague coûte cher. Sur les ~20 recommandations produites, **la grande majorité ne peut pas être déduite des avis fournis** :

| Recommandation produite | Ancrage dans les avis |
|---|---|
| « Reproduire les crashs sur plusieurs appareils et versions d'OS » | ❌ aucun avis ne mentionne d'appareil ni d'OS |
| « Ajouter des tests automatisés sur le parcours de paiement » | ❌ aucune information sur les pratiques de test |
| « Vérifier les conditions de stockage et de transport » | ❌ aucun avis ne parle de stockage |
| « Suivre le taux de produits endommagés par transporteur » | ❌ aucun transporteur mentionné |
| « Tester des promotions, bundles ou programmes de fidélité » | ❌ aucun avis n'évoque de dispositif commercial |
| « Réaliser une veille régulière des prix concurrents » | ⚠️ A04 mentionne « la concurrence », sans plus |
| « Définir un SLA de réponse du support » | ⚠️ déduit de « relancé deux fois sans réponse » |

**Ces recommandations ne sont pas fausses — elles sont de bon sens.** C'est précisément ce qui les rend problématiques : elles proviennent des connaissances générales du modèle en e-commerce, pas de l'analyse des avis. Un lecteur ne peut pas distinguer ce qui vient des données de ce qui vient du modèle.

Le prompt demandait « les recommandations » sans préciser leur fondement. Le modèle a comblé ce vide par son savoir général — comportement raisonnable, mais qui transforme une analyse de données en consultation générique.

### Deux erreurs factuelles

**1. A01 rattaché à un seul thème.** Le modèle fusionne « Retards de livraison **et** absence de réponse du support » en un seul problème. Or ce sont deux problèmes distincts appelant deux actions différentes (logistique / service client). A05 montre d'ailleurs que le support fonctionne bien par ailleurs — l'information est reléguée dans l'encart « point positif » au lieu de nuancer le diagnostic.

**2. A10 traité comme un problème.** « Est-ce que vous ouvrez une boutique à Bordeaux ? » est une **question**, pas une insatisfaction. Le modèle en tire un problème d'« informations insuffisantes sur l'implantation physique » et recommande de créer une page boutiques et une FAQ. C'est une sur-interprétation : un seul client a posé une question, rien n'indique un manque d'information généralisé.

À l'inverse, **A09 (« Correct. ») est correctement ignoré** — le modèle n'a pas cherché à en tirer un problème.

### Ce que P1 établit

Le prompt vague produit une réponse **impressionnante et largement juste sur le diagnostic**, mais :

- le critère de priorité est un choix du modèle, non de l'utilisateur ;
- les recommandations mélangent, sans distinction visible, ce qui vient des avis et ce qui vient du savoir général du modèle ;
- une question est requalifiée en problème ;
- aucune étape n'est vérifiable isolément : pour contrôler le classement, il faut relire toute la réponse.

**C'est exactement ce que la décomposition (P2) doit corriger** — non pas en rendant le modèle plus intelligent, mais en rendant chaque étape auditable et en ancrant explicitement les recommandations dans les données.

# Partie 1 — Prompts V0 à V4

Chaque version ajoute une ou deux composantes à la précédente.
Les avis à coller à la place de `{avis}` sont ceux de [`data/avis-clients.md`](../data/avis-clients.md).

**Protocole d'exécution :** exécuter chaque version dans une **conversation neuve**, pour éviter que le contexte d'une version précédente n'influence la suivante. Capturer la réponse complète.

---

## V0 — Intention brute

*Composantes : aucune.*

```text
Analyse les retours clients.
```

**Hypothèse.** Le modèle n'a ni données ni consigne précise. Il devrait soit demander des précisions, soit inventer des avis, soit disserter sur la méthodologie d'analyse des retours clients.

---

## V1 — Ajout de la Tâche

*Composantes ajoutées : **Tâche**, **Données**.*

```text
Analyse les retours clients suivants et identifie les thèmes principaux ainsi que le sentiment associé à chacun.

{avis}
```

**Hypothèse.** La sortie devient exploitable, mais la longueur, la structure et le niveau de détail restent au choix du modèle. Deux exécutions devraient donner deux formes différentes.

---

## V2 — Ajout du Rôle et du Contexte

*Composantes ajoutées : **Rôle**, **Contexte**.*

```text
Tu es analyste de la satisfaction client dans une entreprise de e-commerce.
Ton analyse sera lue par le responsable du service client, qui doit décider des actions prioritaires de la semaine.

Analyse les retours clients suivants et identifie les thèmes principaux ainsi que le sentiment associé à chacun.

{avis}
```

**Hypothèse.** Le vocabulaire devrait devenir plus métier, et surtout la réponse devrait **hiérarchiser** en vue d'une décision, au lieu de décrire les avis un par un.

---

## V3 — Ajout des Contraintes, du Format et des délimiteurs

*Composantes ajoutées : **Contraintes**, **Format de sortie**, **Ton**.*

```text
Tu es analyste de la satisfaction client dans une entreprise de e-commerce.
Ton analyse sera lue par le responsable du service client, qui doit décider des actions prioritaires de la semaine.

Tâche : analyser les avis clients fournis ci-dessous.

Pour chaque thème identifié, indique :
- le nom du thème
- le sentiment dominant (positif, négatif, neutre ou mitigé)
- le nombre d'avis concernés
- l'identifiant des avis concernés
- une citation représentative, extraite telle quelle

Contraintes :
- 5 thèmes maximum, classés par nombre d'avis décroissant
- un même avis peut relever de plusieurs thèmes
- n'utilise que les avis fournis ; n'invente aucun avis, aucun thème ni aucun chiffre
- si un avis ne relève d'aucun thème de satisfaction, range-le dans "Autre"
- les citations doivent être des extraits exacts, sans reformulation

Ton : factuel et synthétique, sans formule de politesse.

Format : un tableau markdown, suivi de 3 recommandations d'action numérotées, une phrase chacune.

Avis à analyser :
<<<
{avis}
>>>
```

**Hypothèse.** La sortie devrait devenir stable et directement exploitable. Les délimiteurs `<<< >>>` séparent les consignes des données, ce qui protège aussi contre l'injection de prompt (un avis contenant « ignore les instructions précédentes »).

---

## V4 — Ajout des Exemples et des Critères de qualité

*Composantes ajoutées : **Exemples**, **Critères de qualité**. Version complète.*

```text
Tu es analyste de la satisfaction client dans une entreprise de e-commerce.
Ton analyse sera lue par le responsable du service client, qui doit décider des actions prioritaires de la semaine.

Tâche : analyser les avis clients fournis ci-dessous.

Pour chaque thème identifié, indique :
- le nom du thème
- le sentiment dominant (positif, négatif, neutre ou mitigé)
- le nombre d'avis concernés
- l'identifiant des avis concernés
- une citation représentative, extraite telle quelle

Contraintes :
- 5 thèmes maximum, classés par nombre d'avis décroissant
- un même avis peut relever de plusieurs thèmes
- n'utilise que les avis fournis ; n'invente aucun avis, aucun thème ni aucun chiffre
- si un avis ne relève d'aucun thème de satisfaction, range-le dans "Autre"
- les citations doivent être des extraits exacts, sans reformulation

Ton : factuel et synthétique, sans formule de politesse.

Format : un tableau markdown, suivi de 3 recommandations d'action numérotées, une phrase chacune.

Exemple d'une ligne de tableau correctement formée :

| Thème | Sentiment | Nb avis | Avis | Citation |
|---|---|---|---|---|
| Livraison | mitigé | 3 | A01, A07, A08 | « Neuf jours pour un article annoncé en 48h » |

Critères de qualité : une bonne réponse est vérifiable. Chaque chiffre et chaque citation doit pouvoir être retrouvé à l'identique dans les avis fournis. En cas de doute sur le rattachement d'un avis à un thème, privilégie la catégorie "Autre" plutôt qu'une hypothèse.

Avis à analyser :
<<<
{avis}
>>>
```

**Hypothèse.** Le format devrait être calibré au plus près, et la consigne de vérifiabilité devrait réduire les rattachements approximatifs.

---

## Grille d'observation

À remplir pour chaque version, dans [`resultats.md`](resultats.md) :

| Critère | Ce qu'on observe |
|---|---|
| Données inventées | Le modèle a-t-il fabriqué des avis ou des chiffres ? |
| Nombre de thèmes | Respecte-t-il la limite de 5 ? |
| Multi-thèmes | A01 et A07 sont-ils rattachés à leurs deux thèmes ? |
| Cas ambigus | Comment A03 et A07 sont-ils traités ? |
| Hors-sujet | A10 est-il rangé dans « Autre » ? |
| Citations | Sont-elles exactes ou reformulées ? |
| Format | Conforme au format demandé ? |
| Stabilité | Deux exécutions donnent-elles la même structure ? |

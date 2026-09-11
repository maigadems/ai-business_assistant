# Partie 2 — Résultats obtenus et analyse

**LLM utilisé :** ChatGPT (OpenAI)
**Date d'exécution :** 12 septembre 2025
**Protocole :** une conversation neuve par technique, même commentaire dans les quatre cas.

**Commentaire testé :** « Le service est rapide mais l'application plante régulièrement. » *(avis A03)*

---

## T1 — Zero-shot

**Prompt :** voir [`prompts.md`](prompts.md#t1--zero-shot)

![Résultat zero-shot](captures/01-zero-shot.png)

**Réponse obtenue (intégrale) :**

```text
Classe : négatif
```

**Observations :**

| Critère | Constat |
|---|---|
| Classe choisie | `négatif` |
| Justification | ❌ aucune |
| Format | ✅ `Classe : <valeur>`, choisi spontanément |
| Verbosité | ✅ minimale — 3 mots |
| Ambiguïté signalée | ❌ non |
| Taxonomie respectée | ✅ reste dans les 3 classes |

Le modèle a tranché sans hésiter et sans commentaire. La réponse est **exploitable telle quelle** : un simple parsing sur `Classe : ` suffirait à l'extraire.

**Analyse :**

Le résultat contredit l'hypothèse formulée dans [`prompts.md`](prompts.md#t1--zero-shot) : on s'attendait à un risque de verbosité, à ce que le modèle disserte sur l'ambiguïté du commentaire. Il n'en est rien — il applique implicitement la règle « le défaut l'emporte » et produit une étiquette nue.

**Le choix `négatif` est défendable**, et correspond d'ailleurs à celui qu'on souhaiterait obtenir : le « mais » de la phrase donne le poids à la seconde proposition, et un plantage régulier appelle une action corrective là qu'un service rapide n'en appelle aucune.

**Mais ce choix n'est pas traçable.** Trois informations manquent, et leur absence pose problème dès qu'on passe à l'échelle :

1. **Aucune justification** — impossible de vérifier si le modèle a raisonné ou deviné.
2. **Aucun signalement du caractère mixte** — l'information « ce commentaire contient aussi un point positif » est perdue définitivement. Une entreprise qui agrège 10 000 avis ainsi classés ne saura jamais que son service est jugé rapide.
3. **Aucune garantie de stabilité** — rien dans le prompt ne fixe la règle de décision. Un commentaire mixte au phrasé différent (« l'application plante mais le service est rapide ») pourrait basculer de l'autre côté.

**Ce que cette technique révèle :**

Le zero-shot est **imbattable en coût** : consigne de trois lignes, réponse de trois mots. Pour un cas simple et non ambigu, il suffit.

Sa faiblesse n'apparaît que sur les cas limites, et elle est silencieuse : **la réponse a l'air parfaite**. Rien ne signale qu'une décision arbitraire a été prise sur un cas qui ne rentrait dans aucune case. C'est précisément ce qui rend cette technique risquée en production — l'erreur ne se voit pas.

---

## T2 — One-shot

**Prompt :** voir [`prompts.md`](prompts.md#t2--one-shot)

![Résultat one-shot](captures/02-one-shot.png)

**Réponse obtenue (intégrale) :**

```text
Classe : négatif
```

**Observations :**

| Critère | Constat | Écart avec T1 |
|---|---|---|
| Classe choisie | `négatif` | **identique** |
| Justification | ❌ aucune | identique |
| Format | ✅ `Classe : <valeur>` | identique |
| Verbosité | ✅ minimale — 3 mots | identique |
| Ambiguïté signalée | ❌ non | identique |
| Taxonomie respectée | ✅ | identique |

**La réponse est rigoureusement identique au zero-shot, sur les six critères.**

**Analyse :**

Ce résultat sans écart est en réalité le plus instructif de la série, à condition de l'interpréter correctement. Il ne signifie pas que le one-shot est inutile en général — il signifie que **cet exemple-là n'apportait rien à ce cas-là**.

L'exemple fourni était :

> « Produit conforme à la description, emballage soigné. » → `positif`

Il enseigne deux choses : le **format** de réponse (`Classe : <valeur>`) et un **cas franchement positif**. Or :

- Le format était déjà correct en zero-shot — le modèle l'avait déduit seul de la structure de la consigne. L'exemple confirme un comportement acquis.
- Le cas positif n'a **aucun rapport** avec la difficulté à résoudre, qui est un cas *mixte*. L'exemple ne dit rien de ce qu'il faut faire quand positif et négatif coexistent.

**Conclusion : un exemple qui ne couvre pas le cas difficile ne coûte que des tokens.**

C'est une leçon transposable : le choix des exemples importe davantage que leur nombre. Un exemple few-shot n'a de valeur que s'il **désambiguïse une décision que la consigne laisse ouverte**. Ici, la consigne laissait ouverte la règle des cas mixtes, et l'exemple parlait d'autre chose.

**Ce que cette comparaison isole :**

Entre T1 et T2, une seule variable a changé — la présence d'un exemple non pertinent. Le résultat inchangé permet d'attribuer proprement à T3 (few-shot avec cas mixte) et T4 (règle explicite) tout écart qui apparaîtrait ensuite.

**Prédiction pour T3 :** le few-shot contient un cas mixte (A07) résolu en `négatif`. Si la classe reste `négatif`, deux interprétations resteront possibles — imitation de l'exemple, ou même raisonnement implicite qu'en T1. Le départage se fera sur T4, où la règle est énoncée et la justification demandée.

---

## T3 — Few-shot

**Prompt :** voir [`prompts.md`](prompts.md#t3--few-shot)

![Résultat few-shot](captures/03-few-shot.png)

**Réponse obtenue (intégrale) :**

```text
Classe : négatif
```

**Observations :**

| Critère | Constat | Écart avec T1 et T2 |
|---|---|---|
| Classe choisie | `négatif` | **identique** |
| Justification | ❌ aucune | identique |
| Format | ✅ `Classe : <valeur>` | identique |
| Verbosité | ✅ minimale — 3 mots | identique |
| Ambiguïté signalée | ❌ non | identique |
| Taxonomie respectée | ✅ | identique |

**Trois techniques, trois réponses rigoureusement identiques**, alors que le coût en tokens a été multiplié par environ quatre entre T1 et T3.

**Analyse :**

Le quatrième exemple couvrait pourtant bien le cas difficile, contrairement à celui du one-shot :

> « Livraison très rapide, deux jours seulement. Dommage que l'article soit arrivé avec une rayure sur le côté. » → `négatif`

C'est un cas mixte résolu, structurellement analogue au commentaire à classer (un point positif, un point négatif, le négatif l'emportant). L'exemple *enseignait* donc bien la règle « quand c'est mixte, le défaut l'emporte ».

**Et pourtant il n'a rien changé.** Ce qui conduit à la conclusion suivante : le modèle appliquait **déjà** cette règle en zero-shot. L'exemple n'a pas enseigné un comportement, il a confirmé un comportement préexistant.

**Ce que cette convergence établit — et ce qu'elle n'établit pas :**

✅ **Établi :** sur ce cas, les exemples n'apportent aucun gain de classification. La règle implicite du modèle coïncide avec celle qu'on voulait lui transmettre.

❌ **Non établi :** on ne peut **pas** conclure que le few-shot est inutile en général. Deux réserves importantes :

1. **Un seul cas testé.** La convergence sur A03 ne dit rien du comportement sur un commentaire mixte dont on voudrait qu'il soit classé *positif* — là, l'exemple devrait faire une différence, puisqu'il faudrait contredire la règle implicite du modèle.
2. **Une seule exécution par technique.** Sans test de stabilité, on ignore si le few-shot *réduit la variance* entre exécutions. C'est un de ses bénéfices attendus, et il est invisible sur un tirage unique.

**La question restée ouverte :**

Trois techniques donnent `négatif`, mais **aucune ne dit pourquoi**. Impossible de distinguer :

- un modèle qui a identifié le caractère mixte et appliqué délibérément une règle de priorité au défaut ;
- un modèle qui a simplement détecté le mot « plante » et classé sur ce signal.

Les deux produisent la même étiquette sur ce cas, et divergeraient sur d'autres. **C'est exactement ce que T4 va permettre de trancher**, en exigeant une justification et un champ `mixte` explicite.

**Coût comparé :**

| Technique | Longueur du prompt | Résultat |
|---|---|---|
| T1 zero-shot | ~3 lignes | `négatif` |
| T2 one-shot | ~8 lignes | `négatif` |
| T3 few-shot | ~17 lignes | `négatif` |

Sur ce cas précis, **T1 offre le meilleur rapport qualité/coût** : le même résultat pour un cinquième des tokens. Un enseignement contre-intuitif, qui rappelle qu'ajouter des exemples n'est pas une amélioration par défaut — c'est un investissement qui doit se justifier par un gain mesuré.

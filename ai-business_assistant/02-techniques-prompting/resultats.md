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

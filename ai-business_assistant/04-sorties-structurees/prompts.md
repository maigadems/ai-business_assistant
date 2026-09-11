# Partie 4 — Prompts testés

**Protocole :** une conversation neuve par prompt.

**Commentaire de référence** (celui de l'énoncé) :
> « Commande passée le 3, reçue le 12. Neuf jours pour un article annoncé en 48h, c'est inadmissible. J'ai relancé deux fois sans réponse. » *(avis A01)*

---

## Q1 — Demander le JSON

*Champs, types et valeurs autorisées précisés. Aucune règle de validation.*

```text
Tu es un système d'analyse d'avis clients pour une entreprise de e-commerce.

Analyse le commentaire ci-dessous et retourne le résultat en JSON.

Champs attendus :
- "sentiment" (chaîne) : le sentiment global. Valeurs autorisées : "positif", "negatif", "neutre"
- "categorie" (chaîne) : le domaine concerné. Valeurs autorisées : "livraison", "application", "prix", "sav", "produit", "autre"
- "urgence" (chaîne) : le niveau de traitement requis. Valeurs autorisées : "faible", "moyenne", "elevee"
- "probleme" (chaîne) : le problème principal, en une phrase courte
- "confiance" (nombre décimal entre 0 et 1) : ton niveau de certitude sur cette analyse

Commentaire à analyser :
<<<
Commande passée le 3, reçue le 12. Neuf jours pour un article annoncé en 48h, c'est inadmissible. J'ai relancé deux fois sans réponse.
>>>
```

**Hypothèse.** Le modèle devrait produire un JSON correct. Points à surveiller : du texte parasite autour du JSON (« Voici le résultat : »), un bloc de code markdown, ou `confiance` retourné en chaîne plutôt qu'en nombre.

---

## Q2 — Ajouter les règles de validation

*Le même prompt, augmenté des cinq règles de sortie imposées par l'énoncé.*

```text
Tu es un système d'analyse d'avis clients pour une entreprise de e-commerce.

Analyse le commentaire ci-dessous et retourne le résultat en JSON.

Champs attendus :
- "sentiment" (chaîne) : le sentiment global. Valeurs autorisées : "positif", "negatif", "neutre"
- "categorie" (chaîne) : le domaine concerné. Valeurs autorisées : "livraison", "application", "prix", "sav", "produit", "autre"
- "urgence" (chaîne) : le niveau de traitement requis. Valeurs autorisées : "faible", "moyenne", "elevee"
- "probleme" (chaîne) : le problème principal, en une phrase courte
- "confiance" (nombre décimal entre 0 et 1) : ton niveau de certitude sur cette analyse

Règles de sortie — ta réponse doit impérativement les respecter :
1. La réponse est un JSON valide, et rien d'autre : aucun texte avant, aucun texte après, aucun bloc de code markdown.
2. Aucune propriété supplémentaire : exactement les cinq champs listés, ni plus ni moins.
3. "sentiment" vaut exactement "positif", "negatif" ou "neutre" — aucune autre valeur, aucune nuance.
4. "confiance" est un nombre décimal compris entre 0 et 1 inclus, écrit sans guillemets et sans signe pourcentage.
5. "urgence" vaut exactement "faible", "moyenne" ou "elevee".

Avant de répondre, vérifie ta sortie contre ces cinq règles.

Commentaire à analyser :
<<<
Commande passée le 3, reçue le 12. Neuf jours pour un article annoncé en 48h, c'est inadmissible. J'ai relancé deux fois sans réponse.
>>>
```

**Hypothèse.** Si Q1 était déjà conforme, Q2 ne changera rien de visible sur ce commentaire — et ce sera le résultat intéressant, comme en Partie 2 : les règles n'ont de valeur que face à un cas qui les met à l'épreuve.

---

## Q3 — Test sur cas ambigu

*Le prompt Q2, appliqué à un commentaire qu'aucune valeur de `sentiment` ne décrit correctement.*

Reprendre **exactement le prompt Q2**, en remplaçant uniquement le commentaire par :

```text
Le service est rapide mais l'application plante régulièrement dès que je veux consulter mon historique.
```

**Hypothèse.** C'est le test décisif. L'avis A03 est mixte : la Partie 2 a montré que le modèle le classe `negatif`. Trois comportements possibles :

- il respecte l'énumération et abaisse `confiance` pour signaler l'ambiguïté → **comportement souhaité** ;
- il respecte l'énumération et garde une `confiance` élevée → l'ambiguïté est perdue silencieusement ;
- il enfreint l'énumération (« mitigé ») → la règle 3 n'a pas tenu.

Le champ `confiance` a précisément cette fonction : porter l'incertitude que l'énumération fermée ne peut pas exprimer.

---

## Grille d'observation

| Critère | Q1 | Q2 | Q3 (ambigu) |
|---|---|---|---|
| JSON valide | | | |
| Texte parasite | | | |
| Exactement 5 champs | | | |
| Énumérations respectées | | | |
| `confiance` de type nombre | | | |
| Valeur de `confiance` | | | |
| Ambiguïté signalée | | | |

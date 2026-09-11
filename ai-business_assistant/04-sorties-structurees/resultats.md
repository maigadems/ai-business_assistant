# Partie 4 — Résultats obtenus et analyse

**LLM utilisé :** ChatGPT (OpenAI)
**Date d'exécution :** 12 septembre 2025

---

## Q1 — Demander le JSON, sans règles de validation

**Prompt :** voir [`prompts.md`](prompts.md#q1--demander-le-json)

![Résultat JSON sans règles](captures/01-json-simple.png)

**Réponse obtenue (intégrale) :**

```json
{
  "sentiment": "negatif",
  "categorie": "livraison",
  "urgence": "elevee",
  "probleme": "Livraison très en retard et absence de réponse du service client malgré deux relances.",
  "confiance": 0.99
}
```

**Observations :**

| Critère | Constat |
|---|---|
| JSON valide | ✅ parsable tel quel |
| Texte parasite | ✅ aucun — pas de « Voici le résultat », pas de bloc markdown |
| Exactement 5 champs | ✅ ni plus ni moins |
| Énumérations respectées | ✅ `negatif`, `livraison`, `elevee` sont bien dans les domaines |
| `confiance` de type nombre | ✅ `0.99` sans guillemets |
| Valeur de `confiance` | ⚠️ 0.99 — discutable, voir ci-dessous |

**La sortie est directement consommable.** `json.loads()` fonctionne sans nettoyage, les cinq champs sont présents, les trois énumérations tenues et `confiance` est bien un nombre.

### Le contraste avec la prose de l'énoncé

| | Réponse en prose | JSON obtenu |
|---|---|---|
| Sentiment | « semble **plutôt** négatif » | `"negatif"` |
| Extraction | analyse de texte requise | `data["sentiment"]` |
| Agrégation | impossible | `GROUP BY sentiment` |
| Urgence | absente | `"elevee"` |
| Incertitude | modalisée dans la phrase | `0.99`, champ dédié |

Le gain n'est pas seulement une question de forme : **le JSON force à nommer des choses que la prose laissait implicites**. L'urgence n'existait pas dans la réponse d'origine — le champ l'a fait apparaître.

### Le point discutable : `confiance: 0.99`

L'avis A01 contient **deux problèmes distincts** :

- un retard de livraison (9 jours au lieu de 48h) → catégorie `livraison`
- deux relances sans réponse → catégorie `sav`

Le modèle a choisi `livraison` et mentionné le SAV dans le champ `probleme` — arbitrage défendable, le retard étant le grief principal. **Mais il annonce une confiance de 0,99 sur ce choix**, soit une quasi-certitude, alors que `sav` aurait été tout aussi justifiable.

C'est une observation importante : **`confiance` mesure ici la certitude sur l'analyse du sentiment, pas sur le choix de la catégorie.** Le prompt disait « ton niveau de certitude sur cette analyse » — formulation trop vague pour désigner *quoi*, dans une sortie à cinq champs.

Le sentiment est effectivement indiscutable (« c'est inadmissible »), ce qui justifie 0,99. L'arbitrage de catégorie, lui, ne l'est pas. **Un seul scalaire ne peut pas porter la confiance de cinq champs hétérogènes.**

Deux corrections possibles, à retenir pour un usage réel :

1. préciser ce que `confiance` qualifie (« ta certitude sur le champ `sentiment` ») ;
2. ou prévoir un champ `categorie_secondaire`, voire une confiance par champ.

### Les hypothèses sont infirmées

Aucun des trois risques anticipés ne s'est matérialisé : pas de bloc markdown, pas de texte d'introduction, pas de `confiance` en chaîne. Le modèle a produit exactement ce qui était décrit.

**Cela crée la bonne condition pour la question 2 :** si Q1 est déjà conforme, que peuvent bien ajouter les règles de validation ? C'est précisément ce que le prompt Q2 doit permettre de mesurer — et le résultat risque d'être « rien de visible », ce qui sera en soi un enseignement sur la différence entre *demander* et *garantir*.

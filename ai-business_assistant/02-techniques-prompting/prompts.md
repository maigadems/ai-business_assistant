# Partie 2 — Les quatre prompts testés

**Protocole :** une conversation neuve par technique. Le commentaire à classer est identique dans les quatre cas — seule la technique change.

**Commentaire testé :** « Le service est rapide mais l'application plante régulièrement. » *(avis A03)*

---

## T1 — Zero-shot

*La consigne seule, aucun exemple.*

```text
Classe le commentaire suivant.

Commentaire : "Le service est rapide mais l'application plante régulièrement."

Classes possibles : positif, négatif, neutre.
```

**Hypothèse.** Le modèle devrait trancher, mais on ignore vers quelle classe et avec quelle justification. Risque de verbosité : il peut disserter sur l'ambiguïté au lieu de classer.

---

## T2 — One-shot

*La consigne + un exemple résolu.*

```text
Classe les commentaires clients selon leur sentiment.

Classes possibles : positif, négatif, neutre.

Exemple :
Commentaire : "Produit conforme à la description, emballage soigné."
Classe : positif

À classer :
Commentaire : "Le service est rapide mais l'application plante régulièrement."
Classe :
```

**Hypothèse.** Le format de réponse devrait se caler sur celui de l'exemple (une étiquette seule, sans justification). L'exemple choisi est volontairement **non ambigu** : il enseigne le format, pas la règle de décision pour les cas mixtes.

---

## T3 — Few-shot

*La consigne + quatre exemples résolus, dont un cas mixte.*

```text
Classe les commentaires clients selon leur sentiment.

Classes possibles : positif, négatif, neutre.

Exemples :
Commentaire : "Produit conforme à la description, emballage soigné."
Classe : positif

Commentaire : "Prix vraiment élevé par rapport à la concurrence pour une qualité équivalente."
Classe : négatif

Commentaire : "Est-ce que vous ouvrez une boutique à Bordeaux ?"
Classe : neutre

Commentaire : "Livraison très rapide, deux jours seulement. Dommage que l'article soit arrivé avec une rayure sur le côté."
Classe : négatif

À classer :
Commentaire : "Le service est rapide mais l'application plante régulièrement."
Classe :
```

**Hypothèse.** Le quatrième exemple (A07) est lui aussi un **cas mixte**, résolu en `négatif`. Il enseigne implicitement la règle : *quand un commentaire mêle positif et négatif, le défaut l'emporte*. Le modèle devrait donc répondre `négatif` — non parce qu'il l'a raisonné, mais parce qu'il a **imité le précédent**.

C'est le point à vérifier : l'exemple transmet-il bien une règle de décision, comme la Partie 1 l'a suggéré ?

---

## T4 — Prompt structuré

*La consigne décomposée en sections, avec règle de décision explicite.*

```text
# Rôle
Tu es un système de classification de sentiment pour les avis clients d'une entreprise de e-commerce.

# Tâche
Classer un commentaire client dans une des classes autorisées.

# Classes autorisées
- positif : le commentaire exprime uniquement de la satisfaction
- négatif : le commentaire exprime une insatisfaction, même partielle
- neutre : le commentaire n'exprime aucune opinion (question, constat factuel, message trop court)

# Règle de décision pour les cas mixtes
Si un commentaire contient à la fois un élément positif et un élément négatif, classe-le en "négatif" : un défaut signalé appelle une action, un compliment non.

# Contraintes
- réponds uniquement par une des trois classes autorisées
- n'invente aucune classe supplémentaire
- si le commentaire est mixte, signale-le dans le champ prévu

# Format de sortie
JSON valide, sans texte avant ni après :
{
  "classe": "positif | négatif | neutre",
  "mixte": true | false,
  "justification": "une phrase, citant les éléments du commentaire"
}

# Commentaire à classer
<<<
Le service est rapide mais l'application plante régulièrement.
>>>
```

**Hypothèse.** La règle de décision explicite devrait produire le même résultat que le few-shot (`négatif`), mais **pour une raison traçable** plutôt que par imitation. Le champ `mixte` permet de conserver l'information que la taxonomie à 3 classes fait perdre.

---

## Grille d'observation

| Critère | T1 zero-shot | T2 one-shot | T3 few-shot | T4 structuré |
|---|---|---|---|---|
| Classe choisie | | | | |
| Justification fournie | | | | |
| Format exploitable | | | | |
| Verbosité | | | | |
| Ambiguïté signalée | | | | |
| Taxonomie respectée | | | | |

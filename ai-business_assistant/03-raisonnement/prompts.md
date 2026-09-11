# Partie 3 — Prompts testés

**Protocole :** conversation neuve pour P1 et P2. **P3 doit impérativement être envoyé dans la même conversation que P2** — c'est le principe même de l'auto-vérification : le modèle doit avoir sa propre réponse en contexte.

---

## Exercice 1 — Décomposition

### P1 — Prompt vague (référence)

*Le prompt de l'énoncé, tel quel.*

```text
Analyse ces avis clients et donne-moi les problèmes les plus importants ainsi que les recommandations.

{avis}
```

**Hypothèse.** Le modèle va produire un classement sans dire selon quel critère il l'établit. On s'attend à ce qu'il choisisse implicitement la **fréquence**, et probablement à ce que certaines recommandations dépassent ce que les avis permettent d'affirmer.

---

### P2 — Prompt décomposé

*La même demande, découpée en cinq sous-tâches ordonnées, avec le critère de priorité explicité.*

```text
Tu es analyste de la satisfaction client dans une entreprise de e-commerce.

Analyse les avis clients fournis en suivant exactement les cinq étapes ci-dessous, dans l'ordre, et en présentant le résultat de chaque étape sous son propre titre.

## Étape 1 — Extraction
Pour chaque avis, indique l'identifiant et le problème exprimé, en une phrase.
Si un avis n'exprime aucun problème, écris "aucun problème".

## Étape 2 — Regroupement
Regroupe les problèmes extraits en thèmes. Pour chaque thème, liste les identifiants des avis concernés.

## Étape 3 — Mesure
Pour chaque thème, indique séparément :
- fréquence : le nombre d'avis concernés
- gravité : faible, moyenne ou élevée, selon qu'elle empêche ou non le client d'acheter ou de recevoir sa commande

## Étape 4 — Priorisation
Classe les thèmes par priorité décroissante.
Règle de priorité : la gravité prime sur la fréquence. À gravité égale, la fréquence départage.
Justifie le rang de chaque thème en une phrase.

## Étape 5 — Recommandations
Propose une action par thème prioritaire, en te limitant aux trois premiers.
Chaque recommandation doit répondre à un problème effectivement présent dans les avis.

Contraintes :
- n'utilise que les avis fournis ; n'invente aucun avis, aucun chiffre ni aucune cause
- si une cause n'est pas donnée dans les avis, écris "cause non précisée dans les avis"
- ne propose aucune recommandation qui ne corresponde pas à un thème identifié à l'étape 2

Avis à analyser :
<<<
{avis}
>>>
```

**Hypothèse.** Chaque étape devient vérifiable indépendamment. Le critère de priorité étant énoncé, le classement devrait différer de celui de P1 — l'application mobile devrait remonter, puisqu'elle bloque le paiement.

---

## Exercice 2 — Auto-vérification

### P3 — Prompt de vérification

*À envoyer **dans la même conversation** que P2, juste après sa réponse.*

```text
Vérifie maintenant ta réponse précédente.

Contrôle les cinq points suivants, un par un, sous forme de tableau :

1. **Informations non justifiées** — quelles affirmations de ta réponse ne s'appuient sur aucun avis fourni ?
2. **Contradictions** — ta réponse se contredit-elle, ou contredit-elle le contenu des avis ?
3. **Informations absentes** — quels éléments présents dans les avis as-tu omis ?
4. **Hallucinations** — as-tu inventé un fait, un chiffre, une citation ou une cause ?
5. **Respect des contraintes** — pour chacune des trois contraintes du prompt précédent, indique si elle a été respectée.

Pour chaque point, cite le passage exact de ta réponse concerné.
Si tu ne trouves aucun problème sur un point, écris "aucun" — ne cherche pas à en inventer.

Termine par un verdict : ta réponse précédente est-elle utilisable telle quelle, ou doit-elle être corrigée ?
```

**Hypothèse.** C'est le test décisif. Deux issues possibles, toutes deux instructives :

- Le modèle **trouve de vraies erreurs** → l'auto-vérification a une valeur opérationnelle.
- Le modèle **valide tout** → biais de complaisance, et la technique donne une fausse assurance.

La consigne « ne cherche pas à en inventer » est délibérée : elle neutralise le biais inverse, où le modèle fabriquerait des erreurs pour paraître rigoureux.

---

## Grille d'observation

### Exercice 1 (P1 vs P2)

| Critère | P1 vague | P2 décomposé |
|---|---|---|
| Critère de priorité explicite | | |
| Classement obtenu | | |
| Étapes vérifiables séparément | | |
| Recommandations ancrées dans les avis | | |
| Causes inventées | | |

### Exercice 2 (P3)

| Critère | Constat |
|---|---|
| Erreurs réelles détectées | |
| Fausses erreurs signalées | |
| Auto-complaisance | |
| Verdict cohérent avec les constats | |

# Partie 5 — Prompts pour les applications métier

> **Énoncé.** Créer cinq prompts :
> 1) résumer un document (≤ 250 mots, faits conservés, objectifs, résultats, recommandations, aucune invention) ;
> 2) traduire un document français en anglais (sens, structure, termes techniques conservés, sans résumer ni ajouter) ;
> 3) classer un ticket informatique (réseau, logiciel, matériel, sécurité, accès, autre) en JSON avec `categorie` et `justification` ;
> 4) extraire d'une facture `numero_facture`, `date`, `client`, `montant_ht`, `tva`, `montant_ttc` — JSON valide, `null` si absent ;
> 5) rédiger un email à un client dont la livraison a pris du retard (objectifs, ton, ≤ 150 mots).

---

## 1. Ce qui change par rapport aux parties précédentes

Les parties 1 à 4 exploraient **une** technique à la fois sur un cas unique. La partie 5 applique ce qui en ressort à cinq tâches métier réelles, indépendantes les unes des autres.

Trois acquis sont réinvestis systématiquement :

| Acquis | Partie d'origine | Application ici |
|---|---|---|
| Donner une **formule à produire** plutôt qu'une interdiction | 3 (« cause non précisée ») | `null` en extraction, mention explicite des objectifs non atteints en résumé |
| **Fermer les énumérations** | 2 et 4 | Les six catégories de ticket |
| Un **champ libre** n'est pas reproductible | 4 | `justification` et `probleme` réservés au contexte, jamais au filtrage |

---

## 2. Les cinq tâches et leur difficulté propre

### 5.1 — Résumé contraint

**Difficulté :** la contrainte de 250 mots entre en conflit avec « conserver les informations factuelles ». Il faut choisir quoi sacrifier.

Le [document source](../data/rapport-trimestriel.md) est construit pour rendre ce conflit visible : il contient trois objectifs, dont **deux ne sont pas atteints**, quatre recommandations et une quinzaine de chiffres. Un résumé fidèle doit dire que les objectifs sont manqués ; un résumé complaisant lissera le constat.

**Piège principal :** le document dit que septembre atteint l'objectif alors que le trimestre ne l'atteint pas. Un résumé qui retient « objectif atteint » est faux.

### 5.2 — Traduction fidèle

**Difficulté :** les quatre contraintes (sens, structure, termes techniques, ni résumé ni ajout) visent toutes le même risque — **la tentation d'améliorer**. Un LLM a spontanément tendance à fluidifier, réorganiser et expliciter.

**Piège principal :** les termes métier français (« taux de résolution au premier contact », « conseiller », « escalade ») ont des équivalents anglais consacrés. Une traduction littérale les manquerait.

### 5.3 — Classification de ticket

**Difficulté :** contrairement au sentiment de la Partie 2, les six catégories se **recouvrent réellement**. Un poste qui ne se connecte plus au réseau d'entreprise peut relever de `reseau`, `materiel` ou `acces`.

**Piège principal :** le champ `justification` est libre — il ne doit donc jamais servir à filtrer. Sa fonction est de rendre l'arbitrage contestable par un humain.

### 5.4 — Extraction de facture

**Difficulté :** c'est la tâche la plus mécanique, et la plus exposée à l'hallucination. Un modèle qui ne trouve pas un numéro de facture aura tendance à en construire un plausible à partir d'autres chiffres du document.

Les [deux factures de test](../data/facture.md) sont conçues pour cela : la première est complète avec quatre pièges de lecture, la seconde a un **numéro absent** et une **TVA non applicable**.

**Piège principal :** la facture B teste directement la consigne `null`. C'est le seul cas de l'atelier où l'on peut vérifier objectivement si le modèle invente.

### 5.5 — Email client

**Difficulté :** c'est la seule tâche **générative** des cinq. Il n'y a pas de bonne réponse unique, et le risque est inverse de celui de l'extraction : non pas inventer un fait, mais **inventer une cause**.

L'énoncé le dit explicitement — « expliquer la situation **sans inventer de cause** ». Un modèle non contraint écrira spontanément « en raison d'un pic d'activité saisonnier » ou « un incident chez notre transporteur », qui sonnent juste mais sont fabriqués.

**Piège principal :** cette contrainte est en tension avec l'objectif « expliquer la situation ». Comment expliquer sans cause ? La réponse attendue est de décrire ce qui est su (le retard, sa durée) sans en fabriquer l'origine.

---

## 3. Grille d'évaluation commune

| Critère | Question |
|---|---|
| Contraintes de forme | Longueur, format, structure respectés ? |
| Fidélité | Tout ce qui est affirmé provient-il de la source ? |
| Complétude | Les éléments demandés sont-ils tous présents ? |
| Invention | Un fait, chiffre ou cause a-t-il été fabriqué ? |
| Exploitabilité | La sortie est-elle utilisable sans retouche ? |

---

## Prompts testés

Voir [`prompts.md`](prompts.md).

## Résultats et analyse

Voir [`resultats.md`](resultats.md).

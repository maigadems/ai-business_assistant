# Partie 1 — Anatomie d'un prompt

> **Énoncé.** Construire un prompt, à partir de ses différentes composantes, pour résoudre un problème comme « Je souhaite analyser les retours de clients d'une entreprise. »

---

## 1. Analyse du problème de départ

La phrase « Je souhaite analyser les retours de clients d'une entreprise » n'est pas un prompt : c'est une **intention**. Elle exprime un besoin sans préciser aucune des décisions nécessaires à son exécution.

Quatre informations manquent, et chacune sera comblée par un choix par défaut du modèle si on ne la fournit pas :

| Ce qui manque | Question non résolue |
|---|---|
| L'objet de l'analyse | Sentiment ? Thèmes récurrents ? Urgence ? Les trois ? |
| Les données | Quels avis, combien, sous quelle forme ? |
| Le destinataire | Un dirigeant pressé, un analyste, une application ? |
| La forme de la réponse | Prose, tableau, JSON ? Quelle longueur ? |

Un LLM confronté à cette phrase produira donc une réponse **plausible mais générique** : il inventera des avis, choisira seul un angle d'analyse et une mise en forme. Le résultat n'est ni fiable ni reproductible d'une exécution à l'autre.

**Le travail de prompt engineering consiste à reprendre au modèle chacune de ces décisions.**

---

## 2. Les composantes d'un prompt

Un prompt est un assemblage de briques identifiables. Il n'existe pas de liste canonique universelle ; celle retenue ici couvre le consensus et correspond au schéma de l'assistant présenté dans l'énoncé de l'atelier.

| # | Composante | Répond à la question | Conséquence de son absence |
|---|---|---|---|
| 1 | **Rôle** (persona) | Qui parle ? | Registre générique, vocabulaire non métier |
| 2 | **Tâche** (instruction) | Que faire, précisément ? | Le modèle choisit seul l'objectif |
| 3 | **Contexte** | Dans quel cadre, pour qui ? | Réponse hors-sol, mal calibrée |
| 4 | **Données d'entrée** | Sur quoi travailler ? | Le modèle fabrique ses propres exemples |
| 5 | **Contraintes** | Qu'est-ce qui est imposé ou interdit ? | Hallucinations, longueur aléatoire |
| 6 | **Format de sortie** | Sous quelle forme ? | Prose libre, inexploitable en aval |
| 7 | **Exemples** (few-shot) | À quoi ressemble une bonne réponse ? | Interprétation flottante des catégories |
| 8 | **Ton / style** | Sur quel registre ? | Ton par défaut, souvent trop bavard |
| 9 | **Critères de qualité** | Comment la réponse sera-t-elle jugée ? | Aucun garde-fou d'auto-évaluation |

### Hiérarchie d'importance

Toutes les composantes n'ont pas le même rendement :

- **Tâche (2)** et **Format (6)** sont les plus rentables : ce sont elles qui rendent la réponse exploitable.
- **Contraintes (5)** est celle qui réduit le plus les hallucinations.
- **Exemples (7)** est la plus coûteuse en tokens — d'où l'intérêt de la comparaison menée en Partie 2.

### Répartition system / user

Distinction utile pour une mise en production :

- **System prompt** (stable d'un appel à l'autre) : rôle, contexte, contraintes, format, ton, critères de qualité.
- **User prompt** (variable) : les données d'entrée.

C'est cette séparation qui rend le prompt réutilisable plutôt que jetable.

---

## 3. Valeurs retenues pour ce cas

Application des 9 composantes au problème « analyser les retours clients » :

| Composante | Valeur retenue |
|---|---|
| Rôle | Analyste de la satisfaction client, secteur e-commerce |
| Tâche | Identifier les thèmes récurrents et le sentiment associé à chacun |
| Contexte | Lu par le responsable du service client, pour arbitrer les actions de la semaine |
| Données | Les 10 avis de [`data/avis-clients.md`](../data/avis-clients.md), délimités |
| Contraintes | 5 thèmes maximum, citations exactes, aucune invention, catégorie « Autre » |
| Format | Tableau markdown + 3 recommandations numérotées |
| Exemples | Une ligne de tableau type |
| Ton | Factuel et synthétique |
| Qualité | Chaque chiffre et chaque citation doit être retrouvable dans les avis fournis |

---

## 4. Construction incrémentale

La démarche consiste à partir du prompt nu et à **ajouter une composante à la fois**, en observant à chaque étape ce que l'ajout corrige.

Les prompts exécutables se trouvent dans [`prompts.md`](prompts.md).
Les résultats obtenus et leur analyse se trouvent dans [`resultats.md`](resultats.md).

| Version | Composantes ajoutées | Problème visé |
|---|---|---|
| V0 | — (intention brute) | Référence de départ |
| V1 | Tâche | Le modèle ne sait pas quoi faire |
| V2 | Rôle + Contexte | Réponse générique, non hiérarchisée |
| V3 | Contraintes + Format + Données délimitées | Sortie instable et non exploitable |
| V4 | Exemples + Critères de qualité | Calibrage fin, vérifiabilité |

---

## 5. Prompt final retenu

Voir [`prompt-final.md`](prompt-final.md).

---

## 6. Ce que j'en retiens

Les cinq versions ont été exécutées sur ChatGPT, en conversation neuve à chaque fois. Résultats détaillés dans [`resultats.md`](resultats.md).

**Un prompt est un assemblage, et chaque brique a un rendement différent.** Ajouter la Tâche et les Données transforme une non-réponse en analyse utilisable : c'est le gain le plus important. Ajouter les Contraintes et le Format apporte le meilleur gain de qualité : exactitude restaurée, sortie stable et agrégeable.

**L'amélioration n'est pas linéaire.** Deux versions l'ont montré de façon nette : V2 gagne en hiérarchisation mais perd un avis, V4 gagne la catégorie « Autre » mais fusionne deux thèmes distincts. Une composante peut améliorer le critère qu'elle vise tout en dégradant un autre — d'où la nécessité d'une grille d'évaluation multi-critères plutôt que d'un jugement global.

**La version la plus complète n'est pas automatiquement la meilleure.** V4, qui contient les 9 composantes, est moins exacte que V3 sur les rattachements. Le prompt final retenu n'est donc ni l'une ni l'autre, mais leur synthèse corrigée — voir [`prompt-final.md`](prompt-final.md).

**Les exemples few-shot transmettent plus que le format.** L'exemple de V4 montrait un thème large ; le modèle en a déduit une granularité de regroupement qu'on ne cherchait pas à lui enseigner. C'est le principal piège de cette composante, et la raison de son coût réel au-delà des tokens.

**Les contraintes doivent être hiérarchisées, pas juxtaposées.** « 5 thèmes maximum » et « range les hors-sujet dans Autre » sont entrées en conflit : V3 a sacrifié la couverture, V4 la limite. Un prompt rigoureux dit lequel l'emporte.

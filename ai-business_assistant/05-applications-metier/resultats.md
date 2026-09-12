# Partie 5 — Résultats obtenus et analyse

**LLM utilisé :** ChatGPT (OpenAI)
**Date d'exécution :** 12 septembre 2025

---

## 5.1 — Résumé de document

**Prompt :** voir [`prompts.md`](prompts.md#51--résumé-de-document)
**Source :** [`rapport-trimestriel.md`](../data/rapport-trimestriel.md) — environ 950 mots

![Résultat du résumé](captures/01-resume.png)

**Réponse obtenue (intégrale) :**

> ### Objectifs
> - Réduire le délai moyen de première réponse de 14 h à moins de 6 h.
> - Porter la résolution au premier contact de 61 % à 75 %.
> - Déployer le chat en direct sur tout le site avant le 15 septembre 2025.
>
> ### Résultats
> - Délai moyen : **7 h 20**, contre 14 h 10 au trimestre précédent. **Objectif non atteint**. Septembre atteint toutefois **4 h 15**.
> - Résolution au premier contact : **68 %**, contre 61 %. **Objectif de 75 % non atteint**. Les problèmes techniques applicatifs affichent **34 %** de résolution et représentent **22 %** des contacts.
> - Chat déployé le **9 septembre**, six jours avant l'échéance : **objectif atteint**. Il a traité **2 847 conversations**, soit **18 %** des contacts, avec une satisfaction de **4,3/5**.
> - Volume total : **15 820 contacts**, en hausse de **8 %** par rapport au deuxième trimestre.
> - Les deux recrutements prévus ont été réalisés les **12 août** et **3 septembre**.
>
> ### Recommandations
> - Maintenir la cible de **6 heures**, sans renforcement d'effectif supplémentaire.
> - Créer une cellule technique de premier niveau pour résoudre directement **50 %** des problèmes techniques actuellement escaladés, avec un coût estimé à **85 000 € annuels** pour deux postes, sous réserve de validation financière.
> - Négocier avec l'équipe technique un délai d'escalade ramené de **4 à 2 jours ouvrés**.
> - Étendre le chat aux heures de soirée, **18 h–21 h**, période représentant **23 %** des visites du site.

**Observations :**

| Critère | Constat |
|---|---|
| Longueur | ✅ **234 mots** sur 250 autorisés |
| Structure imposée | ✅ les trois intertitres, dans l'ordre |
| Objectifs non atteints signalés | ✅ **explicitement, deux fois** |
| Chiffres conservés | ✅ 17 valeurs numériques reprises, toutes exactes |
| Invention | ✅ aucune |
| Taux de compression | 950 → 234 mots, soit ~75 % |

### Le piège principal est évité

C'était le point de vigilance central. Le document dit que **septembre** atteint l'objectif (4 h 15) alors que **le trimestre** ne l'atteint pas (7 h 20). Un résumé qui retiendrait « objectif atteint » serait faux.

La formulation produite est exactement celle qu'il fallait :

> « Délai moyen : **7 h 20** [...] **Objectif non atteint**. Septembre atteint **toutefois** 4 h 15. »

L'ordre est correct — le constat trimestriel d'abord, la nuance mensuelle ensuite — et le « toutefois » marque la subordination. L'information favorable est conservée sans qu'elle écrase le constat d'échec.

**La contrainte « si un objectif n'est pas atteint, dis-le explicitement ; ne présente pas un résultat partiel comme un succès » a donc fonctionné**, et elle était nécessaire : sans elle, la tentation de mettre en avant la progression (14 h 10 → 7 h 20, soit une division par deux) était forte.

### Les arbitrages de compression

Avec 234 mots pour 950, le modèle a dû sacrifier environ trois quarts du contenu. Ce qu'il a conservé et écarté est révélateur :

| Conservé | Écarté |
|---|---|
| Les 3 objectifs, les 4 recommandations | Le budget de 340 000 € et sa ventilation |
| Tous les résultats chiffrés principaux | Le détail par motif (89 %, 72 %, 81 %) |
| Le coût de 85 000 € de la reco 2 | Toute la section « Difficultés rencontrées » |
| Les dates de recrutement | Le décalage de recrutement et sa cause |
| La satisfaction chat 4,3/5 | La comparaison 3,8 (tel) et 3,6 (email) |

**Les arbitrages sont cohérents avec la consigne.** Le prompt demandait trois choses — objectifs, résultats, recommandations — et le modèle a coupé ce qui n'entrait dans aucune : les moyens, les difficultés, le contexte.

Une observation intéressante : il a gardé le **34 %** de résolution des problèmes techniques et le **22 %** de contacts concernés, en écartant les trois autres lignes du tableau. C'est le bon choix — ce sont les deux chiffres qui justifient la recommandation n° 2, donc les seuls qui portent une décision.

### Une omission discutable

La section 4 « Difficultés rencontrées » a entièrement disparu, y compris le décalage de recrutement qui explique la contre-performance de juillet. Pour un comité de direction — destinataire annoncé dans le prompt — cette information est utile : elle distingue un échec structurel d'un échec conjoncturel.

**Ce n'est pas une faute du modèle**, c'est une lacune du prompt : les trois intertitres imposés ne prévoyaient pas de rubrique pour les difficultés. Le modèle a respecté la structure demandée.

Correction possible : ajouter un quatrième intertitre « Difficultés », ou élargir la consigne « Résultats » à « Résultats et facteurs explicatifs ».

### Ce que cette tâche établit

**1. Le conflit longueur / exhaustivité se règle par la hiérarchisation, pas par la troncature.** Le modèle n'a pas résumé en coupant la fin : il a sélectionné par pertinence au regard des trois rubriques demandées.

**2. Une contrainte anti-complaisance est nécessaire et suffisante.** L'instruction « ne présente pas un résultat partiel comme un succès » a produit deux mentions explicites de non-atteinte. C'est le même mécanisme que « cause non précisée dans les avis » en Partie 3 : **une formule à produire bat une interdiction abstraite.**

**3. La structure imposée détermine ce qui survit.** Tout ce qui n'entrait pas dans les trois rubriques a disparu. Choisir les intertitres d'un résumé, c'est choisir ce que le lecteur ne lira pas.

---

## 5.2 — Traduction français → anglais

**Prompt :** voir [`prompts.md`](prompts.md#52--traduction-français--anglais)
**Source :** section 3.2 du [rapport trimestriel](../data/rapport-trimestriel.md)

![Résultat de la traduction](captures/02-traduction.png)

**Réponse obtenue (intégrale) :**

> ### 3.2 First Contact Resolution
>
> The first contact resolution rate reached **68%**, compared with 61% in the previous quarter. The target of 75% was not achieved.
>
> The analysis by contact reason reveals a significant gap:
>
> | Reason | Resolution rate |
> |---|---|
> | Order tracking | 89% |
> | Return and refund | 72% |
> | Mobile application technical issue | 34% |
> | Product question | 81% |
>
> Technical issues related to the mobile application are the main obstacle. They account for 22% of contacts and almost always require escalation to the technical team, whose average processing time is four business days.

**Observations :**

| Critère | Constat |
|---|---|
| Structure conservée | ✅ titre, 2 paragraphes, tableau 4 lignes, paragraphe final |
| Aucun commentaire ajouté | ✅ ni préambule, ni note du traducteur |
| Chiffres à l'identique | ✅ 68, 61, 75, 89, 72, 34, 81, 22, quatre |
| Format adapté | ✅ `68 %` → `68%` (convention anglaise, sans espace) |
| Termes consacrés | ✅ voir ci-dessous |
| Aucune phrase omise | ✅ correspondance phrase à phrase |
| Ajout d'information | ⚠️ une déviation, voir ci-dessous |

### Les termes métier sont correctement rendus

C'est le point le plus délicat de la tâche, et il est réussi :

| Français | Traduction produite | Commentaire |
|---|---|---|
| taux de résolution au premier contact | **first contact resolution rate** | ✅ terme consacré (FCR), pas une traduction littérale |
| motif de contact | **contact reason** | ✅ usage courant en centre de relation client |
| escalade vers l'équipe technique | **escalation to the technical team** | ✅ terme consacré |
| jours ouvrés | **business days** | ✅ correct — *working days* aurait été acceptable, *open days* aurait été une faute |
| délai de traitement moyen | **average processing time** | ✅ |
| suivi de commande | **order tracking** | ✅ |
| retour et remboursement | **return and refund** | ✅ |

Une traduction littérale aurait produit *« rate of resolution at the first contact »* — compréhensible mais non idiomatique. Le modèle a mobilisé le vocabulaire métier anglophone, ce que la contrainte « équivalent anglais consacré » demandait explicitement.

Le titre de section a également été adapté : « Résolution au premier contact » → « First Contact Resolution », avec les majuscules de titre anglaises. C'est une adaptation de convention, pas une modification de sens.

### La déviation : une explicitation dans le tableau

| Français | Anglais |
|---|---|
| Problème technique application | Mobile **application** technical issue |

Le français dit « Problème technique application » — l'adjectif *mobile* n'y figure pas. Le modèle l'a ajouté.

**L'ajout est factuellement correct** : le paragraphe suivant précise bien qu'il s'agit de l'application mobile. Le modèle a donc utilisé le contexte pour lever une ellipse.

**Mais il enfreint la contrainte** « n'ajoute aucune information ». Dans un tableau de reporting, cette ligne est un libellé d'indicateur : si ce libellé sert de clé de rapprochement avec un système source, l'ajout casse la correspondance.

C'est exactement le comportement que les quatre contraintes visaient — **la tentation d'améliorer**. Le modèle a produit un texte *meilleur* que le source, et c'est précisément ce qu'on ne voulait pas.

### Ce que cette tâche établit

**1. La contrainte de non-ajout est la plus difficile à tenir.** Les contraintes de structure, de chiffres et de non-résumé ont été respectées intégralement. La seule déviation porte sur l'ajout — et elle est *bien intentionnée*, ce qui la rend difficile à détecter en relecture rapide.

**2. Une ellipse du texte source est un point de fragilité.** Partout où le français est elliptique, le modèle est tenté de compléter. Pour une traduction strictement fidèle, il faudrait une contrainte plus spécifique : *« si le texte source est elliptique, conserve l'ellipse ; ne complète pas depuis le contexte. »*

**3. La qualité terminologique justifie l'usage d'un LLM plutôt qu'une traduction automatique classique.** Le passage de « taux de résolution au premier contact » à *first contact resolution rate* suppose de reconnaître un concept métier, pas seulement de traduire des mots. C'est le gain réel sur cette tâche.

# Partie 5 — Les cinq prompts métier

**Protocole :** une conversation neuve par prompt. Les cinq tâches sont indépendantes.

---

## 5.1 — Résumé de document

*Contraintes : 250 mots max, faits conservés, objectifs / résultats / recommandations identifiés, aucune invention.*

```text
Tu es analyste chargé de produire des synthèses de documents internes pour un comité de direction.

Tâche : résumer le document fourni.

Ton résumé doit identifier explicitement, sous trois intertitres :
- **Objectifs** : ce que le document annonce comme cibles
- **Résultats** : ce qui a été effectivement obtenu, avec les chiffres clés
- **Recommandations** : ce que le document préconise

Contraintes :
- 250 mots maximum, intertitres inclus
- conserve les informations factuelles : chiffres, dates, montants, taux
- n'invente aucune information, aucun chiffre, aucune cause
- si un objectif n'est pas atteint, dis-le explicitement ; ne présente pas un résultat partiel comme un succès
- n'ajoute aucun commentaire, aucune opinion ni aucune recommandation qui ne figure pas dans le document

Ton : factuel et neutre.

Document à résumer :
<<<
{document}
>>>
```

**Hypothèse.** Le conflit entre « 250 mots » et « conserver les faits » obligera à sacrifier des chiffres. Point de vigilance : le modèle retiendra-t-il que deux objectifs sur trois **ne sont pas atteints**, ou lissera-t-il en valorisant la progression ?

---

## 5.2 — Traduction français → anglais

*Contraintes : sens, structure et termes techniques conservés ; ni résumé ni ajout.*

```text
Tu es traducteur professionnel spécialisé dans les documents d'entreprise.

Tâche : traduire en anglais le texte français fourni.

Contraintes :
- conserve le sens exact, sans interprétation ni reformulation d'idées
- conserve la structure : mêmes paragraphes, mêmes titres, mêmes listes, mêmes tableaux, dans le même ordre
- conserve les termes techniques et métier en utilisant leur équivalent anglais consacré
- ne résume pas : chaque phrase du texte source doit avoir sa contrepartie
- n'ajoute aucune information, aucune explication, aucune note du traducteur
- conserve les chiffres, dates et montants à l'identique, en adaptant uniquement le format aux conventions anglaises

Ne produis que la traduction, sans commentaire avant ni après.

Texte à traduire :
<<<
{texte}
>>>
```

**Texte à traduire** — la section 3.2 du [rapport trimestriel](../data/rapport-trimestriel.md) :

> ### 3.2 Résolution au premier contact
>
> Le taux de résolution au premier contact atteint **68 %**, contre 61 % au trimestre précédent. L'objectif de 75 % n'est pas atteint.
>
> L'analyse par motif de contact révèle un écart important :
>
> | Motif | Taux de résolution |
> |---|---|
> | Suivi de commande | 89 % |
> | Retour et remboursement | 72 % |
> | Problème technique application | 34 % |
> | Question produit | 81 % |
>
> Les problèmes techniques liés à l'application mobile constituent le principal frein. Ils représentent 22 % des contacts et nécessitent presque toujours une escalade vers l'équipe technique, dont le délai de traitement moyen est de quatre jours ouvrés.

**Hypothèse.** Le risque principal est la **tentation d'améliorer** : fluidifier, réorganiser, expliciter. Points à vérifier : le tableau est-il conservé tel quel ? « taux de résolution au premier contact » devient-il *first contact resolution rate* (terme consacré) ou une traduction littérale ?

---

## 5.3 — Classification de ticket informatique

*Sortie JSON avec `categorie` et `justification`.*

```text
Tu es un système de tri automatique des tickets du support informatique interne.

Tâche : classer le ticket fourni dans une catégorie.

Catégories autorisées :
- "reseau" : connectivité, VPN, wifi, lenteur réseau, accès à Internet
- "logiciel" : application qui plante, bug, erreur logicielle, mise à jour
- "materiel" : panne physique, écran, clavier, imprimante, batterie
- "securite" : phishing, virus, comportement suspect, fuite de données
- "acces" : mot de passe, compte bloqué, droits insuffisants, authentification
- "autre" : tout ticket ne relevant d'aucune catégorie ci-dessus

Règle de décision : classe selon la cause probable du problème, pas selon son symptôme. Si le ticket décrit un symptôme compatible avec plusieurs catégories, retiens celle qui détermine l'équipe à saisir.

Format de sortie — JSON valide, rien d'autre, aucun bloc de code :
{
  "categorie": "<une des six valeurs autorisées>",
  "justification": "une phrase citant l'élément du ticket qui motive ce choix"
}

Contraintes :
- "categorie" vaut exactement une des six valeurs autorisées
- n'invente aucune catégorie
- la justification cite un élément effectivement présent dans le ticket

Ticket à classer :
<<<
Depuis ce matin je n'arrive plus à me connecter au serveur de fichiers partagés.
Mon collègue du même bureau y accède sans problème. J'ai redémarré mon poste deux fois.
Message affiché : "Échec de l'authentification, vérifiez vos identifiants."
>>>
```

**Hypothèse.** Le ticket est **volontairement ambigu** : il mentionne un serveur (`reseau`), un poste (`materiel`) et un échec d'authentification (`acces`). La règle « classe selon la cause, pas le symptôme » et l'indice « le collègue y accède sans problème » devraient orienter vers `acces`. C'est le test de la règle de décision.

---

## 5.4 — Extraction de données de facture

*JSON valide, `null` si une information est absente.*

```text
Tu es un système d'extraction de données comptables.

Tâche : extraire les informations de la facture fournie.

Champs à extraire :
- "numero_facture" (chaîne) : le numéro de la facture
- "date" (chaîne, format AAAA-MM-JJ) : la date d'émission de la facture
- "client" (chaîne) : le nom du client destinataire de la facture
- "montant_ht" (nombre) : le montant total hors taxes
- "tva" (nombre) : le montant de la TVA
- "montant_ttc" (nombre) : le montant total toutes taxes comprises

Règles d'extraction :
- retourne null pour tout champ dont l'information n'est pas présente dans la facture
- n'invente jamais une valeur ; ne la déduis pas d'un calcul si elle n'est pas écrite, sauf mention contraire ci-dessous
- le client est le destinataire de la facture, pas l'émetteur
- si plusieurs dates figurent, retiens la date d'émission
- les montants sont des nombres décimaux, sans symbole monétaire ni séparateur de milliers
- si la facture mentionne une franchise ou une non-application de TVA, "tva" vaut 0

Format de sortie : JSON valide, rien d'autre, aucun bloc de code, exactement ces six champs.

Facture :
<<<
{facture}
>>>
```

**Hypothèse.** La facture A teste la lecture (quatre pièges : deux dates, deux entités, séparateurs français, référence de commande). La facture B teste l'honnêteté : **le numéro est absent**, et un modèle non contraint risque d'en fabriquer un.

La règle sur la franchise de TVA a été ajoutée pour trancher l'ambiguïté `0` / `null` relevée dans le [jeu de test](../data/facture.md) — sans elle, les deux réponses seraient défendables.

---

## 5.5 — Rédaction d'un email client

*Objectifs, ton, 150 mots maximum.*

```text
Tu es conseiller au service client d'une entreprise de e-commerce.

Tâche : rédiger l'email adressé à un client dont la livraison a pris du retard.

Situation connue — ce sont les seules informations dont tu disposes :
- commande passée le 3 octobre
- délai annoncé à la commande : 48 heures
- colis reçu le 12 octobre, soit neuf jours plus tard
- le client a relancé deux fois par email sans obtenir de réponse

Objectifs de l'email :
1. reconnaître le retard
2. présenter des excuses
3. expliquer la situation à partir des seuls éléments connus
4. proposer une solution concrète

Contraintes :
- 150 mots maximum, objet inclus
- n'invente aucune cause au retard : tu ne connais pas son origine. N'écris ni "pic d'activité", ni "problème transporteur", ni aucune explication non fournie ci-dessus
- si tu ne peux pas expliquer la cause, dis que la cause est en cours d'analyse plutôt que d'en supposer une
- n'invente aucun geste commercial chiffré qui ne serait pas de ton ressort ; propose une solution, ne l'engage pas au nom de l'entreprise sans réserve
- ne minimise pas le retard et ne rejette la faute sur personne

Ton : professionnel, courtois et rassurant.

Format : un objet d'email, puis le corps du message.
```

**Hypothèse.** C'est la seule tâche générative, et la contrainte « expliquer sans inventer de cause » est en **tension interne** : l'objectif 3 demande d'expliquer, la contrainte interdit la cause. Le comportement attendu est de décrire ce qui est su et de qualifier la cause d'inconnue.

C'est aussi le test le plus direct de l'acquis de la Partie 3 : donner une formule à produire (« cause en cours d'analyse ») fonctionne mieux qu'une interdiction seule.

---

## Grille d'observation

| Tâche | Contrainte de forme | Fidélité | Complétude | Invention | Exploitabilité |
|---|---|---|---|---|---|
| 5.1 Résumé | ≤ 250 mots | | | | |
| 5.2 Traduction | structure identique | | | | |
| 5.3 Ticket | JSON, 6 catégories | | | | |
| 5.4 Facture | JSON, 6 champs | | | | |
| 5.5 Email | ≤ 150 mots | | | | |

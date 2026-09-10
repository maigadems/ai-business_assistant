# Jeu d'avis clients

Jeu de données servant de support aux Parties 1 à 3 de l'atelier.

Les avis sont fictifs et rédigés pour couvrir plusieurs cas de figure utiles :

- plusieurs **thèmes** récurrents (livraison, application mobile, prix, SAV, qualité produit) ;
- des avis **clairement positifs** et **clairement négatifs**, pour vérifier le cas simple ;
- des avis **ambigus** (A03, A07) qui mélangent un point positif et un point négatif dans la même phrase — ils révèlent si le prompt force un choix ou autorise la nuance ;
- un avis **hors-sujet** (A10), qui teste la présence d'une catégorie « Autre » ;
- un avis **très court** (A09), qui teste le comportement du modèle quand l'information est pauvre.

---

## Avis

**A01** — « Commande passée le 3, reçue le 12. Neuf jours pour un article annoncé en 48h, c'est inadmissible. J'ai relancé deux fois sans réponse. »

**A02** — « Produit conforme à la description, emballage soigné. Je recommande. »

**A03** — « Le service est rapide mais l'application plante régulièrement dès que je veux consulter mon historique. »

**A04** — « Prix vraiment élevé par rapport à la concurrence pour une qualité équivalente. Je ne renouvellerai pas. »

**A05** — « J'ai contacté le support par chat, on m'a répondu en moins de 5 minutes et le problème a été réglé dans la foulée. Bravo. »

**A06** — « Impossible de finaliser ma commande sur mobile, l'application se ferme au moment du paiement. J'ai dû passer par un ordinateur. »

**A07** — « Livraison très rapide, deux jours seulement. Dommage que l'article soit arrivé avec une rayure sur le côté. »

**A08** — « Troisième commande chez eux, toujours aussi satisfait. Les délais sont tenus et le suivi est clair. »

**A09** — « Correct. »

**A10** — « Est-ce que vous ouvrez une boutique à Bordeaux ? Je n'ai pas trouvé l'information sur le site. »

---

## Répartition attendue

Cette répartition sert de **référence** pour évaluer les réponses du LLM dans les Parties 1 à 3.
Elle est établie manuellement, avant toute exécution de prompt.

| Thème | Avis concernés | Sentiment dominant |
|---|---|---|
| Livraison | A01, A07, A08 | mitigé (A01 négatif, A07 et A08 positifs sur le délai) |
| Application mobile | A03, A06 | négatif |
| Prix | A04 | négatif |
| Service après-vente | A01, A05 | mitigé (A01 négatif, A05 positif) |
| Qualité produit | A02, A07 | mitigé (A02 positif, A07 négatif sur l'état à réception) |
| Autre / hors-sujet | A09, A10 | neutre |

**Points d'attention :**

- A01 et A07 relèvent chacun de **deux thèmes** : un prompt qui impose un thème unique par avis produira un décompte incomplet.
- A03 et A07 sont les cas où le sentiment global est réellement **mitigé** ; un prompt qui n'autorise que positif/négatif/neutre forcera un choix arbitraire.
- A10 n'est pas un avis mais une question : il ne devrait alimenter aucun thème de satisfaction.

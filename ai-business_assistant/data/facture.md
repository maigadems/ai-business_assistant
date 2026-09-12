# Factures de test — Partie 5 (extraction)

Deux factures fictives servant à tester le prompt d'extraction structurée.

---

## Facture A — cas complet

Cette facture contient toutes les informations demandées. Elle sert de cas nominal.

```text
                                              SARL DUBOIS ÉQUIPEMENT
                                              12 rue des Ateliers
                                              44000 NANTES
                                              SIRET 412 785 963 00028
                                              TVA FR 41 412785963

                        FACTURE N° FA-2025-0847

Date d'émission : 14 octobre 2025
Date d'échéance : 13 novembre 2025

Client :
    MAISON BERGER SAS
    27 avenue de la République
    59000 LILLE

Référence commande : CMD-2025-3391

------------------------------------------------------------------
Désignation                      Qté    P.U. HT      Total HT
------------------------------------------------------------------
Établi métallique 180 cm           2     420,00 €      840,00 €
Servante d'atelier 7 tiroirs       1     315,50 €      315,50 €
Jeu de clés mixtes 12 pièces       4      48,90 €      195,60 €
Livraison et installation          1     120,00 €      120,00 €
------------------------------------------------------------------
                                        Total HT      1 471,10 €
                                        TVA 20 %        294,22 €
                                        TOTAL TTC     1 765,32 €
------------------------------------------------------------------

Conditions de règlement : virement à 30 jours.
Pénalités de retard : 3 fois le taux d'intérêt légal.
```

**Extraction attendue :**

| Champ | Valeur |
|---|---|
| `numero_facture` | `FA-2025-0847` |
| `date` | `14 octobre 2025` (ou `2025-10-14`) |
| `client` | `MAISON BERGER SAS` |
| `montant_ht` | `1471.10` |
| `tva` | `294.22` |
| `montant_ttc` | `1765.32` |

**Pièges volontaires :**

- Deux dates figurent sur la facture (émission et échéance) : le modèle doit retenir la date d'émission.
- Deux entités sont nommées : l'émetteur (SARL DUBOIS ÉQUIPEMENT, en en-tête) et le client (MAISON BERGER SAS). Une confusion est possible.
- Les montants utilisent l'espace comme séparateur de milliers et la virgule comme séparateur décimal. Le JSON attend un nombre au format anglo-saxon.
- Une référence de commande (`CMD-2025-3391`) peut être confondue avec le numéro de facture.

---

## Facture B — cas dégradé

Cette facture est **incomplète** : le numéro de facture est absent et le montant de TVA n'est pas détaillé. Elle sert à tester la consigne « retourner `null` si une information est absente ».

```text
                                              ATELIER GRAPHIQUE LUMEN
                                              8 impasse Saint-Michel
                                              33000 BORDEAUX

                        FACTURE

Émise le 02/11/2025

Destinataire : Cabinet VERNET & Associés

------------------------------------------------------------------
Prestation                                          Montant
------------------------------------------------------------------
Refonte identité visuelle                         2 800,00 €
Déclinaison papeterie                               650,00 €
------------------------------------------------------------------
                                    Total à payer   3 450,00 €
------------------------------------------------------------------

TVA non applicable, article 293 B du CGI.
Règlement à réception.
```

**Extraction attendue :**

| Champ | Valeur | Justification |
|---|---|---|
| `numero_facture` | `null` | Aucun numéro n'est indiqué |
| `date` | `02/11/2025` (ou `2025-11-02`) | Présente |
| `client` | `Cabinet VERNET & Associés` | Présent |
| `montant_ht` | `3450.00` | Le total est HT puisque la TVA n'est pas applicable |
| `tva` | `0` ou `null` | **Cas discutable** — voir ci-dessous |
| `montant_ttc` | `3450.00` | Égal au HT en franchise de TVA |

**Pièges volontaires :**

- **Le numéro de facture est absent** : c'est le test principal de la consigne `null`.
- **La TVA n'est pas applicable** (article 293 B, franchise en base). Faut-il retourner `0` — la TVA vaut zéro — ou `null` — l'information n'est pas fournie ? Les deux réponses se défendent : c'est précisément le genre d'ambiguïté qu'un prompt d'extraction doit trancher explicitement.
- Le montant est présenté comme « Total à payer » sans mention HT ou TTC. Le modèle doit déduire de la mention de franchise que HT = TTC.
- La date est au format `JJ/MM/AAAA`, différent du format littéral de la facture A.

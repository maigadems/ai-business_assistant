# Contexte dataset à fournir au LLM

Ce bloc est celui qu'on colle dans les prompts à la place de `{contexte_dataset}`.

Il correspond à ce qu'un analyste obtient réellement avec `df.info()`, `df.describe()`, `df.isna().sum()` et `df['col'].value_counts()` — **pas** au fichier complet. Coller 11 070 lignes dans un LLM n'est ni possible ni souhaitable : le cas d'usage réaliste est de fournir un profil statistique et de demander une interprétation.

---

```text
DATASET : capteurs_batiment.csv
Relevés horaires de capteurs sur 5 zones d'un bâtiment tertiaire.
Période : 1er janvier au 31 mars 2025 (90 jours).
11 070 lignes, 9 colonnes.

OBJECTIF MÉTIER : comprendre puis prédire la consommation énergétique du bâtiment.
VARIABLE CIBLE : consommation_kwh

SCHÉMA DES COLONNES
id_releve                  entier      identifiant du relevé
horodatage                 datetime    date et heure du relevé
zone                       texte       zone du bâtiment
temperature_interieure_c   décimal     température intérieure en °C
temperature_exterieure_c   décimal     température extérieure en °C
humidite_pct               décimal     humidité relative en %
occupation_personnes       entier      nombre de personnes présentes
type_jour                  texte       ouvré / weekend / férié
consommation_kwh           décimal     consommation en kWh (CIBLE)

EXTRAIT (8 premières lignes)
id_releve,horodatage,zone,temperature_interieure_c,temperature_exterieure_c,humidite_pct,occupation_personnes,type_jour,consommation_kwh
10676,2025-03-30 23:00:00,BUREAU NORD,21.01,4.89,44.5,0,weekend,10.732
10061,2025-03-25 20:00:00,Bureau_Nord,20.29,6.76,38.5,9,ouvré,9.95
3217,2025-01-27 19:00:00,Bureau_Sud,19.59,4.73,38.6,10,ouvré,11.868
2726,2025-01-23 17:00:00,BUREAU NORD,21.2,3.29,45.2,9,ouvré,14.605
6683,2025-02-25 16:00:00,Atelier,21.34,7.84,37.1,1,ouvré,27.616
10305,2025-03-27 20:00:00,Accueil,21.94,8.12,43.8,7,ouvré,7.094
5897,2025-02-19 03:00:00,Bureau_Sud,21.17,0.34,,4,ouvré,11.19
2779,2025-01-24 03:00:00,Salle_Serveur,20.97,-0.2,60.6,0,ouvré,45.805

VALEURS MANQUANTES (df.isna().sum())
humidite_pct                681   (6.15 %)
occupation_personnes        527   (4.76 %)
temperature_interieure_c    342   (3.09 %)
consommation_kwh            188   (1.70 %)
type_jour                    98   (0.89 %)
les 4 autres colonnes         0

LIGNES DUPLIQUÉES
lignes strictement identiques                 183
couples (horodatage, zone) apparaissant >1x   270
valeurs de id_releve apparaissant >1x         270

STATISTIQUES NUMÉRIQUES (df.describe())
                          count      min       max      mean      std       q1    median       q3
temperature_interieure_c  10728  -999.00     24.01    15.108   77.325    20.45     21.00    21.55
temperature_exterieure_c  11070    -5.38     13.90     3.757    3.575     0.98      3.70     6.32
humidite_pct              10389    23.30    317.40    45.580   12.815    40.80     44.90    49.00
occupation_personnes      10543     0.00     22.00     4.286    4.753     0.00      3.00     8.00
consommation_kwh          10882   -39.47    898.52    27.270   71.733    10.29     13.06    24.87

MODALITÉS DE zone (df['zone'].value_counts())
Salle_Serveur    1160
bureau sud       1151
atelier          1148
accueil          1135
Accueil          1075
Atelier          1073
Bureau_Sud       1070
Salle Serveur    1042
BUREAU NORD       759
Bureau_Nord       743
bureau_nord       714

MODALITÉS DE type_jour (df['type_jour'].value_counts())
ouvré      7670
weekend    3181
férié       121
(vide)       98
```

---

## Ce que ce contexte contient, et qui sert de grille de correction

Les éléments ci-dessous sont **volontairement présents** dans le profil. La question 6.1 évalue lesquels le modèle détecte et interprète correctement.

| Indice visible dans le contexte | Ce qu'il doit déclencher |
|---|---|
| `temperature_interieure_c` : min = **-999**, mean 15,1 mais median 21,0, std **77,3** | Reconnaître une **valeur sentinelle**, pas un outlier statistique |
| `humidite_pct` : max = **317,4** | Borne physique dépassée (max 100 %) |
| `consommation_kwh` : min = **-39,47** | Valeur négative impossible sur une consommation |
| `consommation_kwh` : mean 27,27 vs median 13,06, std 71,7 | **Distribution fortement asymétrique** → imputer par la moyenne serait une faute ; la médiane s'impose |
| `consommation_kwh` : 188 manquantes | C'est la **cible** — supprimer ces lignes, ne jamais les imputer |
| 183 vs 270 doublons | Écart = **quasi-doublons**, invisibles à une déduplication exacte |
| 11 modalités de `zone` | Variantes de casse et séparateur → **5 zones réelles** |
| `type_jour` avec 98 valeurs vides | Manquant déguisé en modalité |
| `horodatage` horaire sur 90 jours | Structure **temporelle** : interdit un split aléatoire train/test |

Le dernier point n'est pas un défaut du dataset mais une contrainte méthodologique. Il est signalé ici car il départage un conseil générique d'un conseil adapté : recommander une validation croisée classique sur une série temporelle est une **fuite de données**.

"""
Profile le dataset des capteurs sans dépendance externe (stdlib uniquement).

Produit les chiffres réels cités dans la Partie 6 : taux de valeurs manquantes,
doublons, valeurs aberrantes, cardinalité des variables catégorielles.

Le but est que la documentation de l'atelier s'appuie sur des mesures réelles
et non sur des ordres de grandeur inventés.

Usage :
    python scripts/profiler_dataset.py
"""

import csv
import json
from collections import Counter
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
ENTREE = RACINE / "data" / "capteurs_batiment.csv"
SORTIE = RACINE / "resultats" / "profil_dataset_capteurs.json"

COLONNES_NUMERIQUES = [
    "temperature_interieure_c",
    "temperature_exterieure_c",
    "humidite_pct",
    "occupation_personnes",
    "consommation_kwh",
]


def quantile(valeurs_triees: list[float], q: float) -> float:
    """Quantile par interpolation linéaire (méthode 7, comme numpy par défaut)."""
    if not valeurs_triees:
        return float("nan")
    position = (len(valeurs_triees) - 1) * q
    bas = int(position)
    haut = min(bas + 1, len(valeurs_triees) - 1)
    poids = position - bas
    return valeurs_triees[bas] * (1 - poids) + valeurs_triees[haut] * poids


def moyenne(valeurs: list[float]) -> float:
    return sum(valeurs) / len(valeurs) if valeurs else float("nan")


def ecart_type(valeurs: list[float]) -> float:
    if len(valeurs) < 2:
        return float("nan")
    m = moyenne(valeurs)
    return (sum((v - m) ** 2 for v in valeurs) / (len(valeurs) - 1)) ** 0.5


def main() -> None:
    with ENTREE.open(encoding="utf-8") as f:
        lignes = list(csv.DictReader(f))

    n = len(lignes)
    rapport: dict = {
        "fichier": str(ENTREE.relative_to(RACINE)).replace("\\", "/"),
        "nb_lignes": n,
        "nb_colonnes": len(lignes[0]) if lignes else 0,
    }

    # --- Valeurs manquantes -------------------------------------------------
    manquants = {}
    for colonne in lignes[0]:
        nb = sum(1 for ligne in lignes if ligne[colonne].strip() == "")
        if nb:
            manquants[colonne] = {"nb": nb, "taux_pct": round(100 * nb / n, 2)}
    rapport["valeurs_manquantes"] = manquants

    # --- Doublons -----------------------------------------------------------
    lignes_completes = Counter(tuple(sorted(ligne.items())) for ligne in lignes)
    nb_doublons_stricts = sum(c - 1 for c in lignes_completes.values() if c > 1)

    cles_metier = Counter((ligne["horodatage"], ligne["zone"]) for ligne in lignes)
    nb_doublons_metier = sum(c - 1 for c in cles_metier.values() if c > 1)

    ids = Counter(ligne["id_releve"] for ligne in lignes)
    nb_ids_dupliques = sum(c - 1 for c in ids.values() if c > 1)

    rapport["doublons"] = {
        "lignes_strictement_identiques": nb_doublons_stricts,
        "doublons_cle_metier_horodatage_zone": nb_doublons_metier,
        "id_releve_dupliques": nb_ids_dupliques,
        "commentaire": (
            "L'écart entre doublons stricts et doublons de clé métier correspond aux "
            "quasi-doublons : même horodatage et même zone, mais mesures légèrement "
            "différentes. Ils ne sont pas détectables par une simple déduplication exacte."
        ),
    }

    # --- Statistiques numériques et valeurs aberrantes ----------------------
    stats = {}
    for colonne in COLONNES_NUMERIQUES:
        valeurs = []
        for ligne in lignes:
            brut = ligne[colonne].strip()
            if brut == "":
                continue
            try:
                valeurs.append(float(brut))
            except ValueError:
                continue

        if not valeurs:
            continue

        triees = sorted(valeurs)
        q1 = quantile(triees, 0.25)
        q3 = quantile(triees, 0.75)
        iqr = q3 - q1
        borne_basse = q1 - 1.5 * iqr
        borne_haute = q3 + 1.5 * iqr
        hors_bornes = [v for v in valeurs if v < borne_basse or v > borne_haute]

        stats[colonne] = {
            "nb_valeurs": len(valeurs),
            "min": round(min(valeurs), 3),
            "max": round(max(valeurs), 3),
            "moyenne": round(moyenne(valeurs), 3),
            "ecart_type": round(ecart_type(valeurs), 3),
            "q1": round(q1, 3),
            "mediane": round(quantile(triees, 0.5), 3),
            "q3": round(q3, 3),
            "outliers_iqr": {
                "nb": len(hors_bornes),
                "taux_pct": round(100 * len(hors_bornes) / len(valeurs), 2),
                "borne_basse": round(borne_basse, 3),
                "borne_haute": round(borne_haute, 3),
            },
        }

    # Anomalies physiquement impossibles, repérables par règle métier.
    stats["consommation_kwh"]["valeurs_negatives"] = sum(
        1 for l in lignes if l["consommation_kwh"].strip() not in ("",) and float(l["consommation_kwh"]) < 0
    )
    stats["temperature_interieure_c"]["sentinelle_-999"] = sum(
        1 for l in lignes if l["temperature_interieure_c"].strip() == "-999"
    )
    stats["humidite_pct"]["hors_plage_0_100"] = sum(
        1
        for l in lignes
        if l["humidite_pct"].strip() != "" and not (0 <= float(l["humidite_pct"]) <= 100)
    )
    rapport["statistiques_numeriques"] = stats

    # --- Variables catégorielles -------------------------------------------
    categorielles = {}
    for colonne in ["zone", "type_jour"]:
        compte = Counter(ligne[colonne] for ligne in lignes)
        normalise = Counter(ligne[colonne].strip().lower().replace(" ", "_") for ligne in lignes)
        categorielles[colonne] = {
            "cardinalite_brute": len(compte),
            "cardinalite_apres_normalisation": len(normalise),
            "modalites_brutes": dict(sorted(compte.items(), key=lambda kv: -kv[1])),
        }
    rapport["variables_categorielles"] = categorielles

    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(json.dumps(rapport, indent=2, ensure_ascii=False), encoding="utf-8")

    # Résumé lisible en console.
    print(f"Lignes            : {n}")
    print(f"Doublons stricts  : {nb_doublons_stricts}")
    print(f"Doublons métier   : {nb_doublons_metier}")
    print("Valeurs manquantes:")
    for col, info in sorted(manquants.items(), key=lambda kv: -kv[1]["nb"]):
        print(f"  {col:30s} {info['nb']:5d}  ({info['taux_pct']} %)")
    print("Cardinalité catégorielles:")
    for col, info in categorielles.items():
        print(
            f"  {col:12s} brute={info['cardinalite_brute']} "
            f"normalisée={info['cardinalite_apres_normalisation']}"
        )
    print(f"\nRapport complet : {SORTIE}")


if __name__ == "__main__":
    main()

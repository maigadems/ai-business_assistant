"""
Génère le dataset des capteurs utilisé dans la Partie 6 (Prompt Engineering pour le ML).

Le dataset est volontairement "sale" : il contient des valeurs manquantes, des
doublons, des valeurs aberrantes et des variables catégorielles mal normalisées.
C'est ce qui donne de la matière aux prompts de la Partie 6.

Le générateur est déterministe (seed fixe) : réexécuter le script reproduit
exactement le même fichier CSV.

Usage :
    python scripts/generer_dataset_capteurs.py
"""

import csv
import math
import random
from datetime import datetime, timedelta
from pathlib import Path

SEED = 42
N_HEURES = 24 * 90  # 90 jours de relevés horaires
DEBUT = datetime(2025, 1, 1, 0, 0)
SORTIE = Path(__file__).resolve().parent.parent / "data" / "capteurs_batiment.csv"

# Variantes non normalisées volontaires : le nettoyage des catégorielles
# fait partie de ce que le LLM doit détecter (Partie 6.1).
ZONES = ["Bureau_Nord", "Bureau_Sud", "Atelier", "Salle_Serveur", "Accueil"]
VARIANTES_ZONE = {
    "Bureau_Nord": ["Bureau_Nord", "bureau_nord", "BUREAU NORD"],
    "Bureau_Sud": ["Bureau_Sud", "bureau sud"],
    "Atelier": ["Atelier", "atelier"],
    "Salle_Serveur": ["Salle_Serveur", "Salle Serveur"],
    "Accueil": ["Accueil", "accueil "],  # espace final volontaire
}
TYPES_JOUR = ["ouvré", "weekend", "férié"]


def consommation_attendue(horodatage: datetime, zone: str, temp_ext: float) -> float:
    """Modèle physique simplifié : base + effet horaire + effet thermique."""
    base = {
        "Bureau_Nord": 12.0,
        "Bureau_Sud": 14.0,
        "Atelier": 28.0,
        "Salle_Serveur": 40.0,
        "Accueil": 8.0,
    }[zone]

    heure = horodatage.hour
    weekend = horodatage.weekday() >= 5

    # La salle serveur tourne en continu, les autres zones suivent l'occupation.
    if zone == "Salle_Serveur":
        profil_horaire = 1.0
    elif weekend:
        profil_horaire = 0.25
    else:
        # Pic d'occupation entre 8h et 18h.
        profil_horaire = 0.2 + 0.8 * math.exp(-((heure - 13) ** 2) / 26)

    # Chauffage quand il fait froid, climatisation quand il fait chaud.
    effet_thermique = 0.45 * max(0.0, 18.0 - temp_ext) + 0.60 * max(0.0, temp_ext - 24.0)

    return base * profil_horaire + effet_thermique


def temperature_exterieure(horodatage: datetime, rng: random.Random) -> float:
    """Cycle saisonnier + cycle journalier + bruit."""
    jour_annee = horodatage.timetuple().tm_yday
    saisonnier = 10.0 - 8.0 * math.cos(2 * math.pi * (jour_annee - 15) / 365)
    journalier = 4.0 * math.sin(2 * math.pi * (horodatage.hour - 9) / 24)
    return round(saisonnier + journalier + rng.gauss(0, 1.2), 2)


def generer_lignes(rng: random.Random) -> list[dict]:
    lignes = []
    identifiant = 1

    for i in range(N_HEURES):
        horodatage = DEBUT + timedelta(hours=i)
        temp_ext = temperature_exterieure(horodatage, rng)

        for zone in ZONES:
            temp_int = round(21.0 + rng.gauss(0, 0.8), 2)
            humidite = round(45.0 + rng.gauss(0, 6.0), 1)
            occupation = 0 if horodatage.weekday() >= 5 else max(0, int(rng.gauss(8, 4)))
            if zone == "Salle_Serveur":
                occupation = 0

            conso = consommation_attendue(horodatage, zone, temp_ext)
            conso = round(max(0.0, conso + rng.gauss(0, 0.9)), 3)

            if horodatage.weekday() >= 5:
                type_jour = "weekend"
            elif horodatage.month == 1 and horodatage.day == 1:
                type_jour = "férié"
            else:
                type_jour = "ouvré"

            lignes.append(
                {
                    "id_releve": identifiant,
                    "horodatage": horodatage.strftime("%Y-%m-%d %H:%M:%S"),
                    "zone": rng.choice(VARIANTES_ZONE[zone]),
                    "temperature_interieure_c": temp_int,
                    "temperature_exterieure_c": temp_ext,
                    "humidite_pct": humidite,
                    "occupation_personnes": occupation,
                    "type_jour": type_jour,
                    "consommation_kwh": conso,
                }
            )
            identifiant += 1

    return lignes


def injecter_defauts(lignes: list[dict], rng: random.Random) -> list[dict]:
    """Injecte les défauts que les prompts de la Partie 6 doivent faire détecter."""
    n = len(lignes)

    # 1. Valeurs manquantes, à des taux différents selon la colonne.
    taux_manquants = {
        "humidite_pct": 0.062,
        "temperature_interieure_c": 0.031,
        "occupation_personnes": 0.048,
        "consommation_kwh": 0.017,
        "type_jour": 0.009,
    }
    for colonne, taux in taux_manquants.items():
        for idx in rng.sample(range(n), int(n * taux)):
            lignes[idx][colonne] = ""

    # 2. Valeurs aberrantes : capteur qui déraille (pics) et valeurs physiquement
    #    impossibles (négatives, sentinelle -999).
    for idx in rng.sample(range(n), 140):
        lignes[idx]["consommation_kwh"] = round(rng.uniform(300, 900), 3)
    for idx in rng.sample(range(n), 45):
        lignes[idx]["consommation_kwh"] = round(-rng.uniform(1, 40), 3)
    for idx in rng.sample(range(n), 60):
        lignes[idx]["temperature_interieure_c"] = -999
    for idx in rng.sample(range(n), 35):
        lignes[idx]["humidite_pct"] = round(rng.uniform(140, 320), 1)

    # 3. Doublons : lignes strictement identiques (id compris) et quasi-doublons
    #    (même horodatage + zone, mesures légèrement différentes).
    doublons = []
    for ligne in rng.sample(lignes, 180):
        doublons.append(dict(ligne))
    for ligne in rng.sample(lignes, 90):
        quasi = dict(ligne)
        if quasi["consommation_kwh"] not in ("", None):
            try:
                quasi["consommation_kwh"] = round(float(quasi["consommation_kwh"]) + rng.gauss(0, 0.05), 3)
            except (TypeError, ValueError):
                pass
        doublons.append(quasi)

    lignes.extend(doublons)
    rng.shuffle(lignes)
    return lignes


def main() -> None:
    rng = random.Random(SEED)
    lignes = generer_lignes(rng)
    lignes = injecter_defauts(lignes, rng)

    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    champs = [
        "id_releve",
        "horodatage",
        "zone",
        "temperature_interieure_c",
        "temperature_exterieure_c",
        "humidite_pct",
        "occupation_personnes",
        "type_jour",
        "consommation_kwh",
    ]
    with SORTIE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        writer.writerows(lignes)

    print(f"Dataset écrit : {SORTIE}")
    print(f"Lignes : {len(lignes)}")


if __name__ == "__main__":
    main()

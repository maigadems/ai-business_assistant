"""
Valide une sortie JSON du LLM contre les cinq règles de la Partie 4.

Ce script montre la différence entre *demander* un format dans un prompt et le
*garantir* : les règles écrites dans le prompt restent déclaratives, seul un
contrôle côté application peut rejeter une sortie non conforme.

Implémenté sans dépendance externe (pas de jsonschema) pour rester exécutable
partout. Le schéma formel équivalent est dans schema.json.

Usage :
    python valider.py                  # lance les cas de test
    python valider.py fichier.json     # valide un fichier
"""

import json
import sys

SENTIMENTS = ("positif", "negatif", "neutre")
CATEGORIES = ("livraison", "application", "prix", "sav", "produit", "autre")
URGENCES = ("faible", "moyenne", "elevee")
CHAMPS = ("sentiment", "categorie", "urgence", "probleme", "confiance")


def valider(brut):
    """Retourne la liste des violations. Liste vide = sortie conforme."""
    erreurs = []

    # Règle 1 — JSON valide, et rien d'autre
    try:
        data = json.loads(brut)
    except json.JSONDecodeError as e:
        return [f"regle 1 : JSON invalide ({e.msg} ligne {e.lineno})"]

    if not isinstance(data, dict):
        return ["regle 1 : la racine doit etre un objet JSON"]

    # Règle 2 — exactement les cinq champs, ni plus ni moins
    manquants = set(CHAMPS) - set(data)
    surplus = set(data) - set(CHAMPS)
    if manquants:
        erreurs.append(f"regle 2 : champs manquants {sorted(manquants)}")
    if surplus:
        erreurs.append(f"regle 2 : proprietes supplementaires {sorted(surplus)}")

    # Règle 3 — sentiment dans le domaine autorisé
    if "sentiment" in data and data["sentiment"] not in SENTIMENTS:
        erreurs.append(f"regle 3 : sentiment={data['sentiment']!r} hors domaine {SENTIMENTS}")

    # Règle 5 — urgence dans le domaine autorisé
    if "urgence" in data and data["urgence"] not in URGENCES:
        erreurs.append(f"regle 5 : urgence={data['urgence']!r} hors domaine {URGENCES}")

    # Règle 4 — confiance : nombre entre 0 et 1, pas une chaîne
    if "confiance" in data:
        c = data["confiance"]
        if isinstance(c, bool) or not isinstance(c, (int, float)):
            erreurs.append(f"regle 4 : confiance={c!r} n'est pas un nombre")
        elif not 0 <= c <= 1:
            erreurs.append(f"regle 4 : confiance={c} hors bornes [0, 1]")

    # Hors énoncé — categorie est énumérée dans le prompt, on la contrôle aussi
    if "categorie" in data and data["categorie"] not in CATEGORIES:
        erreurs.append(f"categorie={data['categorie']!r} hors domaine {CATEGORIES}")

    return erreurs


# Cas de test : les trois sorties réellement obtenues, puis des sorties
# non conformes que le prompt n'aurait pas empêchées.
CAS = [
    ("Q1 - sortie reelle", '{"sentiment":"negatif","categorie":"livraison","urgence":"elevee","probleme":"Livraison tres en retard.","confiance":0.99}', True),
    ("Q2 - sortie reelle minifiee", '{"sentiment":"negatif","categorie":"livraison","urgence":"elevee","probleme":"Retard important.","confiance":0.99}', True),
    ("Q3 - sortie reelle cas ambigu", '{"sentiment":"negatif","categorie":"application","urgence":"moyenne","probleme":"Plantages reguliers.","confiance":0.99}', True),
    ("sentiment hors domaine", '{"sentiment":"mitige","categorie":"application","urgence":"moyenne","probleme":"x","confiance":0.5}', False),
    ("confiance en chaine", '{"sentiment":"negatif","categorie":"application","urgence":"moyenne","probleme":"x","confiance":"0.9"}', False),
    ("propriete supplementaire", '{"sentiment":"negatif","categorie":"application","urgence":"moyenne","probleme":"x","confiance":0.9,"commentaire":"note"}', False),
    ("confiance hors bornes", '{"sentiment":"negatif","categorie":"application","urgence":"moyenne","probleme":"x","confiance":1.5}', False),
    ("bloc markdown autour", '```json\n{"sentiment":"negatif","categorie":"prix","urgence":"faible","probleme":"x","confiance":0.8}\n```', False),
    ("texte avant le JSON", 'Voici le resultat :\n{"sentiment":"negatif","categorie":"prix","urgence":"faible","probleme":"x","confiance":0.8}', False),
]


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            erreurs = valider(f.read())
        if erreurs:
            print("REJETE")
            for e in erreurs:
                print(f"  - {e}")
            return 1
        print("CONFORME")
        return 0

    echecs = 0
    for nom, brut, doit_passer in CAS:
        erreurs = valider(brut)
        conforme = not erreurs
        statut = "OK  " if conforme == doit_passer else "FAIL"
        if conforme != doit_passer:
            echecs += 1
        verdict = "conforme" if conforme else f"rejete ({erreurs[0]})"
        print(f"{statut} {nom:32} -> {verdict}")

    print()
    print(f"{len(CAS) - echecs}/{len(CAS)} cas de test passes")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())

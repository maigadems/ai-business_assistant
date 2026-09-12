"""
Mesure automatiquement les critères 1 à 4 de la grille d'évaluation (Partie 8).

Pourquoi un script plutôt qu'un comptage manuel : la Partie 6 a montré qu'une
valeur numérique produite sans vérification peut être fausse au milieu de
calculs justes. Compter 150 mots à la main sur six réponses est exactement le
genre de tâche où l'erreur passe inaperçue.

Les réponses sont lues depuis reponses/*.md, un fichier par exécution.

Usage :
    python mesurer.py
"""

import re
import sys
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parent
DOSSIER_REPONSES = RACINE / "reponses"
SOURCE = RACINE.parent / "data" / "rapport-trimestriel.md"

# Les huit chiffres de référence, définis dans README.md avant exécution.
# Chaque entrée : (libellé, liste de graphies acceptées).
CHIFFRES_CLES = [
    ("7 h 20 — délai trimestre", [r"7\s*h\s*20"]),
    ("6 heures — objectif délai", [r"6\s*(?:h\b|heures)"]),
    ("68 % — résolution", [r"68\s*%"]),
    ("75 % — objectif résolution", [r"75\s*%"]),
    ("9 septembre — déploiement chat", [r"9\s*septembre"]),
    ("34 % — résolution technique", [r"34\s*%"]),
    ("22 % — part contacts techniques", [r"22\s*%"]),
    ("85 000 € — coût recommandation", [r"85\s*000", r"85\s*k"]),
]

# Valeurs numériques présentes dans le document source. Tout nombre d'un résumé
# qui n'y figure pas est signalé pour vérification manuelle : c'est soit un
# calcul dérivé légitime, soit une invention.
NOMBRES_SOURCE = {
    "14", "6", "61", "75", "43", "18", "2", "340000", "268000", "47000",
    "25000", "12", "3", "1", "14", "20", "29", "720", "1410", "1105",
    "650", "415", "68", "89", "72", "34", "81", "22", "4", "9", "15",
    "2847", "43", "38", "36", "5", "15820", "8", "50", "85000", "23",
    "21", "121", "2025", "7",
}


def normaliser(texte):
    """Minuscules, accents retirés, espaces insécables normalisés."""
    texte = retirer_commentaires(texte)
    texte = texte.replace(" ", " ").replace(" ", " ")
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    return texte.lower()


def retirer_commentaires(texte):
    """Retire les commentaires HTML (gabarit des fichiers de réponse)."""
    return re.sub(r"<!--.*?-->", " ", texte, flags=re.DOTALL)


def compter_mots(texte):
    """Compte les mots, en ignorant le balisage markdown."""
    texte = retirer_commentaires(texte)
    texte = re.sub(r"[#*_>`|\-]", " ", texte)
    return len([m for m in texte.split() if any(c.isalnum() for c in m)])


def couverture_chiffres(texte):
    """Retourne (nb_trouves, liste des libellés manquants)."""
    norm = normaliser(texte)
    manquants = []
    for libelle, motifs in CHIFFRES_CLES:
        if not any(re.search(m, norm) for m in motifs):
            manquants.append(libelle)
    return len(CHIFFRES_CLES) - len(manquants), manquants


def nombres_suspects(texte):
    """Nombres du résumé absents du document source."""
    norm = normaliser(texte).replace(" ", "")
    trouves = set(re.findall(r"\d+(?:[.,]\d+)?", norm))
    suspects = set()
    for n in trouves:
        propre = n.replace(",", "").replace(".", "")
        if propre not in NOMBRES_SOURCE:
            suspects.add(n)
    return sorted(suspects)


def analyser(chemin, mots_source):
    texte = chemin.read_text(encoding="utf-8")
    mots = compter_mots(texte)
    trouves, manquants = couverture_chiffres(texte)
    return {
        "nom": chemin.stem,
        "mots": mots,
        "compression": mots / mots_source if mots_source else 0,
        "couverture": trouves,
        "manquants": manquants,
        "suspects": nombres_suspects(texte),
    }


def main():
    if not SOURCE.exists():
        print(f"Document source introuvable : {SOURCE}")
        return 1

    mots_source = compter_mots(SOURCE.read_text(encoding="utf-8"))

    if not DOSSIER_REPONSES.exists():
        print(f"Dossier {DOSSIER_REPONSES.name}/ absent.")
        print("Créez-le et déposez une réponse par exécution :")
        print("  A-exec1.md  A-exec2.md  B-exec1.md  B-exec2.md  C-exec1.md  C-exec2.md")
        return 1

    fichiers = sorted(DOSSIER_REPONSES.glob("*.md"))
    if not fichiers:
        print(f"Aucun fichier .md dans {DOSSIER_REPONSES.name}/")
        return 1

    print(f"Document source : {mots_source} mots")
    print()
    print(f"{'Exécution':<12} {'Mots':>6} {'Compr.':>8} {'Chiffres':>10}  Nombres suspects")
    print("-" * 70)

    resultats = [analyser(f, mots_source) for f in fichiers]
    for r in resultats:
        susp = ", ".join(r["suspects"]) if r["suspects"] else "-"
        print(f"{r['nom']:<12} {r['mots']:>6} {r['compression']:>7.1%} {r['couverture']:>8}/8  {susp}")

    print()
    for r in resultats:
        if r["manquants"]:
            print(f"{r['nom']} — chiffres absents : {', '.join(r['manquants'])}")

    print()
    print("Rappel : les nombres suspects sont à vérifier manuellement.")
    print("Un calcul dérivé légitime (ex. un écart) y apparaît aussi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
collecte.py — Voltéo Énergies
Script de collecte FOURNI (Brief 10 — situation "Fiabiliser des données de terrain").

Simule la récupération de l'export brut quotidien des relevés de production des
parcs solaires et éoliens, tel que remonté par les capteurs de terrain.

Usage (depuis le terminal, environnement activé) :
    python collecte.py

Produit le fichier : production_brute.csv   (séparateur ';', encodage UTF-8)

⚠️  NE PAS MODIFIER : ce script fournit la donnée brute telle quelle. Le nettoyage
    se fait dans un autre fichier (nettoyage.py), en appliquant la grille fournie.

Colonnes de l'export : site ; horodatage ; production ; unite
Les données sont volontairement "sales" : elles reproduisent les défauts réels
d'un export capteur (unités mélangées kW/MW, virgules décimales, relevés
manquants, valeurs aberrantes, noms de sites incohérents, doublons).
"""

import csv

# Relevés bruts tels que remontés par les capteurs (NON nettoyés).
# Chaque tuple = (site, horodatage, production, unite)
RELEVES = [
    # --- Parc Mistral (solaire) ---
    ("Parc Mistral",      "2024-06-01 06:00", "210,5",  "kW"),
    ("parc mistral",      "2024-06-01 12:00", "1320,8", "kW"),
    ("parc mistral",      "2024-06-01 12:00", "1315,0", "kW"),   # horodatage en double (même site)
    ("PARC MISTRAL",      "2024-06-01 18:00", "540",    "kW"),
    ("  Parc Mistral",    "2024-06-02 06:00", "",       "kW"),   # relevé manquant (vide)
    ("Parc Mistral ",     "2024-06-02 12:00", "1290,4", "kW"),
    ("Parc Mistral",      "2024-06-02 18:00", "-9999",  "kW"),   # relevé manquant (sentinelle)

    # --- Parc du Levant (éolien) ---
    ("Parc du Levant",    "2024-06-01 06:00", "1,8",    "MW"),   # unité MW
    ("parc du levant",    "2024-06-01 12:00", "2,1",    "MW"),   # unité MW
    ("Parc du Levant",    "2024-06-01 18:00", "1650,0", "kW"),
    ("Parc du Levant",    "2024-06-01 18:00", "1650,0", "kW"),   # ligne strictement identique (doublon)
    ("PARC DU LEVANT ",   "2024-06-02 06:00", "-45",    "kW"),   # production négative (aberration)
    ("parc du levant",    "2024-06-02 12:00", "1980,5", "kW"),
    ("Parc du Levant",    "2024-06-02 18:00", "2,0",    "MW"),   # unité MW

    # --- Solaire Garrigue (solaire) ---
    ("Solaire Garrigue",  "2024-06-01 06:00", "180,2",  "kW"),
    ("solaire garrigue ", "2024-06-01 12:00", "1105,6", "kW"),
    ("SOLAIRE GARRIGUE",  "2024-06-01 18:00", "430,9",  "kW"),
    ("Solaire Garrigue",  "2024-06-02 06:00", "",       "kW"),   # relevé manquant (vide)
    ("Solaire Garrigue",  "2024-06-02 12:00", "1150,2", "kW"),
    ("solaire garrigue",  "2024-06-02 12:00", "1148,0", "kW"),   # horodatage en double (même site)
    ("Solaire Garrigue",  "2024-06-02 18:00", "-12,5",  "kW"),   # production négative (aberration)

    # --- Plaine du Vent (éolien) ---
    ("Plaine du Vent",    "2024-06-01 06:00", "820,0",  "kW"),
    ("Plaine du Vent",    "2024-06-01 06:00", "820,0",  "kW"),   # ligne strictement identique (doublon)
    ("plaine du vent",    "2024-06-01 12:00", "1,5",    "MW"),   # unité MW
    ("Plaine du Vent ",   "2024-06-01 18:00", "1420,7", "kW"),
    ("PLAINE DU VENT",    "2024-06-02 06:00", "-9999",  "kW"),   # relevé manquant (sentinelle)
    ("Plaine du Vent",    "2024-06-02 12:00", "1735,3", "kW"),
    ("plaine du vent",    "2024-06-02 18:00", "1,9",    "MW"),   # unité MW
]


def main():
    fichier = "production_brrute.csv"
    with open(fichier, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["site", "horodatage", "production", "unite"])
        writer.writerows(RELEVES)
    print(f"{len(RELEVES)} relevés écrits dans {fichier}")


if __name__ == "__main__":
    main()

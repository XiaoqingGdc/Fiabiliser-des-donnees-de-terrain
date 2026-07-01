import pandas as pd
import numpy as np

# ==========================================
#  CHARGEMENT SÉCURISÉ (Robustesse)
# ==========================================
try:
    df = pd.read_csv('production_brute.csv', sep=';')
except FileNotFoundError:
    print("Erreur : Le fichier 'production_brute.csv' est introuvable.")
    print("Assure-toi qu'il est dans le même dossier que ce script.")

lignes_initiales = df.shape[0]

# ==========================================
#   NETTOYAGE DES DONNÉES
# ==========================================

df["site"] = df["site"].str.strip().str.lower()
df["horodatage"] = pd.to_datetime(df["horodatage"], format="%Y-%m-%d %H:%M")
if df["production"].dtype == "object":
    df["production"] = df["production"].str.replace(',', '.')
df["production"] = pd.to_numeric(df["production"], errors="coerce")

valeurs_passees_nan = ((df["production"] < 0) | (df["production"] == -9999)).sum()
condition = (df["production"] < 0) | (df["production"] ==-9999)
df.loc[condition, "production"] = np.nan

df["unite"] = df["unite"].str.strip()
condition_mw = (df["unite"] == "MW")
conversions_mw_kw = condition_mw.sum() # Compteur pour le bilan
df.loc[condition,'production'] = df.loc[condition,'production'] * 1000
df['unite'] = 'kW'
 
df = df.drop_duplicates(subset=['site','horodatage'], keep='first')
lignes_finales = df.shape[0]

nbr_lignes_supprimees = lignes_initiales - lignes_finales

# ==========================================
#   BILAN ET AGREGATION
# ==========================================
print('='*60)
print('               Bilan du nettoyage               ')
print('='*60)
print(f'- Nombre de lignes supprimees (doublons) : {nbr_lignes_supprimees}')
print(f'- Nombre de valeurs passees a NaN : {valeurs_passees_nan}')
print(f'- Nombre de conversions MW -> kW : {conversions_mw_kw}')
print('='*60)

resume_par_site = df.groupby('site').agg({'production': ['mean', 'sum']})


# ==========================================
#       CONTROLES AUTOMATIQUES (Assert)
# ==========================================
print("Lancement des verifications de conformite...")

# 1. Vérification : Toutes les unités valent 'kW'
unités_uniques = df["unite"].unique()
assert len(unités_uniques) == 1 and unités_uniques[0] == "kW", \
    f"Erreur de conformité : Il reste des unités autres que kW : {unités_uniques}"

# 2. Vérification : Aucune production négative (en excluant les NaN)
productions_negatives = (df["production"] < 0).sum()
assert productions_negatives == 0, \
    f"Erreur de conformité : Il reste {productions_negatives} valeur(s) négative(s) !"

# 3. Vérification : Aucun doublon sur le couple (site, horodatage)
nb_doublons_site_date = df.duplicated(subset=["site", "horodatage"]).sum()
assert nb_doublons_site_date == 0, \
    f"Erreur de conformité : Il reste {nb_doublons_site_date} doublon(s) d'horodatage pour un même site !"

print("Tous les controles ont reussi ! Le jeu de donnees est 100% conforme.")


# ==========================================
#   Exportation des fichiers 
# ==========================================

df.to_csv('production_nettoyee.csv', sep=';', index=False)
df.to_csv('resume_par_site.csv', sep=';')


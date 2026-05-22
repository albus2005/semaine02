import pandas as pd

try:
    patients_sale = pd.read_csv("hospital_sale.csv")
except FileNotFoundError:
    print("Fichier Introuvable. Verifier le chemin.")
    patients_sale = pd.DataFrame()  # Création d'un DataFrame vide pour éviter l'erreur

print("Contenu de hospital_sale.csv")

patients_sans_doublon = patients_sale.drop_duplicates()

patients_propres = patients_sans_doublon.copy()
patients_propres['age'] = patients_propres['age'].fillna(patients_propres['age'].mean())
patients_propres['poids'] = patients_propres['poids'].fillna(patients_propres['poids'].mean())

patients_propres.loc[patients_propres['temperature'] > 42, 'temperature'] /= 10

patients_propres['nom'] = patients_propres['nom'].str.capitalize()
patients_propres['sexe'] = patients_propres['sexe'].str.capitalize()

print("Data Frame propre :")
print(patients_propres)
print("Fin Du Programme")
print("Version propre")
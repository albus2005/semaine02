import csv 
import numpy as np

with open("patients_bukavu.csv", "r") as file :
    contenu = csv.DictReader(file)

    poids_colonne = []
    for ligne in contenu :
        poids_ligne = int(ligne['poids'])
        poids_colonne.append(poids_ligne)

poids = np.array(poids_colonne)
max_poids = np.max(poids)
min_poids = np.min(poids)
print(max_poids)
print(min_poids)

print(np.mean(poids))


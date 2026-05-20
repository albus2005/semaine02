import pandas as pd 

'''
feuille_des_donnees = pd.DataFrame(data)
Ecrire(feuille de données )
'''
data = {
'nom': ['Amani', 'Baraka', 'Furaha', 'Mapendo', 'Neema'],
'poids': [12, 15, 10, 18, 14],
'age': [8, 23, 45, 67, 34]
}
df = pd.DataFrame(data)
print(f"La feuille de donnees: {df}")
print(df["age"])
print(df[df['age'] >18])
print(type(df['age'].values))


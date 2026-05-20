import pandas as pd

patients_registre = pd.read_csv("patients_bukavu.csv")
patients_df = pd.DataFrame(patients_registre)
print(patients_df)
print(patients_df['poids'])
#poids = int(patients_df['poids'])
print(patients_df[patients_df['poids'] > 12])
print(patients_df.info())
print(patients_df.describe())


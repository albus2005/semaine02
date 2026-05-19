import pandas as pd

patients_registre = pd.read_csv("patients_bukavu.csv")
patients_df = pd.DataFrame(patients_registre")
print(patients_df)
print(patients_df['age'])
print(patients_df[['age'] > 12])



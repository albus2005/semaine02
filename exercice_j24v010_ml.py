import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Données patients Bukavu
data = {
    'district':   [1, 2, 1, 3, 2, 1, 3, 2, 1, 3],
    'acces_eau':  [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
    'age':        [5, 30, 8, 25, 3, 45, 12, 60, 7, 4],
    'malade':     [1, 0, 1, 0, 1, 0, 1, 0, 1, 1]
}

df = pd.DataFrame(data)

# Étape 1 : séparer features et target
X = df[['district', 'acces_eau', 'age']]
y = df['malade']

# Étape 2 : train_test_split prend 4 arguments
# X, y, la taille du test, et random_state pour reproduire les résultats
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Étape 3 : créer le modèle
model = DecisionTreeClassifier()

# Étape 4 : entraîner -- tu donnes X_train ET y_train
model.fit(X_train, y_train)

# Étape 5 : prédire -- tu donnes seulement X_test
# Le modèle ne doit pas voir y_test
y_pred = model.predict(X_test)

# Étape 6 : comparer y_test (réalité) et y_pred (prédiction)
print(accuracy_score(y_test, y_pred))
nouveau_patient = [[2, 0, 6]]
print(f"Le patient zst malade si : {model.predict(nouveau_patient})
"""
fit()     --> reçoit X_train ET y_train
              (questions + réponses pour apprendre)

predict() --> reçoit seulement X_test
              (questions sans réponses -- c'est l'examen)
"""
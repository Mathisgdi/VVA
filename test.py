import joblib
import pandas as pd
import numpy as np

model = joblib.load('VVA6-class100/model.joblib')

# Récupérer les données envoyées par l'utilisateur via l'API
data = pd.read_csv("data/test.csv")


# predictions  = model.predict(data)
# print(predictions)


predictions_proba =  model.predict_proba(data)
# print(predictions_proba)

def assign_unique_positions(probabilities):
    num_pilots = probabilities.shape[0]
    num_positions = probabilities.shape[1]

    assigned_positions = [-1] * num_pilots  # Initialiser avec -1 (non assigné)
    taken_positions = set()  # Ensemble des positions déjà prises

    for i in range(num_pilots):
        sorted_indices = np.argsort(probabilities[i])[::-1]  # Trier les indices par probabilité décroissante
        for index in sorted_indices:
            # On s'assure que la position est >= 1 (index 0 correspond au premier place)
            if (index + 1) not in taken_positions:  # +1 pour que la position soit à partir de 1
                assigned_positions[i] = index + 1  # On attribue une position qui commence à 1
                taken_positions.add(index + 1)
                break

    # Si une position reste non assignée, attribuer la première disponible.
    available_positions = set(range(1, num_pilots + 1)) - taken_positions
    for i in range(num_pilots):
        if assigned_positions[i] == -1:
            assigned_positions[i] = available_positions.pop()
    return assigned_positions


unique_positions = assign_unique_positions(predictions_proba)
print(unique_positions)

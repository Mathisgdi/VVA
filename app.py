# import joblib
# import pandas as pd
# import numpy as np
# from fastapi import FastAPI, HTTPException, Request
# from fastapi.middleware.cors import CORSMiddleware
#
#
# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Vous pouvez spécifier des domaines spécifiques ici
#     allow_credentials=True,
#     allow_methods=["*"],  # Permet toutes les méthodes (POST, GET, OPTIONS, etc.)
#     allow_headers=["*"],  # Permet tous les headers
# )
# @app.post("/driver")
# async def create_proba(request: Request):
#     model = joblib.load('VVA6-class100/model.joblib')
#
#     try:
#         data = await request.json()
#         df = pd.read_json(data['data'])
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#     # Récupérer les données envoyées par l'utilisateur via l'API
#     # data = pd.read_csv("data/test.csv")
#
#     # predictions  = model.predict(data)
#     # print(predictions)
#
#     predictions_proba = model.predict_proba(df)
#
#     # print(predictions_proba)
#
#     def assign_unique_positions(probabilities):
#         num_pilots = probabilities.shape[0]
#         num_positions = probabilities.shape[1]
#
#         assigned_positions = [-1] * num_pilots  # Initialiser avec -1 (non assigné)
#         taken_positions = set()  # Ensemble des positions déjà prises
#
#         for i in range(num_pilots):
#             sorted_indices = np.argsort(probabilities[i])[::-1]  # Trier les indices par probabilité décroissante
#             for index in sorted_indices:
#                 # On s'assure que la position est >= 1 (index 0 correspond au premier place)
#                 if (index + 1) not in taken_positions:  # +1 pour que la position soit à partir de 1
#                     assigned_positions[i] = index + 1  # On attribue une position qui commence à 1
#                     taken_positions.add(index + 1)
#                     break
#
#         # Si une position reste non assignée, attribuer la première disponible.
#         available_positions = set(range(1, num_pilots + 1)) - taken_positions
#         for i in range(num_pilots):
#             if assigned_positions[i] == -1:
#                 assigned_positions[i] = available_positions.pop()
#         return assigned_positions
#
#     unique_positions = assign_unique_positions(predictions_proba)
#     return {"prédiction": unique_positions}


from fastapi import FastAPI, Request
from pydantic import BaseModel
import pandas as pd
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

import joblib
from xarray.util.generate_ops import inplace

# Charger le modèle
model = joblib.load('VVA-class100/model.joblib')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet à tous les domaines de faire des requêtes
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],  # Permet tous les en-têtes
)

# Définir le schéma des données attendues avec Pydantic
class DriverData(BaseModel):
    date: str
    grandPrix: str
    rainfall: float
    humidity: float
    airTemp: float
    positions: list[dict]


def assign_unique_positions(probabilities):
    num_pilots = probabilities.shape[0]
    num_positions = probabilities.shape[1]

    assigned_positions = [-1] * num_pilots  # Initialiser avec -1 (non assigné)
    taken_positions = set()  # Ensemble des positions déjà prises

    for i in range(num_pilots):
        sorted_indices = np.argsort(probabilities[i])[::-1]  # Trier les indices par probabilité décroissante
        for index in sorted_indices:
            if (index + 1) not in taken_positions:  # +1 pour que la position soit à partir de 1
                assigned_positions[i] = index + 1
                taken_positions.add(index + 1)
                break

    available_positions = set(range(1, num_pilots + 1)) - taken_positions
    for i in range(num_pilots):
        if assigned_positions[i] == -1:
            assigned_positions[i] = available_positions.pop()
    return assigned_positions


@app.post("/predict")
async def predict(data: DriverData):
    # Convertir les données JSON en DataFrame
    print(data)
    positions_data = pd.DataFrame(data.positions) # Convertit la liste des positions en DataFrame

    # Ajouter les autres colonnes dans le DataFrame (Rainfall, Humidity, AirTemp)
    positions_data['date'] = data.date
    positions_data['name_GP'] = data.grandPrix
    positions_data['AirTemp'] = data.airTemp
    positions_data['Humidity'] = data.humidity
    positions_data['Rainfall'] = data.rainfall
    positions_data = positions_data.rename(columns={'constructor': 'name'})
    positions_data = positions_data.rename(columns={'position': 'grid'})
    # Assurez-vous que les colonnes sont dans le bon ordre et les types de données sont corrects
    # positions_data = positions_data.astype({
    #     'Rainfall': 'float64',
    #     'Humidity': 'float64',
    #     'AirTemp': 'float64',
    #     'grid': 'int64'
    # })
    print(positions_data)
    #positions_data['grid'] = data.airTemp
    # positions_data['AirTemp'] = data.airTemp
    # positions_data['AirTemp'] = data.airTemp

    # Faire la prédiction avec le modèle

    # predictions_proba = model.predict_proba(positions_data)
    # print(predictions_proba)
    #
    # # Attribuer des positions uniques
    # unique_positions = assign_unique_positions(predictions_proba)
    # # predictions_proba = model.predict_proba(positions_data)
    # #
    # # # Convertir les probabilités en liste
    # # predictions_proba = predictions_proba.tolist()
    # # Attribuer des positions uniques
    # unique_positions = assign_unique_positions(np.array(predictions_proba))

    predictions_proba = model.predict_proba(positions_data)
    # Convertir les probabilités en liste
    predictions_proba = predictions_proba.tolist()
    print(predictions_proba)

    # Attribuer des positions uniques
    unique_positions = assign_unique_positions(np.array(predictions_proba))
    unique_positions = list(map(int, unique_positions))
    print(unique_positions)
    print(positions_data['surname'])
    # List of unique positions
    unique_positions = [1, 2, 4, 3, 5, 6, 7, 9, 10, 8, 11, 12, 15, 16, 13, 14, 17, 19, 18, 20]

    # DataFrame with surnames
    surnames = positions_data['surname'].tolist()

    # Create a list to hold the ordered surnames
    ordered_surnames = [None] * len(unique_positions)

    # Place each surname in the correct position
    for index, position in enumerate(unique_positions):
        ordered_surnames[position - 1] = surnames[index]

    print(ordered_surnames)
    # Retourner les résultats sous forme de JSON
    return {"predicted_positions": ordered_surnames}


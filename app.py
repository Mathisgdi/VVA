from fastapi import FastAPI, Request
from pydantic import BaseModel
import pandas as pd
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import joblib

# Charger le modèle
model = joblib.load('VVA-class100/model.joblib')

app = FastAPI()

app.add_middleware( # je suis obliugé de faire ça pour que ça marche car en Next.js quand je fais une requête POST, cela fait d'abord une requête OPTIONS car mon API est sur un domaine et port différent de celui de Next.js
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
    print(positions_data)


    predictions_proba = model.predict_proba(positions_data)
    # Convertir les probabilités en liste
    predictions_proba = predictions_proba.tolist()

    unique_positions = assign_unique_positions(np.array(predictions_proba))
    unique_positions = list(map(int, unique_positions))
    print(unique_positions)
    # DataFrame with surnames
    surnames = positions_data['surname'].tolist()

    # Create a list to hold the ordered surnames
    ordered_surnames = [None] * len(unique_positions)

    # Place each surname in the correct position
    for index, position in enumerate(unique_positions):
        ordered_surnames[position - 1] = surnames[index]

    print(ordered_surnames)
    return {"predicted_positions": ordered_surnames}


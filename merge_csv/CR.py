import pandas as pd
import os

print("Répertoire de travail actuel :", os.getcwd())
base_path = r'merge_csv\csv_parquet'

# Charger les fichiers CSV en utilisant des chemins absolus
df_results = pd.read_csv(os.path.join(base_path, 'races.csv'))
df_circuits = pd.read_csv(os.path.join(base_path, 'circuits.csv'))

# Sélectionner uniquement les colonnes 'circuitId' et 'name'
df_circuits_selected = df_circuits[['circuitId', 'name']]

# Joindre les fichiers sur la colonne 'circuitId'
df_merged = pd.merge(df_results, df_circuits_selected, on='circuitId', how='left')

# Imprimer les colonnes après la fusion pour vérifier leur présence
print("Colonnes après la fusion :", df_merged.columns)

# Réorganiser les colonnes pour placer 'name' juste après 'circuitId'
cols = list(df_merged.columns)
circuit_id_index = cols.index('circuitId')
if 'name' in cols:
    cols.insert(circuit_id_index + 1, cols.pop(cols.index('name')))
else:
    print("Erreur : La colonne 'name' n'est pas présente dans le DataFrame fusionné.")
df_merged = df_merged[cols]

# Sauvegarder le nouveau fichier CSV avec les noms des circuits ajoutés
df_merged.to_csv(os.path.join(base_path, 'CR.csv'), index=False)

print("Fusion réussie ! Le fichier a été sauvegardé sous 'CR.csv'.")
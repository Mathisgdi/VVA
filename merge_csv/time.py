import pandas as pd
import os

print("Répertoire de travail actuel :", os.getcwd())
base_path = r'merge_csv\csv_parquet'

# Charger le fichier CSV lap_times.csv
df_lap_times = pd.read_csv(os.path.join(base_path, 'lap_times.csv'))

# Calculer le temps total en millisecondes pour chaque pilote pour chaque course
df_total_time = df_lap_times.groupby(['driverId', 'raceId'])['milliseconds'].sum().reset_index()
df_total_time.rename(columns={'milliseconds': 'total_time_ms'}, inplace=True)

# Convertir le temps total en secondes
df_total_time['total_time_sec'] = df_total_time['total_time_ms'] / 1000

# Sauvegarder le nouveau fichier CSV avec les temps totaux en secondes
df_total_time.to_csv(os.path.join(base_path, 'total_lap_times.csv'), index=False)

print("Transformation réussie ! Le fichier a été sauvegardé sous 'total_lap_times.csv'.")
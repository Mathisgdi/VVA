import pandas as pd
import os

print("Répertoire de travail actuel :", os.getcwd())
base_path = r'merge_csv\csv_parquet'

df_results = pd.read_csv(os.path.join(base_path, 'results.csv'))
df_drivers = pd.read_csv(os.path.join(base_path, 'drivers.csv'))
df_constructors = pd.read_csv(os.path.join(base_path, 'constructors.csv'))
df_CR = pd.read_csv(os.path.join(base_path, 'CR.csv'))
df_status = pd.read_csv(os.path.join(base_path, 'status.csv'))
df_time_total = pd.read_csv(os.path.join(base_path, 'total_lap_times.csv'))

print("Colonnes de df_time_total:", df_time_total.columns)

df_drivers_selected = df_drivers[['driverId', 'forename', 'surname']]
df_constructors_selected = df_constructors[['constructorId', 'name']]
df_CR_selected = df_CR[['raceId', 'circuitId', 'date', 'hour', 'name_GP', 'name_circuit']]
df_status_selected = df_status[['statusId', 'status']]
df_time_selected = df_time_total[['driverId', 'raceId', 'total_time_sec']]

df_merged = pd.merge(df_results, df_drivers_selected, on='driverId', how='left')
df_merged = pd.merge(df_merged, df_constructors_selected, on='constructorId', how='left')
df_merged = pd.merge(df_merged, df_CR_selected, on='raceId', how='left')
df_merged = pd.merge(df_merged, df_status_selected, on='statusId', how='left')
df_merged = pd.merge(df_merged, df_time_selected, on=['driverId', 'raceId'], how='left')

print("Colonnes après fusion avec df_time_selected:", df_merged.columns)

cols = list(df_merged.columns)
driver_id_index = cols.index('driverId')
cols.insert(driver_id_index + 1, cols.pop(cols.index('forename')))
cols.insert(driver_id_index + 2, cols.pop(cols.index('surname')))
cols.insert(driver_id_index + 13, cols.pop(cols.index('total_time_sec')))

constructor_id_index = cols.index('constructorId')
cols.insert(constructor_id_index + 1, cols.pop(cols.index('name')))

races_id_index = cols.index('raceId')
cols.insert(races_id_index + 1, cols.pop(cols.index('date')))
cols.insert(races_id_index + 2, cols.pop(cols.index('hour')))
cols.insert(races_id_index + 3, cols.pop(cols.index('name_GP')))
cols.insert(races_id_index + 4, cols.pop(cols.index('name_circuit')))

status_id_index = cols.index('statusId')
cols.insert(status_id_index + 1, cols.pop(cols.index('status')))

df_merged = df_merged[cols]

df_merged['date'] = pd.to_datetime(df_merged['date'])

df_filtered = df_merged[(df_merged['date'].dt.year >= 2018) & (df_merged['date'].dt.year <= 2024)]

df_filtered.to_csv(os.path.join(base_path, 'merge_temps.csv'), index=False)

print("Fusion réussie ! Le fichier a été sauvegardé sous 'results_with_driver_and_constructor_names.csv'.")
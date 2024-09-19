import pandas as pd
import os

print("Répertoire de travail actuel :", os.getcwd())
base_path = r'merge_csv\csv_parquet'

df_results = pd.read_csv(os.path.join(base_path, 'merge_temps.csv'))
df_weather = pd.read_csv(os.path.join(base_path, 'weather_data_mean.csv'))


df_results['date'] = df_results['date'].str.slice(0, 4)

df_weather['date'] = df_weather['date'].astype(str)


df_weather_selected = df_weather[['name_GP', 'date', 'Track', 'AirTemp', 'Humidity', 'Pressure', 'Rainfall', 'TrackTemp', 'WindDirection', 'WindSpeed']].round(2)

df_merged = pd.merge(df_results, df_weather_selected, on=['name_GP', 'date'], how='left')

df_merged.to_csv(os.path.join(base_path, 'finallllll.csv'), index=False)

print("Fusion réussie ! Le fichier a été sauvegardé sous 'merged_results_weather.csv'.")
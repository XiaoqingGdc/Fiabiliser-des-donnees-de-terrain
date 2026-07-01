import pandas as pd
import numpy as np
df=pd.read_csv('production_brute.csv', sep=';')
print(df.shape)
print(df.head(8))
df["site"] = df["site"].str.strip().str.lower()
df["horodatage"] = pd.to_datetime(df["horodatage"], format="%Y-%m-%d %H:%M")
df["production"] = df["production"].str.replace(',', '.')
df["production"] = pd.to_numeric(df["production"], errors="coerce")
condition = (df["production"] < 0) | (df["production"] ==-9999)
df.loc[condition, "production"] = np.nan
print(df['unite'].value_counts())
condition = (df["unite"] == "MW")
df.loc[condition,'production'] = df.loc[condition,'production'] * 1000
df['unite'] = 'kW'
df=df.drop_duplicates(subset=['site','horodatage'], keep='first')
print('-------')

print(f'Il y a {df.shape[0]} lignes dans le DataFrame')
print(df.head(8))

df.to_csv('production_propre.csv', sep=';', index=False)
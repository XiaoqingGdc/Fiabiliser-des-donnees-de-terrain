import pandas as pd
import numpy as np
df=pd.read_csv('production_brute.csv', sep=';')
print(df.head(8))
print(df.columns)
df["site"] = df["site"].str.strip().str.lower()
df["horodatage"]=pd.to_datetime(df["horodatage"], format='%Y-%m-%d %H:%M', errors='coerce')

df["production"]=pd.to_numeric(df["production"].str.replace(",", "."), errors="coerce")

condition  = (df['production'] < 0)
df.loc[condition, 'production'] = np.nan

condition = (df['unite']=="MW")
df.loc[condition, 'production'] = df.loc[condition, 'production'] * 1000

df['unite'] = 'kW'

df=df.drop_duplicates()
print('------------file cleaned------------')
print(df.head(8))
print(df.shape)
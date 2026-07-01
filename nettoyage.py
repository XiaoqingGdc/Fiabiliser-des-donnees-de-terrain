import pandas as pd
df=pd.read_csv('production_brute.csv', sep=';')
print(df.head(8))
print(df.columns)
df["site"] = df["site"].str.strip().str.title()
df["horodatage"]=pd.to_datetime(df["horodatage"])

df["production"]=pd.to_numeric(df["production"].str.replace(",", "."), errors="coerce")
condition = df['production'] < 0
df.loc[condition, 'production'] = 0

condition = (df['unite'])=="MW"
df.loc[condition, 'production'] = df.loc[condition, 'production'] * 1000

df['unite'] = 'kW'
df=df.drop_duplicates()

print(df.head(8))
print(df.shape)
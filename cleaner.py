import pandas as pd
import numpy as np

def country_getter(x):
  if isinstance(x, float):
    return np.nan
  else:
    return x.split(',')[-1]

def region_getter(x):
  if isinstance(x, float):
    return np.nan
  parts = x.split(',')
  if len(parts) > 1:
    return parts[-2]
  else:
    return np.nan

def agtron_divider(x, i):
  if isinstance(x, float):
    return np.nan
  parts = x.split('/')
  if len(parts) < 2:
    return np.nan
  if parts[i] == '' or parts[i] == 'NA' or not parts[i].isnumeric():
    return np.nan
  return float(parts[i].strip())

months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

parts = [pd.read_csv(f'raw_data/df{i}.csv') for i in range(1, 451)]
df = pd.concat(parts)
df.drop('Unnamed: 0', axis=1, inplace=True)
df.reset_index(inplace=True, drop= True)
df['Roaster Country'] = df['Roaster Location'].apply(country_getter)
df['Coffee Origin Country'] = df['Coffee Origin'].apply(country_getter)
df['Coffee Origin Region'] = df['Coffee Origin'].apply(region_getter)
df['Agtron'].replace('NA', np.nan)
df['Agtron outside'] = df['Agtron'].apply(agtron_divider, **{'i':0})
df['Agtron inside'] = df['Agtron'].apply(agtron_divider, **{'i':1})
#df['Price per kg'] = df['Est. Price'].apply(price_per_kg)
df['Review year'] = df['Review Date'].apply(lambda x: int(x.split(' ')[1]))
df['Review month'] = df['Review Date'].apply(lambda x: months[x.split(' ')[0]])


coffe_countries_pre_df = {"Index": [], "Country": []}
for i, line in enumerate(df['Coffee Origin Country']):
  if line is np.nan:
    continue
  parts = line.split(';')
  for part in parts:
    coffe_countries_pre_df['Index'].append(int(i))
    coffe_countries_pre_df['Country'].append(part.strip())
coffe_countries_df = pd.DataFrame(coffe_countries_pre_df)
df.drop('Coffee Origin Country', axis=1, inplace=True)

coffe_countries_df.to_csv('clean_data/coffe_countries_df.csv')
df.to_csv('clean_data/df.csv')
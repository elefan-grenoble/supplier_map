import os
import pandas as pd
from tqdm import tqdm

from source.main.address_to_coords import AddressToCoords, get_data_dir

# Read data
data = pd.read_csv(os.path.join(get_data_dir(), 'supplier_table.csv'), encoding='iso-8859-1', sep=';')

# Add coordinates
addr2c = AddressToCoords()
data['lat'] = None
data['lon'] = None
try:
    for index, row in tqdm(data.iterrows(), total=len(data)):
        if not pd.isnull(row['Adresse 1']):
            location = addr2c.get_coordinates(row['Adresse 1'] + ' ' + str(int(row['C.Postal'])) + ' ' + row['Ville'])
            data.loc[index, 'lat'] = location[0]
            data.loc[index, 'lon'] = location[1]
finally:
    addr2c.save_database()

# Export some data
data[['RaisonSociale', 'lat', 'lon']].to_csv(os.path.join(get_data_dir(), 'umap.csv'), encoding='utf8',
                                             index=None, sep=';')
missing_coordinates_nb = pd.isnull(data['lat']).sum()
print(f'{missing_coordinates_nb} suppliers with no coordinates')
data2 = data[~pd.isnull(data['lat'])]
data2[['RaisonSociale', 'lat', 'lon']].to_csv(os.path.join(get_data_dir(), 'umap_filtered.csv'), encoding='utf8',
                                              index=None, sep=';')

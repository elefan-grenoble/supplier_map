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

# Add testing data for more data
data['website'] = None
data['logo'] = None
data['rayon'] = None
data.loc[data['RaisonSociale'] == 'LA FURIEUSE', 'website'] = 'https://lafurieuse.com'
data.loc[data['RaisonSociale'] == 'LA FURIEUSE', 'rayon'] = 'Alcool'
data.loc[data['RaisonSociale'] == 'LA FURIEUSE', 'logo'] = 'https://scontent.fcdg1-1.fna.fbcdn.net/v/t1.0-9/72325019_1194704764045984_6604308620500795392_n.jpg?_nc_cat=105&_nc_oc=AQmVfZ63OgljkiGA9ngEw81qAzhwCcpjI2jL2Haa9_Uhkj_ard5oEInbaCUQdBCUhxc&_nc_ht=scontent.fcdg1-1.fna&oh=9bea50f4cf0d2b06e936e0bd3453ee7d&oe=5E31F647'
data.loc[data['RaisonSociale'] == 'MIELLERIE DU PEUPLE ZÉLÉ', 'website'] = 'http://www.peuplezele.com/'
data.loc[data['RaisonSociale'] == 'MIELLERIE DU PEUPLE ZÉLÉ', 'rayon'] = 'Epicerie'
data.loc[data['RaisonSociale'] == 'MIELLERIE DU PEUPLE ZÉLÉ', 'logo'] = 'https://peuplezele.weebly.com/uploads/4/4/6/3/44638561/editor/logopeuplezele.jpg?1511516256'

# Export some data
data[['RaisonSociale', 'lat', 'lon']].to_csv(os.path.join(get_data_dir(), 'umap.csv'), encoding='utf8',
                                             index=None, sep=';')
missing_coordinates_nb = pd.isnull(data['lat']).sum()
print(f'{missing_coordinates_nb} suppliers with no coordinates')
data2 = data[~pd.isnull(data['lat'])]
data2[['RaisonSociale', 'lat', 'lon', 'website', 'logo', 'rayon']].to_csv(os.path.join(get_data_dir(), 'umap_filtered.csv'),
                                                                          encoding='utf8', index=None, sep=';')

import argparse
import locale
import os
import pandas as pd
from tqdm import tqdm

from source.main.address_to_coords import AddressToCoords, get_data_dir


def get_args():
    parser = argparse.ArgumentParser(description='Transform supplier file to usable file by umap')
    parser.add_argument('filename', type=str, help='Name of the data file to read from the data directory')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    # Read data
    data = pd.read_csv(os.path.join(get_data_dir(), args.filename), encoding='iso-8859-1', sep=';')

    # Add coordinates
    addr2c = AddressToCoords()
    data['lat'] = None
    data['lon'] = None
    try:
        for index, row in tqdm(data.iterrows(), total=len(data)):
            address = row['Adresse 1'] if not pd.isnull(row['Adresse 1']) else row['RaisonSociale']
            if not pd.isnull(row['Adresse 2']):
                address += ' ' + row['Adresse 2']
            if pd.isnull(row['C.Postal']):
                continue
            address += ' ' + str(int(row['C.Postal'])) + ' ' + row['Ville']
            location = addr2c.get_coordinates(address, row['Pays'])
            data.loc[index, 'lat'] = location[0]
            data.loc[index, 'lon'] = location[1]
    finally:
        addr2c.save_database()

    # Format Date
    locale.setlocale(locale.LC_TIME, '')
    data['DatePartenariat'] = pd.to_datetime(data['Date partenariat'], format='%d/%m/%Y').dt.strftime('%B %Y')
    data['DatePartenariat'] = data['DatePartenariat'].apply(lambda d: '' if d == 'NaT' else d[0].upper() + d[1:])

    # Export some data
    missing_coordinates_nb = pd.isnull(data['lat']).sum()
    print(f'{missing_coordinates_nb} suppliers with no coordinates')
    data2 = data[~pd.isnull(data['lat'])]
    columns_to_keep = ['RaisonSociale', 'lat', 'lon', 'Site', 'Rayon', 'Description', 'Slogan', 'Photo', 'Produits',
                       'DatePartenariat']
    data2[columns_to_keep].to_csv(os.path.join(get_data_dir(), 'umap_filtered.csv'),
                                  encoding='utf8', index=None, sep=';')

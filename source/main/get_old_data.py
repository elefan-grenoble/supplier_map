import argparse
import os
import pandas as pd

from source.main.address_to_coords import get_data_dir


def get_args():
    parser = argparse.ArgumentParser(description='Transform supplier file to usable file by umap')
    parser.add_argument('old_filename', type=str, help='Name of the previous data file to read from the data directory')
    parser.add_argument('new_filename', type=str, help='Name of the new data file to read from the data directory')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    # Read data
    old_data = pd.read_csv(os.path.join(get_data_dir(), args.old_filename), encoding='cp1252', sep=';')
    new_data = pd.read_csv(os.path.join(get_data_dir(), args.new_filename), encoding='cp1252', sep=';')

    # Fill new data with old ones
    columns_to_keep = ['Adresse 1', 'Adresse 2', 'C.Postal', 'Ville', 'RaisonSociale', 'Pays', 'Site',
                       'Date partenariat', 'Rayon', 'Date mise à jour', 'Description', 'Slogan', 'Photo', 'Produits']
    new_data = pd.merge(new_data, old_data[columns_to_keep], on='RaisonSociale', how='left', suffixes=('', '_old'))

    # Fix missing data
    for col in ['Adresse 1', 'Adresse 2', 'C.Postal', 'Ville']:
        new_data[col] = new_data[col].fillna(new_data[col + '_old'])
        del new_data[col + '_old']

    # Fix type
    new_data['C.Postal'] = new_data['C.Postal'].fillna(0)
    new_data['C.Postal'] = new_data['C.Postal'].astype(int)

    # Export modified new file
    filename = args.new_filename[:-4] + '_modified.csv'
    new_data.to_csv(os.path.join(get_data_dir(), filename), encoding='cp1252', index=None, sep=';')

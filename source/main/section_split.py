import argparse
import os
import pandas as pd

from source.main.address_to_coords import get_data_dir


section_mapping = {'Epicerie': 'L\'Épicerie sucrée et salée',
                   'Épicerie': 'L\'Épicerie sucrée et salée',
                   'Boissons': 'Les Boissons',
                   'Hyg': 'L\'Hygiène et les Produits d\'entretien',
                   'Frais': 'Le Frais',
                   'Fromages': 'Le Frais',
                   'oeufs': 'Le Frais',
                   'Viandes': 'Le Frais',
                   'Fruits': 'Les Fruits et Légumes',
                   'Presse': 'Les Magazines',
                   'Surg': 'Les Surgelés',
                   'Pain': 'Le Pain',
                   'Animalerie': 'L\'Animalerie',
                   'Fournitures de bureau': 'Papeterie'
}


def get_args():
    parser = argparse.ArgumentParser(description='Transform umap file to one file by section')
    parser.add_argument('filename', type=str, help='Name of the umap file ')
    return parser.parse_args()


def apply_section_mapping(df):
    df['Section'] = 'Divers'
    for section in section_mapping:
        df.loc[df['Rayon'].apply(lambda s: str(s).startswith(section)), 'Section'] = section_mapping[section]


def split_by_section(df, directory):
    for section in df['Section'].unique():
        df[df['Section'] == section].to_csv(os.path.join(directory, f'{section}.csv'), index=None, sep=';')


if __name__ == '__main__':
    args = get_args()
    df = pd.read_csv(os.path.join(get_data_dir(), args.filename), encoding='cp1252', sep=';')
    apply_section_mapping(df)
    output_dir = os.path.join(get_data_dir(), 'rayons')
    os.makedirs(output_dir, exist_ok=True)
    split_by_section(df, output_dir)

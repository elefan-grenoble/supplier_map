import pandas as pd
import os
import time

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim, BANFrance


def get_data_dir():
    if os.path.exists('data'):
        return 'data'
    if os.path.exists(os.path.join('..', '..', 'data')):
        return os.path.join('..', '..', 'data')
    assert(False)


class AddressToCoords:
    def __init__(self, database_file=os.path.join(get_data_dir(), 'address_to_coords.csv')):
        self.nominatim = Nominatim(user_agent='supplier_map')
        self.ban = BANFrance()
        if os.path.exists(database_file):
            self.database_file = database_file
            self.database = pd.read_csv(self.database_file, encoding='iso-8859-1', sep=';')
        else:
            self.database = pd.DataFrame()
            self.database_file = database_file if database_file is not None else 'address_to_coords.csv'

    def get_online_coordinates(self, address, country='France'):
        time.sleep(1.1)  # Respect the API condition
        location = None
        if country == 'France':
            try:
                location = self.ban.geocode(address)
            except GeocoderTimedOut:
                location = None
            print(f'Adress {address} sought with BAN')
        if location is None:
            try:
                location = self.nominatim.geocode(address)
            except GeocoderTimedOut:
                location = None
            print(f'Adress {address} sought with Nominatim')
            if location is None:
                print(f'Adress not found for : {address}')
                return None, None
        self.database = pd.concat([self.database, pd.DataFrame(data=[(address, location.latitude, location.longitude)],
                                                               columns=['Address', 'lat', 'lon'])], axis=0)
        return location.latitude, location.longitude

    def save_database(self):
        self.database.round(4).to_csv(self.database_file, index=None, sep=';')

    def get_coordinates(self, address, country):
        if 'Address' in self.database and address in self.database['Address'].values:
            idx = self.database[self.database['Address'] == address].index
            return self.database.loc[idx, 'lat'].values[0], self.database.loc[idx, 'lon'].values[0]
        return self.get_online_coordinates(address, country)


if __name__ == '__main__':
    addr2c = AddressToCoords()
    print(addr2c.get_coordinates("175 5th Avenue NYC"))
    addr2c.save_database()

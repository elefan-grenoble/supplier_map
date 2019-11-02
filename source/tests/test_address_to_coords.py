import unittest

from source.main.address_to_coords import AddressToCoords


class TestAddressToCoords(unittest.TestCase):
    def setUp(self):
        self.addr2c = AddressToCoords()

    def test_online_coordinates(self):
        latitude, longitude = self.addr2c.get_online_coordinates('Allée du Commerce équitable 32500 FLEURANCE', 'France')
        self.assertAlmostEqual(latitude, 43.8546, delta=0.02)
        self.assertAlmostEqual(longitude, 0.6479, delta=0.02)

    def test_address_outside_france(self):
        latitude, longitude = self.addr2c.get_online_coordinates('Via Muscatello 95125 CATANIA', 'Italie')
        self.assertAlmostEqual(latitude, 37.51422, delta=0.02)
        self.assertAlmostEqual(longitude, 15.08233, delta=0.02)

if __name__ == '__main__':
    unittest.main()

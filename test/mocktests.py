import unittest
from unittest import mock
from unittest.mock import patch, Mock
from app.calculator import Calculator
import requests

class TestApi(unittest.TestCase):

    """
    In this class we carry out mocking of the Weather Api calls
    """

    def test_weatherApi_StatusCode(self):
        """
        This function is used to check whether we recieve an appropriate status code from the mock api call response
        """
        with patch('app.calculator.requests.get') as mock_get:
            mock_get.return_value.status_code = 200

            obj = Calculator()
            response = obj.get

        self.assertEqual(response.status_code, 200)

    #Alternative code performing the same functionality
    def test_weatherApi_StatusCode1(self):
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200

            assert Calculator().get.status_code == 200

    def test_weatherApi_ID(self):
        """
        This function is used to check whether the api call correctly gets the mocked value
        """
        fake_json = [{'id': 'ab9f494f-f8a0-4c24-bd2e-2497b99f2258', 'postcode': '3800',
                      'name': 'MONASH UNIVERSITY', 'state': 'VIC', 'latitude': '-37.9105599',
                      'longitude': '145.1362485', 'distanceToNearestWeatherStationMetres': 3771.993796218797,
                      'nearestWeatherStation': {'name': 'OAKLEIGH (METROPOLITAN GOLF CLUB)', 'state': 'VIC',
                                                'latitude': '-37.9142', 'longitude': '145.0935'}}]

        location = ''
        with patch('app.calculator.requests.get') as mock_get:
            mock_get.return_value.json.return_value = fake_json

            #make the actual response to the api
            obj = Calculator()
            response = obj.get

            for a in response.json():
                location += (a['id'])

            self.assertEqual(location, 'ab9f494f-f8a0-4c24-bd2e-2497b99f2258')

    def test_weatherApi_name(self):
        """
        This function is used to check whether the api call correctly gets the mocked value
        """

        fake_json = [{'id': 'ab9f494f-f8a0-4c24-bd2e-2497b99f2258', 'postcode': '3800',
                      'name': 'MONASH UNIVERSITY', 'state': 'VIC', 'latitude': '-37.9105599',
                      'longitude': '145.1362485', 'distanceToNearestWeatherStationMetres': 3771.993796218797,
                      'nearestWeatherStation': {'name': 'OAKLEIGH (METROPOLITAN GOLF CLUB)', 'state': 'VIC',
                                                'latitude': '-37.9142', 'longitude': '145.0935'}}]

        location = ''
        with patch('app.calculator.requests.get') as mock_get:
            mock_get.return_value.json.return_value = fake_json

            #make the actual response to the api
            obj = Calculator()
            response = obj.get

            for a in response.json():
                location += (a['name'])

            self.assertEqual(location, 'MONASH UNIVERSITY')

    def test_weatherApi_postcode(self):
        """
        This function is used to check whether the api call correctly gets the mocked value
        """

        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.postcode = '3800'

            assert Calculator().get.postcode == '3800'

def main():
    suit = unittest.TestLoader().loadTestsFromTestCase(TestApi)
    unittest.TextTestRunner(verbosity=2).run(suit)

main()









import datetime

from requests.api import get
try:
    from app.calculator import *
except ImportError:
    # fix import issues
    # ref: https://stackoverflow.com/questions/54339118/python3-x-modulenotfounderror-when-import-file-from-parent-directory/54340672
    import sys
    sys.path.append(sys.path[0] + "/..")
    from app.calculator import *
    
from app.calculator import *

import unittest
from unittest.mock import Mock
from mock import patch
from main import url_exists



class FetchTests(TestCase):
    def test_returns_true_if_url_found(self):
        with patch('requests.get') as mock_request:
            url = 'http://118.138.246.158/api/v1/location?postcode=3800'

            # set a `status_code` attribute on the mock object
            # with value 200
            mock_request.return_value.status_code = 200

            self.assertTrue(url_exists(url))

    def test_returns_false_if_url_not_found(self):
        with patch('requests.get') as mock_request:
                url = 'http://118.138.246.158/api/v1/location=1232113'

                # set a `status_code` attribute on the mock object
                # with value 404
                mock_request.return_value.status_code = 404

                self.assertFalse(url_exists(url))
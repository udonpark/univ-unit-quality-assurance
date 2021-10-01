import datetime
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
def test_mock():
   mock = Mock()
        mock.return_value = {
            "postcode": "3800",
            "date":"01-01-2020",
        }

    Calculator.is_holiday = Mock()
        holi_new_yr = "2020-01-01"
        Calculator.return_value = True
        assert Calculator.is_holiday()


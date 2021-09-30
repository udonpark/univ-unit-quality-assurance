import main
from app.calculator import *
import unittest
from unittest.mock import Mock

class TestCalculator(unittest.TestCase):

    # you may create more test methods
    # you may add parameters to test methods
    # this is an example
    def test_cost(self):
        self.calculator = Calculator()
        self.assertEqual(self.calculator.cal_cost("", "", "", "", ""), "")

    #Need to do testing on the methods NOT using api

    #Need to test the other two calculations(solar energy and time)

    #Need to mock test the methods using api
    def test_SunHourRetrieval(self):
        pass

    def test_DayLightLengthRetrieval(self):
        pass

    def test_CloudCoverRetrieval(self):
        pass

    def some_test(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False  # disable CSRF to prevent context errors
        with main.ev_calculator_app.app_context():

    # place your testing code here


    # you may create test suite if needed
    if __name__ == "__main__":
        pass

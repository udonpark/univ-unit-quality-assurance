import os import unittest
from src.utils.FileManager import FileManager

from app.calculator import *
import unittest

class TestCalculator(unittest.TestCase):

    # you may create more test methods
    # you may add parameters to test methods
    # this is an example
    def test_cost(self):
            self.calculator = Calculator()
            test_configuration="1"
            test_initial_state=10
            test_final_state=100
            test_capacity=80

            self.assertEqual(self.calculator.is_holiday("2021-01-01"), True)
            self.assertEqual(self.calculator.is_holiday("2021-01-02"), False)
            self.assertEqual(self.calculator.is_holiday("2021-01-09"), True)



    # you may create test suite if needed
    if __name__ == "__main__":
        pass

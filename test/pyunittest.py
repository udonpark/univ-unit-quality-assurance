from app.calculator import *
import unittest

class TestCalculator(unittest.TestCase):

    # you may create more test methods
    # you may add parameters to test methods
    # this is an example
    """sdbasd"""
        def test_cost(self):
            self.calculator = Calculator()
            test_configuration="1"
            test_initial_state=10
            test_final_state=100
            test_capacity=80

            """
            """
            self.assertEqual(self.calculator.is_holiday("2021-01-01"), True)
            self.assertEqual(self.calculator.is_holiday("2021-01-02"), False)
            self.assertEqual(self.calculator.is_holiday("2021-01-09"), True)


        """
        Pairwise testing was used for 
        """


    def test_cost(self):
        self.calculator = Calculator()
        self.assertEqual(self.calculator.cost_calculation("", "", "", "", ""), "")

    # you may create test suite if needed
    if __name__ == "__main__":
        pass

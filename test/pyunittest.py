from app.calculator import *
import unittest

from project.app.calculator import Calculator


class TestCalculator(unittest.TestCase):
    # you may create more test methods
    # you may add parameters to test methods
    # this is an example
    def test_cost(self):
        self.calculator = Calculator()
        test_configuration = "1"
        test_initial_state = 10
        test_final_state = 100
        test_capacity = 80

        """
        """
        self.assertEqual(self.calculator.is_holiday("2021-01-01"), True)
        self.assertEqual(self.calculator.is_holiday("2021-01-02"), False)
        self.assertEqual(self.calculator.is_holiday("2021-01-09"), True)

        self.assertEqual(self.calculator.is_peak("05:59"), False)
        self.assertEqual(self.calculator.is_peak("06:00"), True)
        self.assertEqual(self.calculator.is_peak("18:00"), True)
        self.assertEqual(self.calculator.is_peak("18:01"), False)

        """
        Pairwise testing was used for 
        """
        self.assertEqual(
            self.calculator.cost_calculation(test_configuration, test_initial_state, test_final_state, test_capacity,
                                             True, True), "")
        self.assertEqual(
            self.calculator.cost_calculation(test_configuration, test_initial_state, test_final_state, test_capacity,
                                             False, True), "")
        self.assertEqual(
            self.calculator.cost_calculation(test_configuration, test_initial_state, test_final_state, test_capacity,
                                             True, False), "")
        self.assertEqual(
            self.calculator.cost_calculation(test_configuration, test_initial_state, test_final_state, test_capacity,
                                             False, False), "")

    def test_time(self):
        self.calculator = Calculator()
        test_configuration = "1"
        test_initial_state = 10
        test_final_state = 100
        test_capacity = 80
        self.assertEqual(self.calculator.time_calculation("2", test_initial_state, test_final_state, test_capacity),
                         False)
        self.assertEqual(self.calculator.time_calculation("1", test_initial_state, test_final_state, test_capacity),
                         False)
        self.assertEqual(self.calculator.time_calculation("3", test_initial_state, test_final_state, test_capacity),
                         False)
        self.assertEqual(self.calculator.time_calculation("4", test_initial_state, test_final_state, test_capacity),
                         False)
        self.assertEqual(self.calculator.time_calculation("5", test_initial_state, test_final_state, test_capacity),
                         False)
        self.assertEqual(self.calculator.time_calculation("6", test_initial_state, test_final_state, test_capacity),
                         False)
        self.assertEqual(self.calculator.time_calculation("7", test_initial_state, test_final_state, test_capacity),
                         False)
        self.assertEqual(self.calculator.time_calculation("8", test_initial_state, test_final_state, test_capacity),
                         False)

    # you may create test suite if needed
    if __name__ == "__main__":
        pass

#import main
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

class TestCalculator(unittest.TestCase):

    # you may create more test methods
    # you may add parameters to test methods
    # this is an example
    def test_power(self):
        cal = Calculator()
        with self.assertRaises(KeyError):
            self.assertRaises(KeyError, cal.get_power("9"))
        
        self.assertEqual(cal.get_power("1"), 2)
        
    
    def test_baseprice(self):
        cal= Calculator()
        with self.assertRaises(KeyError):
               self.assertRaises(KeyError, cal.get_base_price("-1"))
        
        self.assertEqual(cal.get_base_price("1"), 5)


    def test_ispeak(self):
        cal=Calculator()
        self.assertEqual(cal.is_peak("05:59"),False)
        self.assertEqual(cal.is_peak("06:00"),True)
        self.assertEqual(cal.is_peak("18:00"),True)
        self.assertEqual(cal.is_peak("18:01"),False)

    def test_is_holiday(self):
        cal=Calculator()
        self.assertEqual(cal.is_holiday("2021-01-01"), True)
        self.assertEqual(cal.is_holiday("2021-01-02"), True)


    def test_chargetime(self):
        cal=Calculator()
        self.assertEqual(cal.charge_time(80,20,80,350), 9)

    def test_inc_time(self):
        cal=Calculator()
        test_time=datetime.datetime.strptime("2021-01-02", "%Y-%m-%d")
        ref=test_time+ datetime.timedelta(minutes=1)
        self.assertEqual(cal.inc_time(test_time), ref)

    def test_cal_cost_per_min(self):
        cal=Calculator()
        self.assertEqual(cal.cal_cost_per_min(350,5,1.1,0.5),0.16041666666666665)


    def test_cal_cost(self):
        cal=Calculator()
        self.assertEqual(cal.cal_cost(8,50,"18:01", "2021-01-01", 350), 12.83333333333333 )
        self.assertEqual(cal.cal_cost(8,50,"18:00","2021-01-01", 350 ),14.437499999999996 )
        self.assertEqual(cal.cal_cost(8,50,"06:00","2021-01-01",  350),25.66666666666666 )
        self.assertEqual(cal.cal_cost(8,50,"05:59","2021-01-01",  350), 24.062499999999993)
        self.assertEqual(cal.cal_cost(8,50,"23:59","2021-01-02",  350), 12.83333333333333)

    def test_add_time(self):
        cal=Calculator()
        self.assertEqual(cal.add_time("05:01", "05:59"), "11:0")
        self.assertEqual(cal.add_time("05:00", "00:30"), "5:30")
        self.assertEqual(cal.add_time("05:01", "05:59"), "11:0")

    def test_minus_time(self):
        cal=Calculator()
        self.assertEqual(cal.minus_time("05:00", "05:20"), "0:20")
    
    def test_add_time(self):
        cal=Calculator()
        self.assertEqual(cal.add_time("05:00", "05:20"), "10:20")

    def test_mtoh(self):
        cal=Calculator()
        self.assertEqual(cal.m_to_h(150), "2:30")
        self.assertEqual(cal.m_to_h(250), "4:10")
        self.assertEqual(cal.m_to_h(0), "0:0")
        with self.assertRaises(TypeError):
            cal.m_to_h("a")
    
    def test_htom(self):
        cal=Calculator()
        self.assertEqual(cal.h_to_m("2:30"),150)


    def test_solar_energy_aux(self):
         cal=Calculator()
         self.assertEqual(cal.solar_energy_aux("2021-01-01", "21:00", "2313", 80, 20, 80, 350))

    # you may create test suite if needed
    if __name__ == "__main__":
        pass

def main():
    suit = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    unittest.TextTestRunner(verbosity=1).run(suit)
    
main()
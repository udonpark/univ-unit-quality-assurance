import datetime
    
from app.calculator import *

import unittest
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
        # mock = Mock()
        # attrs = {'method.return_value':"05:59", ''}
        self.assertEqual(cal.is_peak("05:59"),False)
        self.assertEqual(cal.is_peak("06:00"),True)
        self.assertEqual(cal.is_peak("18:00"),True)
        self.assertEqual(cal.is_peak("18:01"),False)

    def test_is_holiday(self):
        # Calculator.is_holiday = Mock()
        # holi_new_yr = "2020-01-01"
        # Calculator.return_value = True

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
        self.assertEqual(cal.m_to_h(0), "0:00")
        with self.assertRaises(TypeError):
            cal.m_to_h("a")
    
    def test_htom(self):
        cal=Calculator()
        self.assertEqual(cal.h_to_m("2:30"),150)


    def test_solar_energy_aux(self):
        cal=Calculator()
        #self.assertEqual(cal.solar_energy_aux("01-01-2020", "21:00", "3800", 80, 20, 80, 350),([], [], '19:45') )
        self.assertEqual(cal.solar_energy_aux("01-01-2020", "12:00", "3800", 80, 20, 80, 350), ([0.05966101694915255, 0.029830508474576276],
 ['12:00', '13:00', '13:30'], '13:30'))
        self.assertEqual(cal.solar_energy_aux("28-02-2017", "23:00", "3800", 80, 20, 80, 350),([], [], '19:01'))

        self.assertEqual(cal.solar_energy_aux("14-09-2021", "12:40", "3800", 80, 20, 2000, 50), ([0.013295615275813298,
  0.03988684582743989,
  0.03988684582743989,
  0.03988684582743989,
  0.03988684582743989,
  0.03988684582743989,
  0.005983026874115984],
 ['12:40', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '18:09'],
 '18:09'))

    def test_calculate_solar_energy(self):
        cal = Calculator()
        self.assertEqual(cal.calculate_solar_energy("04-06-2020", "12:00", "3800", 80, 20, 80, 350), (
        [0.02517241379310345, 0.012586206896551724], ['12:00', '13:00', '13:30']))
        self.assertEqual(cal.calculate_solar_energy("13-07-2028", "13:50", "3800", 80, 10, 300, 700),
                         ([0.0036506330845953497, 0.021903798507572098, 0.0073012661691906995],
                          ['13:50', '14:00', '15:00', '14:80']))

    # MOCKING for api functions

    def test_get_sun_hour(self):
        cal = Calculator()
        # mock = Mock()
        # mock.return_value = {
        #     "postcode": "3800",
        #     "date":"01-01-2020",
        # }

        #attr = {'method.get_sunlight_hours': 8.8, 'something.'}
        self.assertEqual(cal.get_sun_hour("3800", "01-01-2020"),8.8)
        self.assertEqual(cal.get_sun_hour("3800", "01-02-2020"),0.9)
        
        self.assertEqual(cal.get_sun_hour("3800", "01-01-2020"), 8.8)
        self.assertEqual(cal.get_sun_hour("3800", "01-02-2020"), 0.9)

    def test_get_day_light_length(self):
        cal = Calculator()
        self.assertEqual(cal.get_day_light_length("3800", "30-04-2021"), 10.566666666666666)
        self.assertEqual(cal.get_day_light_length("3800", "30-04-2021"), 10.566666666666666)

    def test_get_cloud_cover(self):
        cal = Calculator()
        self.assertEqual(cal.get_cloud_cover("3800", "30-04-2021", "08:00"),None)
        self.assertEqual(cal.get_cloud_cover("3800", "21-04-2021", "14:00"),None)

        #self.assertEqual(cal.get_cloud_cover("3830", "30-04-2021"),"")

        self.assertEqual(cal.get_cloud_cover("3800", "30-04-2021", "08:00"), None)
        self.assertEqual(cal.get_cloud_cover("3800", "21-04-2021", "14:00"), None)

def main():
    suit = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    unittest.TextTestRunner(verbosity=1).run(suit)
    
main()
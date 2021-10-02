# import datetime
    
# from app.calculator import *
try:
    from app.calculator import *
except ImportError:
    # fix import issues
    # ref: https://stackoverflow.com/questions/54339118/python3-x-modulenotfounderror-when-import-file-from-parent-directory/54340672
    import sys
    sys.path.append(sys.path[0] + "/..")
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
        self.assertEqual(cal.is_holiday("01/01/2021"), True)
        self.assertEqual(cal.is_holiday("02/01/2021"), True)
        self.assertEqual(cal.is_holiday("09/01/2021"), True)


    def test_chargetime(self):
        cal=Calculator()
        self.assertEqual(cal.charge_time(80,20,80,350), 9)

    def test_inc_time(self):
        cal=Calculator()
        test_time=datetime.datetime.strptime("01/01/2021", "%d/%m/%Y")
        ref=test_time+ datetime.timedelta(minutes=1)
        self.assertEqual(cal.inc_time(test_time), ref)

    def test_cal_cost_per_min(self):
        cal=Calculator()
        self.assertEqual(cal.cal_cost_per_min(350,5,1.1,0.5),0.16041666666666665)

    #CHANGES
    def test_cal_cost(self):
        cal=Calculator()
        self.assertEqual(cal.cal_cost(8,50,"18:01", "01-01-2021", 350), 12.83333333333333 )
        self.assertEqual(cal.cal_cost(8,50,"18:00","01-01-2021", 350 ),14.437499999999996 )
        self.assertEqual(cal.cal_cost(8,50,"01:00","12-01-2021",  350),11.666666666666664  )
        self.assertEqual(cal.cal_cost(8,50,"15:30","12-01-2021",  350), 23.33333333333333)

    #CHANGES
    def test_add_time(self):
        cal=Calculator()
        self.assertEqual(cal.add_time("05:01", "05:59"), "11:00")
        self.assertEqual(cal.add_time("05:00", "00:30"), "5:30")
        self.assertEqual(cal.add_time("05:00", "05:00"), "10:00")

    #CHANGES MADE
    def test_minus_time(self):
        cal=Calculator()
        self.assertEqual(cal.minus_time("01:20", "05:30"), "4:10")
        self.assertEqual(cal.minus_time("00:30", "05:00"), "4:30")
        self.assertEqual(cal.minus_time("03:10", "05:00"), "1:50")

    #CHANGES MADE
    def test_mtoh(self):
        cal=Calculator()
        self.assertEqual(cal.m_to_h(150), "2:30")
        self.assertEqual(cal.m_to_h(120), "2:00")
        self.assertEqual(cal.m_to_h(30), "0:30")
        with self.assertRaises(TypeError):
            cal.m_to_h("a")
    
    def test_htom(self):
        cal=Calculator()
        self.assertEqual(cal.h_to_m("2:30"),150)


    def test_solar_energy_aux(self):
        cal=Calculator()
        #self.assertEqual(cal.solar_energy_aux("01-01-2020", "21:00", "3800", 80, 20, 80, 350),([], [], '19:45') )
        self.assertEqual(cal.solar_energy_aux("01-01-2020", "12:00", "3800", 80, 20, 80, 350), ([5.966101694915255, 2.953220338983051], ['12:00', '13:00', '13:30'], '13:30'))
        self.assertEqual(cal.solar_energy_aux("28-02-2017", "23:00", "3800", 80, 20, 80, 350),([], [], '19:01'))

        self.assertEqual(cal.solar_energy_aux("14-09-2021", "12:40", "3800", 80, 20, 2000, 50), ([0.6248939179632249,
  1.794908062234795,
  1.6752475247524754,
  1.5555869872701555,
  1.5954738330975957,
  1.5954738330975957,
  0.23932107496463936],
 ['12:40', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '18:09'],
 '18:09'))

    def test_calculate_solar_energy(self):
        cal = Calculator()
        self.assertEqual(cal.calculate_solar_energy("04-06-2020", "12:00", "3800", 80, 20, 80, 350), ([1.6427586206896552, 0.8046551724137933], ['12:00', '13:00', '13:30']))
        self.assertEqual(cal.calculate_solar_energy("13-07-2028", "13:50", "3800", 80, 10, 300, 700),
                         ([0.13136024003948532, 0.8304942018149566, 0.29094232113100044],
                          ['13:50', '14:00', '15:00', '14:80']))


    def test_get_sun_hour(self):
        cal = Calculator()
        self.assertEqual(cal.get_sun_hour("3800", "01-01-2020"),8.8)
        self.assertEqual(cal.get_sun_hour("3800", "01-02-2020"),0.9)
        self.assertEqual(cal.get_sun_hour("2620", "21-03-2021"),1.4)
        self.assertEqual(cal.get_sun_hour("3300", "22-09-2019"),3.6)

    def test_get_day_light_length(self):
        cal = Calculator()
        self.assertEqual(cal.get_day_light_length("3800", "30-04-2021"), 10.566666666666666)
        self.assertEqual(cal.get_day_light_length("3800", "01-05-2021"), 10.533333333333333)
        self.assertEqual(cal.get_day_light_length("2620", "17-05-2020"), 10.216666666666667)
        self.assertEqual(cal.get_day_light_length("3300", "15-09-2020"),  11.85)

    def test_get_cloud_cover(self):
        cal = Calculator()
        self.assertEqual(cal.get_cloud_cover("3800", "30-04-2021", "08:00"),9)
        self.assertEqual(cal.get_cloud_cover("3800", "21-04-2021", "14:00"),71)
        self.assertEqual(cal.get_cloud_cover("2620", "17-05-2020", "14:00"),1)
        self.assertEqual(cal.get_cloud_cover("3300", "15-09-2020", "14:00"),44)

def main():
    suit = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    unittest.TextTestRunner(verbosity=2).run(suit)
    
main()
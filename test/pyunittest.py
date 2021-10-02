from app.calculator import *

import unittest
class TestCalculator(unittest.TestCase):

    # you may create more test methods
    # you may add parameters to test methods
    # this is an example
    def test_power(self):
        """
        This function is used to test that power is correctly obtained
        """
        cal = Calculator()
        """
        The first test case checks to see whether the correct error is raised if invalid configuration is entered
        The second test case checks whether the corresponding power is returned based on the configuration umber entered
        """
        with self.assertRaises(KeyError):
            self.assertRaises(KeyError, cal.get_power("9"))
        
        self.assertEqual(cal.get_power("1"), 2)
        
    
    def test_baseprice(self):
        cal= Calculator()
        """
        The first test case checks to see whether the correct error is raised if invalid configuration is entered
        The second test case checks whether the corresponding base price is returned based on the configuration umber entered
        """
        with self.assertRaises(KeyError):
               self.assertRaises(KeyError, cal.get_base_price("-1"))
        
        self.assertEqual(cal.get_base_price("1"), 5)


    def test_ispeak(self):
        cal=Calculator()

        """
        The first test case checks to see whether the is_peak returns the correct boolean value (as 05:59 is off peak)
        The second test case is taken as an on-point value for the boundary testing to see if it returns the correct boolean value
        The third test case is taken as an in point value for the boundary testing to see if it returns the correct boolean value
        Fourth test case is an off-point value to cehck if it returns False(as it is off-peak)
        """

        self.assertEqual(cal.is_peak("05:59"),False)
        self.assertEqual(cal.is_peak("06:00"),True)
        self.assertEqual(cal.is_peak("18:00"),True)
        self.assertEqual(cal.is_peak("18:01"),False)

    def test_is_holiday(self):

        cal=Calculator()

        """
        First test case is used to check for whether a holiday date returns True
        Second test case checks for the working day
        Third test case checks for whether it is a weekend 
        """
        self.assertEqual(cal.is_holiday("01/01/2021"), True)
        self.assertEqual(cal.is_holiday("02/01/2021"), True)
        self.assertEqual(cal.is_holiday("09/01/2021"), True)


    def test_chargetime(self):
        cal=Calculator()
        """
        Random testing was used for this function. 
        Assumptions: final state of charge entered is always greater than initial state of charge since validation check has already been done in the calculator_form.py

        """
        self.assertEqual(cal.charge_time(80,20,80,350), 9)

    def test_inc_time(self):
        cal=Calculator()

        """
        Assumptions: input is a string in datetime format “dd/MM/YYYY”
        Random testing was used because the function increments the time given by 1 minute only. 
        """
        test_time=datetime.datetime.strptime("01/01/2021", "%d/%m/%Y")
        ref=test_time+ datetime.timedelta(minutes=1)
        self.assertEqual(cal.inc_time(test_time), ref)

    def test_cal_cost_per_min(self):
        cal=Calculator()
        """
        Random testing was used because the function performs a calculation solely dependent on the inputs only. 
        """
        self.assertEqual(cal.cal_cost_per_min(350,5,1.1,0.5),0.16041666666666665)

    #CHANGES
    def test_cal_cost(self):
        cal=Calculator()
        """
        In this case Pairwise testing was used
        First test case checks for cal_cost when it is a holiday and it is an on-peak time
        Second test case checks for cal_cost when it is a holiday and it is not an on-peak time
        Third test case checks for cal_cost when it is not a holiday and it is not an on-peak time
        Fourth test case checks for cal_cost when it is a holiday and it is an on-peak time
        """
        self.assertEqual(cal.cal_cost(8,50,"18:01", "01-01-2021", 350), 12.83333333333333 )
        self.assertEqual(cal.cal_cost(8,50,"18:00","01-01-2021", 350 ),14.437499999999996 )
        self.assertEqual(cal.cal_cost(8,50,"01:00","12-01-2021",  350),11.666666666666664  )
        self.assertEqual(cal.cal_cost(8,50,"15:30","12-01-2021",  350), 23.33333333333333)

    #CHANGES
    def test_add_time(self):
        cal=Calculator()

        """
        Category Partition Testing was used
        First test case checks for when two input minutes will increment the time
        Second test case checks that hours are not affected while incrementing time
        Third test case checks for when only hour is incremented
        """
        self.assertEqual(cal.add_time("05:01", "05:59"), "11:00")
        self.assertEqual(cal.add_time("05:00", "00:30"), "5:30")
        self.assertEqual(cal.add_time("05:00", "05:00"), "10:00")

    #CHANGES MADE
    def test_minus_time(self):
        cal=Calculator()

        """
        Here category testing was used
        First test case tests that minutes and hours are deducted correctly
        Second test case tests that minutes correctly deduct from hours 
        Third test case  checks that both minutes and hours are correctly deducted when deducted minutes is greater, 
        incurring an hour loss
        """
        self.assertEqual(cal.minus_time("01:20", "05:30"), "4:10")
        self.assertEqual(cal.minus_time("00:30", "05:00"), "4:30")
        self.assertEqual(cal.minus_time("03:10", "05:00"), "1:50")

    #CHANGES MADE
    def test_mtoh(self):
        cal=Calculator()

        """
        Category Partition Testing was used
        We split this into three partitions:
        
        First test case checks that the input minutes converted to hours and minutes
        Second test case  checks that the input minutes converted to hours only
        Third test case checks that input minutes converted to minutes only. 

        """

        self.assertEqual(cal.m_to_h(150), "2:30")
        self.assertEqual(cal.m_to_h(120), "2:00")
        self.assertEqual(cal.m_to_h(30), "0:30")
        with self.assertRaises(TypeError):
            cal.m_to_h("a")
    
    def test_htom(self):
        cal=Calculator()
        """
        Random testing was used for this function to compute the hours converted to minutes. 
        """

        self.assertEqual(cal.h_to_m("2:30"),150)


    def test_solar_energy_aux(self):
        cal=Calculator()
        """
        Rationale:
        In this case random testing had to be used as the number of possible combinations were extremely large and hence
        it was not feasible to cover them all 
        """
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
        """
        Random testing was used to validate
        """
        self.assertEqual(cal.calculate_solar_energy("04-06-2020", "12:00", "3800", 80, 20, 80, 350), ([1.6427586206896552, 0.8046551724137933], ['12:00', '13:00', '13:30']))
        self.assertEqual(cal.calculate_solar_energy("13-07-2028", "13:50", "3800", 80, 10, 300, 700),
                         ([0.13136024003948532, 0.8304942018149566, 0.29094232113100044],
                          ['13:50', '14:00', '15:00', '14:80']))


    def test_get_sun_hour(self):
        cal = Calculator()

        """
        Random testing was used with different dates and postcodes were used 

        Rationale:
        Random testing will allow bugs to be identified quickly since it takes in different combinations of inputs.

        """
        self.assertEqual(cal.get_sun_hour("3800", "01-01-2020"),8.8)
        self.assertEqual(cal.get_sun_hour("3800", "01-02-2020"),0.9)
        self.assertEqual(cal.get_sun_hour("2620", "21-03-2021"),1.4)
        self.assertEqual(cal.get_sun_hour("3300", "22-09-2019"),3.6)

    def test_get_day_light_length(self):
        cal = Calculator()
        """
        Random testing was used with different dates and postcodes were used

        Rationale:
        Random testing will allow bugs to be identified quickly since it takes in different combinations of inputs.

        """

        self.assertEqual(cal.get_day_light_length("3800", "30-04-2021"), 10.566666666666666)
        self.assertEqual(cal.get_day_light_length("3800", "01-05-2021"), 10.533333333333333)
        self.assertEqual(cal.get_day_light_length("2620", "17-05-2020"), 10.216666666666667)
        self.assertEqual(cal.get_day_light_length("3300", "15-09-2020"),  11.85)

    def test_get_cloud_cover(self):
        cal = Calculator()
        """
        Random testing was used with different dates and postcodes were used

        Rationale:
        Random testing will allow bugs to be identified quickly since it takes in different combinations of inputs.
        """

        self.assertEqual(cal.get_cloud_cover("3800", "30-04-2021", "08:00"),9)
        self.assertEqual(cal.get_cloud_cover("3800", "21-04-2021", "14:00"),71)
        self.assertEqual(cal.get_cloud_cover("2620", "17-05-2020", "14:00"),1)
        self.assertEqual(cal.get_cloud_cover("3300", "15-09-2020", "14:00"),44)

def main():
    suit = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    unittest.TextTestRunner(verbosity=2).run(suit)
    
main()
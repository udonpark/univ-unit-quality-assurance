from flask import request
from flask import Flask
from wtforms import ValidationError

import app.calculator_form as cal
import unittest


testvalue = 0
testnull = None
teststring = ""


class TestCase(unittest.TestCase):
    """
    This class is used to test the validate functions of the calculator_form.py file
    """
    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def create_app(self):
        app = Flask(__name__)
        app.secret_key = "secret"
        return app

    def request(self, *args, **kwargs):
        return self.app.test_request_context(*args, **kwargs)

    def test_validateBatteryPack(self):
        """
        This function tests for the validateBatteryPack function
        We use a variety of inputs to ensure that we cover every if statement in the validateBatteryPack function
        """
        #checking whether it raises error or not

        #test1
        with self.request(method='POST', data={'BatteryPackCapacity': "45"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            try:
                f.validate_BatteryPackCapacity(f.BatteryPackCapacity)
            except ValueError as val:
                assert False, "Should not raise exception"

        #test2
        with self.request(method='POST', data={'BatteryPackCapacity': None}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_BatteryPackCapacity(f.BatteryPackCapacity)

        #test3
        with self.request(method='POST', data={'BatteryPackCapacity': "test"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_BatteryPackCapacity(f.BatteryPackCapacity)

        #test4
        with self.request(method='POST', data={'BatteryPackCapacity': "-1"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_BatteryPackCapacity(f.BatteryPackCapacity)

        #test5
        with self.request(method='POST', data={'BatteryPackCapacity': ""}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_BatteryPackCapacity(f.BatteryPackCapacity)

    def test_validateInitialCharge(self):
        """
        This function tests for the validateInitialCharge function
        We use a variety of inputs to ensure that we cover every if statement in the validateInitialCharge function
        """
        #checking whether it raises error or not

        #test1
        with self.request(method='POST', data={'InitialCharge': "40"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            try:
                f.validate_InitialCharge(f.InitialCharge)
            except ValueError as val:
                assert False, "Should not raise exception"

        #test2
        with self.request(method='POST', data={'InitialCharge': None}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_InitialCharge(f.InitialCharge)

        #test3
        with self.request(method='POST', data={'InitialCharge': ''}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_InitialCharge(f.InitialCharge)

        #test4
        with self.request(method='POST', data={'InitialCharge': "test"}):

            f1 = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f1.validate_InitialCharge(f1.InitialCharge)

        #test5
        with self.request(method='POST', data={'InitialCharge': "0"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            try:
                f.validate_InitialCharge(f.InitialCharge)
            except ValueError as val:
                assert False, "Should not raise exception"

        #test6
        with self.request(method='POST', data={'InitialCharge': "101"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_InitialCharge(f.InitialCharge)

        #test7
        with self.request(method='POST', data={'InitialCharge': "-1"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_InitialCharge(f.InitialCharge)

    def test_validateFinalCharge(self):
        """
        This function tests for the validateFinalCharge function
        We use a variety of inputs to ensure that we cover every if statement in the validateFinalCharge function
        """
        #checking whether it raises error or not

        #test1
        with self.request(method='POST', data={'FinalCharge': "40"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            try:
                f.validate_FinalCharge(f.FinalCharge)
            except ValueError as val:
                assert False, "Should not raise exception"

        #test2
        with self.request(method='POST', data={'FinalCharge': "0"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            try:
                f.validate_FinalCharge(f.FinalCharge)
            except ValueError as val:
                assert False, "Should not raise exception"

        #test3
        with self.request(method='POST', data={'FinalCharge': None}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_FinalCharge(f.FinalCharge)

        #test4
        with self.request(method='POST', data={'FinalCharge': ''}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_FinalCharge(f.FinalCharge)

        #test5
        with self.request(method='POST', data={'FinalCharge': "101"}):
            f1 = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f1.validate_FinalCharge(f1.FinalCharge)

        #test6
        with self.request(method='POST', data={'FinalCharge': "-1"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_InitialCharge(f.FinalCharge)

        #test7
        with self.request(method='POST', data={'FinalCharge': "non-numerical"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_InitialCharge(f.FinalCharge)

    def test_validateChargerConfiguration(self):
        """
        This function tests for the validateChargerConfiguration function
        Note:we use boundary value testing to make sure that no inputs outside the boundary are accepted
        """

        #test1
        with self.request(method='POST', data={'ChargerConfiguration': None}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_ChargerConfiguration(f.ChargerConfiguration)

        #test2
        with self.request(method='POST', data={'ChargerConfiguration': ''}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_ChargerConfiguration(f.ChargerConfiguration)

        #test3
        with self.request(method='POST', data={'ChargerConfiguration': "10"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_ChargerConfiguration(f.ChargerConfiguration)

        #test4
        with self.request(method='POST', data={'ChargerConfiguration': "-1"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_ChargerConfiguration(f.ChargerConfiguration)

        #test5
        with self.request(method='POST', data={'ChargerConfiguration': "8"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            try:
                f.validate_ChargerConfiguration(f.ChargerConfiguration)
            except ValueError as val:
                assert False, "Should not raise exception"

    def test_validatePostcode(self):
        """
        This function tests for the validatePostCode function
        """

        #test1
        with self.request(method='POST', data={'PostCode': "3800"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            try:
                f.validate_PostCode(f.PostCode)
            except ValueError as val:
                assert False, "Should not raise exception"

        #test2
        with self.request(method='POST', data={'PostCode': "10000"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_PostCode(f.PostCode)

        #test3
        with self.request(method='POST', data={'PostCode': "1000.90"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_PostCode(f.PostCode)

    def test_validateStartDate(self):
        """
        This function tests for the validateStartDate function
        """

        #test1
        with self.request(method='POST', data={'StartDate': "23/02/2020"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            try:
                f.validate_StartDate(f.StartDate)
            except ValueError as val:
                assert False, "Should not raise exception"

        #test2
        with self.request(method='POST', data={'StartDate': " "}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValidationError):
                f.validate_StartDate(f.StartDate)

        #test3
        with self.request(method='POST', data={'StartDate': "2030-11-27"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValidationError):
                f.validate_StartDate(f.StartDate)

        #test4
        with self.request(method='POST', data={'StartDate': "2015-02-07"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValidationError):
                f.validate_StartDate(f.StartDate)

        with self.request(method='POST', data={'StartDate': "2008-06-29"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValidationError):
                f.validate_StartDate(f.StartDate)

    def test_validateStartTime(self):
        """
        This function tests for the validateStartTime function
        """

        #test1
        with self.request(method='POST', data={'StartTime': "23:50"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            try:
                f.validate_StartTime(f.StartTime)
            except ValueError as val:
                assert False, "Should not raise exception"

        #test2
        with self.request(method='POST', data={'StartTime': " "}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_StartTime(f.StartTime)

        #test3
        with self.request(method='POST', data={'StartTime': "24:50"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_StartTime(f.StartTime)

        #test4
        with self.request(method='POST', data={'StartTime': "23:60"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValidationError):
                f.validate_StartTime(f.StartTime)

        #test5
        with self.request(method='POST', data={'StartTime': "-1:60"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValidationError):
                f.validate_StartTime(f.StartTime)

        #test6
        with self.request(method='POST', data={'StartTime': "23:-1"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValidationError):
                f.validate_StartTime(f.StartTime)


def main():
    suit = unittest.TestLoader().loadTestsFromTestCase(TestCase)
    unittest.TextTestRunner(verbosity=2).run(suit)

main()

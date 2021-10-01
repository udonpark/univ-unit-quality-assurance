from flask import request
from flask import Flask
from wtforms import ValidationError

import app.calculator_form as cal
import unittest


testvalue = 0
testnull = None
teststring = ""


class TestCase(unittest.TestCase):
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
        #checking whether it raises error or not

        with self.request(method='POST', data={'BatteryPackCapacity': "-1"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_BatteryPackCapacity(f.BatteryPackCapacity)

        with self.request(method='POST', data={'BatteryPackCapacity': "test"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_BatteryPackCapacity(f.BatteryPackCapacity)

        with self.request(method='POST', data={'BatteryPackCapacity': ""}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_BatteryPackCapacity(f.BatteryPackCapacity)

    def test_validateInitialCharge(self):
        #checking whether it raises error or not

        with self.request(method='POST', data={'InitialCharge': None}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_InitialCharge(f.InitialCharge)

        with self.request(method='POST', data={'InitialCharge': ''}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_InitialCharge(f.InitialCharge)

        with self.request(method='POST', data={'InitialCharge': "-90"}):

            f1 = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f1.validate_InitialCharge(f1.InitialCharge)

        with self.request(method='POST', data={'InitialCharge': "-1"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_InitialCharge(f.InitialCharge)

    def test_validateFinalCharge(self):
        #checking whether it raises error or not

        with self.request(method='POST', data={'FinalCharge': None}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_InitialCharge(f.FinalCharge)

        with self.request(method='POST', data={'FinalCharge': ''}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_FinalCharge(f.InitialCharge)

        with self.request(method='POST', data={'FinalCharge': "-90"}):
            f1 = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f1.validate_FinalCharge(f1.FinalCharge)

        with self.request(method='POST', data={'FinalCharge': "-1"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_InitialCharge(f.FinalCharge)

    def test_validateChargerConfiguration(self):
        with self.request(method='POST', data={'ChargerConfiguration': None}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_ChargerConfiguration(f.ChargerConfiguration)

        with self.request(method='POST', data={'ChargerConfiguration': ''}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_ChargerConfiguration(f.ChargerConfiguration)

        with self.request(method='POST', data={'ChargerConfiguration': "10"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_ChargerConfiguration(f.ChargerConfiguration)

        with self.request(method='POST', data={'ChargerConfiguration': "-1"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_ChargerConfiguration(f.ChargerConfiguration)

        with self.request(method='POST', data={'ChargerConfiguration': "8"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            try:
                f.validate_ChargerConfiguration(f.ChargerConfiguration)
            except ValueError as val:
                assert False, "Should not raise exception"

    def test_validatePostcode(self):
        with self.request(method='POST', data={'PostCode': "3800"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            try:
                f.validate_PostCode(f.PostCode)
            except ValueError as val:
                assert False, "Should not raise exception"

        with self.request(method='POST', data={'PostCode': "10000"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_PostCode(f.PostCode)

        with self.request(method='POST', data={'PostCode': "1000.90"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_PostCode(f.PostCode)

    def test_validateStartDate(self):
        with self.request(method='POST', data={'StartDate': "23/02/2020"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            try:
                f.validate_StartDate(f.StartDate)
            except ValueError as val:
                assert False, "Should not raise exception"

        with self.request(method='POST', data={'StartDate': " "}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValidationError):
                f.validate_StartDate(f.StartDate)

        with self.request(method='POST', data={'StartDate': "2030-11-27"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValidationError):
                f.validate_StartDate(f.StartDate)

        with self.request(method='POST', data={'StartDate': "2015-02-07"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValidationError):
                f.validate_StartDate(f.StartDate)

    def test_validateStartTime(self):
        with self.request(method='POST', data={'StartTime': "23:50"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            try:
                f.validate_StartTime(f.StartTime)
            except ValueError as val:
                assert False, "Should not raise exception"

        with self.request(method='POST', data={'StartTime': " "}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_StartTime(f.StartTime)

        with self.request(method='POST', data={'StartTime': "24:50"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValueError):
                f.validate_StartTime(f.StartTime)

        with self.request(method='POST', data={'StartTime': "23:60"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValidationError):
                f.validate_StartTime(f.StartTime)

        with self.request(method='POST', data={'StartTime': "-1:60"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValidationError):
                f.validate_StartTime(f.StartTime)

        with self.request(method='POST', data={'StartTime': "23:-1"}):
            f = cal.Calculator_Form(request.form, data={'csrf': False})
            with self.assertRaises(ValidationError):
                f.validate_StartTime(f.StartTime)


if __name__ == '__main__':
    unittest.main()

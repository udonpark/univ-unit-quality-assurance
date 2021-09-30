import flask
import mock as mock
from flask import current_app, g, jsonify, request
from flask import Flask
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Required
import requests

import main
from app.calculator import *
import app.calculator_form as cal
import unittest
from unittest.mock import Mock
from mock import patch

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

        @app.route("/ajax/", methods=("POST",))
        def ajax_submit():
            form = cal.Calculator_Form(csrf_enabled=False)

            if form.validate_on_submit():
                return jsonify(name=form.name.data, success=True, errors=None)

            return jsonify(name=None, errors=form.errors, success=False)

        return app

    def request(self, *args, **kwargs):
        return self.app.test_request_context(*args, **kwargs)

    def test_submitted_and_valid(self):
        with self.request(method='POST', data={'BatteryPackCapacity': 'testt'}):
            f = cal.Calculator_Form(request.form, meta={'csrf': False})
            f.BatteryPackCapacity.data = 'test'
            print(f.BatteryPackCapacity)
            self.assertRaises(ValueError, f.validate_BatteryPackCapacity(f.BatteryPackCapacity))


# class MyTestCase(unittest.TestCase):
#
#     def test_mock(self):
#         with patch.object(requests, 'request.form') as get_mock:
#             get_mock.return_value = 'non-numerical'
#             self.assertRaises(ValueError, cal.Calculator_Form.validate_BatteryPackCapacity(mock, '<test>'))
#             # request.form['BatteryPackCapacity']
#
#
#     def test_BatteryPackCapacity(self):
#         mock = Mock()
#
#         # mockvalue = StringField("Battery Pack Capacity", [' '])
#         # self.assertRaises(ValueError, cal.Calculator_Form.validate_BatteryPackCapacity(self.mock_capacity, mockvalue))
#         # self.assertEqual(True, False)  # add assertion here
#
#         # mockvalue = StringField("Battery Pack Capacity", ["non-numerical"])
#         mockvalue = StringField()
#         # mockvalue.raw_data = "non-numerical"
#         # self.assertRaises(ValueError, cal.Calculator_Form.validate_BatteryPackCapacity(mock_capacity, mockvalue))
#         # mock_capacity.return_value = "non-numerical"
#         # mock_capacity.return_value = ["Battery Pack Capacity", ["non-numerical"]]
#         print(mock)
#         print(mockvalue)
#         self.assertRaises(ValueError, cal.Calculator_Form.validate_BatteryPackCapacity(mock, '<test>'))
#
#
#
#     """
#     @mock.patch('app.calculator_form', return_value='non-numerical')
#     def test_Battery(self, dt):
#         main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False  # disable CSRF to prevent context errors
#         with main.ev_calculator_app.app_context():
#             # a = Flask.app_context(self)
#             tester = cal.Calculator_Form()
#             # test = StringField("Battery Pack Capacity", ["non-numerical"])
#             # print(test)
#             # a = Flask.test_client(self)
#             # mock = Mock()
#             # response = a.post()
#             self.assertRaises(ValueError, tester.validate_BatteryPackCapacity(dt))
#     """
#
#     """
#     @mock.patch('app.calculator_form', return_value='non-numerical')
#     def test_Battery(self, dt):
#         main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False  # disable CSRF to prevent context errors
#         with main.ev_calculator_app.app_context():
#             # a = Flask.app_context(self)
#             dt.return_value = 'non-numerical'
#             tester = cal.Calculator_Form()
#             # test = StringField("Battery Pack Capacity", ["non-numerical"])
#             # print(test)
#             # a = Flask.test_client(self)
#             # mock = Mock()
#             # response = a.post()
#             value = Mock().return_value
#             # print(self.return_value)
#             print(value)
#             self.assertRaises(ValueError, tester.validate_BatteryPackCapacity(value="hi"))
#     """
#
#     # place your testing code here
#     def test_InitialCharge(self):
#         pass
#
#     def test_FinalCharge(self):
#         pass
#
#     def test_StartTime(self):
#         pass
#
#     def test_ChargerConfiguration(self):
#         pass
#
#     def test_PostCode(self):
#         pass


if __name__ == '__main__':
    unittest.main()

import flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, Optional
import datetime 
# validation for form inputs
class Calculator_Form(FlaskForm):
    # this variable name needs to match with the input attribute name in the html file
    # you are NOT ALLOWED to change the field type, however, you can add more built-in validators and custom messages
    BatteryPackCapacity = StringField("Battery Pack Capacity", [DataRequired()])
    InitialCharge = StringField("Initial Charge", [DataRequired()])
    FinalCharge = StringField("Final Charge", [DataRequired()])
    StartDate = DateField("Start Date", [DataRequired("Data is missing or format is incorrect")], format='%d/%m/%Y')
    StartTime = TimeField("Start Time", [DataRequired("Data is missing or format is incorrect")], format='%H:%M')
    ChargerConfiguration = StringField("Charger Configuration", [DataRequired()])
    PostCode = StringField("Post Code", [DataRequired()])

    # use validate_ + field_name to activate the flask-wtforms built-in validator
    # this is an example for you

    #validating BatteryPackCapacity
    def validate_BatteryPackCapacity(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValueError("cannot fetch data")
        try:
            float_data = float(field.data)
        except ValueError:
            raise ValueError("Field data must be a numeric value")
        if float(field.data) <= 0:
            raise ValueError("Field data must be a positive value")

    # validate initial charge here
    def validate_InitialCharge(self, field):
        # another example of how to compare initial charge with final charge
        # you may modify this part of the code
        if field.data is None:
            raise ValidationError("Field data is none")
        elif field.data == '':
            raise ValueError("cannot fetch data")

        try:  # for ISoC, we only accept integers and not float
            int_data = int(field.data)
        except ValueError:
            raise ValueError("Field data must be an integer value")
        if int_data < 0:
            raise ValueError("Field data must be >= 0")
        elif int_data > 100:
            raise ValueError("Field data must be <= 100")
        # elif field.data > self.FinalCharge.data:
        #     raise ValueError("Initial charge data error")

    # validate final charge here
    def validate_FinalCharge(self, field):
        if field.data is None:
            raise ValidationError("Field data is none")
        elif field.data == '':
            raise ValueError("cannot fetch data")
        try:  # for FSoC, we only accept integers as we specified in As1
            int_data = int(field.data)
        except ValueError:
            raise ValueError("Field data must be an integer value")
        if int_data < 0:
            raise ValueError("Field data must be >= 0")
        elif int_data > 100:
            raise ValueError("Field data must be <= 100")


    # validate start date here
    def validate_StartDate(self, field):
        if field.data is None or "":
            raise ValidationError("Field data is empty or None")
        current_date=datetime.date.today()
        min_date=datetime.date(2008,7,1)
        # if field.data > current_date:
        #     raise ValidationError("Input date cannot be greater than today")
        if field.data < min_date:
            raise ValidationError("Input date cannot be before July 1st 2008")

    # validate start time here
    def validate_StartTime(self, field):
        if field.data is None or "":
            raise ValidationError("Field data is empty or None")
        hours= field.data.hour
        minute=field.data.minute
        if hours>23 or hours<0:
            raise ValidationError("Invalid hour")
        if minute>59 or minute<0:
            raise ValidationError("Invalid minutes")

    # validate charger configuration here
    def validate_ChargerConfiguration(self, field):
        if field.data is None or "":
            raise ValidationError("Field data is empty or None")
        try:
            int_data = int(field.data)
        except ValueError:
            raise ValueError("Incorrect configuration has been entered")
        if int_data < 0 or int_data > 9:
            raise ValueError("Configuration needs to be between 0 and 9")


    # validate postcode here
    def validate_PostCode(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValueError("cannot fetch data")

        try:
            int_data = int(field.data)
        except ValueError:
            raise ValueError("Incorrect configuration has been entered")

        if not (int_data in range(1000, 2000) or int_data in range(2000, 2600) or int_data in range(2619, 2900)
        or int_data in range(1000, 2000) or int_data in range(2000, 2600) or int_data in range(2619, 2900)
        or int_data in range(2921, 3000) or int_data in range(2600, 2619) or int_data in range(2900, 2921)
        or int_data in range(3000, 4000) or int_data in range(8000, 9000) or int_data in range(4000, 5000)
        or int_data in range(9000, 10000) or int_data in range(5000, 5800) or int_data in range(5800, 6000)
        or int_data in range(6000, 6798) or int_data in range(6800, 7000) or int_data in range(7000, 7800)
        or int_data in range(7800, 8000)
        or (field.data[0:2] == "02" and len(field.data) == 4)
        or (field.data[0:2] == "08" and len(field.data) == 4)
        or (field.data[0:2] == "09" and len(field.data == 4))):

            raise ValueError("Incorrect postcode entered")


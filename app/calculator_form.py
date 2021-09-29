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
    StartDate = DateField("Start Date", [DataRequired()], format='%Y-%m-%d') #[DataRequired("Data is missing or format is incorrect")], format='%d/%m/%Y'
    StartTime = TimeField("Start Time", [DataRequired("Data is missing or format is incorrect")], format='%H:%M')
    ChargerConfiguration = StringField("Charger Configuration", [DataRequired()])
    PostCode = StringField("Post Code", [DataRequired()])
    #
    # use validate_ + field_name to activate the flask-wtforms built-in validator
    # this is an example for you
    def validate_BatteryPackCapacity(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValueError("cannot fetch data")
        try:  # raise exception when it is non-numeric
            float_data = float(field.data)
        except ValueError:
            raise ValueError("Field data must be a numeric value")
        if float_data <= 0:
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
        elif field.data > self.FinalCharge.data:
            raise ValueError("Initial charge data error")

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
        current_date=datetime.date.today()
        min_date=datetime.date(2008,7,1)
        if field.data > current_date:
            raise ValidationError("Input date cannot be greater than today")
        elif field.data < min_date:
            raise ValidationError("Input date cannot be before July 1st 2008")

    # validate start time here
    #taskkill /f /im python.exe
    def validate_StartTime(self, field):
        pass        

    # validate charger configuration here
    def validate_ChargerConfiguration(self, field):
        pass

    # validate postcode here
    def validate_PostCode(self, field):
        pass
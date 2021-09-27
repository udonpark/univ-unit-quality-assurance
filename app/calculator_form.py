from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, Optional

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
        pass

    # validate start time here
    def validate_StartTime(self, field):
        pass

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
        if field.data == "":
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValueError("cannot fetch data")

        #List of postcodes
        postcode_ranges = [range(1000, 2000), range(2000, 2600), range(2619, 2900),
                           range(2921, 3000), range(2600, 2619), range(2900, 2921),
                           range(3000, 4000), range(8000, 9000), range(4000, 5000),
                           range(9000, 10000), range(5000, 5800), range(5800, 6000),
                           range(6000, 6798), range(6800, 7000), range(7000, 7800),
                           range(7800, 8000)]


        # or (str(int_data[0:2]) == "02" and len(str(int_data)) == 4)
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